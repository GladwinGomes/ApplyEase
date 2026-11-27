import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Skill
from jobs.models import Company, Job


class Command(BaseCommand):
    help = "Seed companies, skills, and jobs from seed_data CSV files."

    def handle(self, *args, **options):
        seed_dir = Path(settings.BASE_DIR) / "seed_data"

        skills_created = self._seed_skills(seed_dir / "skills.csv")
        companies_created = self._seed_companies(seed_dir / "companies.csv")
        jobs_created = self._seed_jobs(seed_dir / "jobs.csv")

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {skills_created} skills, "
                f"{companies_created} companies, {jobs_created} jobs created."
            )
        )

    def _seed_skills(self, csv_path: Path) -> int:
        if not csv_path.exists():
            self.stdout.write(self.style.WARNING(f"Missing {csv_path}"))
            return 0

        created_count = 0
        with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or "").strip()
                category = (row.get("category") or "").strip() or None
                if not name:
                    continue
                _, created = Skill.objects.get_or_create(
                    skill_name=name,
                    defaults={"category": category},
                )
                if created:
                    created_count += 1
        return created_count

    def _seed_companies(self, csv_path: Path) -> int:
        if not csv_path.exists():
            self.stdout.write(self.style.WARNING(f"Missing {csv_path}"))
            return 0

        created_count = 0
        with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or "").strip()
                if not name:
                    continue
                _, created = Company.objects.get_or_create(
                    company_name=name,
                    defaults={
                        "website": (row.get("website") or "").strip() or None,
                        "industry": (row.get("industry") or "").strip() or None,
                    },
                )
                if created:
                    created_count += 1
        return created_count

    def _seed_jobs(self, csv_path: Path) -> int:
        if not csv_path.exists():
            self.stdout.write(self.style.WARNING(f"Missing {csv_path}"))
            return 0

        created_count = 0
        with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                company_name = (row.get("company_name") or "").strip()
                title = (row.get("title") or "").strip()
                if not company_name or not title:
                    continue

                company, _ = Company.objects.get_or_create(company_name=company_name)
                _, created = Job.objects.get_or_create(
                    company=company,
                    title=title,
                    defaults={
                        "description": (row.get("description") or "").strip(),
                        "location": (row.get("location") or "").strip() or None,
                        "job_type": (row.get("job_type") or "full-time").strip(),
                        "work_mode": (row.get("work_mode") or "on-site").strip(),
                        "apply_url": (row.get("apply_url") or "").strip() or None,
                    },
                )
                if created:
                    created_count += 1
        return created_count
