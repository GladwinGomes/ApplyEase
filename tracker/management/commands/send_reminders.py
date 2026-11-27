from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from tracker.models import Reminder


class Command(BaseCommand):
    help = "Send email notifications for due, unsent application reminders."

    def handle(self, *args, **options):
        now = timezone.now()
        due_reminders = (
            Reminder.objects.select_related("application", "application__user", "application__job")
            .filter(is_sent=False, remind_on__lte=now)
        )

        sent_count = 0
        failed_count = 0
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@applyease.local")

        for reminder in due_reminders:
            user = reminder.application.user
            recipient = getattr(user, "email", None)
            if not recipient:
                continue

            job_label = str(reminder.application.job) if reminder.application.job else "your job application"
            subject = f"ApplyEase Reminder: {job_label}"
            body = (
                f"Hello,\n\n"
                f"This is your scheduled reminder for {job_label}.\n"
                f"Note: {reminder.message or 'Follow up on your application.'}\n\n"
                f"Best regards,\nApplyEase"
            )

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=from_email,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                reminder.is_sent = True
                reminder.save(update_fields=["is_sent"])
                sent_count += 1
            except Exception as exc:
                failed_count += 1
                self.stderr.write(
                    self.style.ERROR(f"Failed to send reminder #{reminder.id}: {exc}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Reminder check complete: {sent_count} sent, {failed_count} failed."
            )
        )
