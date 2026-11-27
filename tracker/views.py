from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application, Reminder, StatusLog
from .serializers import (
    ApplicationSerializer,
    KanbanBoardSerializer,
    ReminderSerializer,
)


# ---------------------------------------------------------------------------
# Web views
# ---------------------------------------------------------------------------


@login_required
def kanban_board_view(request):
    applications = Application.objects.filter(user=request.user).select_related('job__company')
    return render(request, 'tracker/board.html', {'applications': applications})


@login_required
def application_list_view(request):
    applications = Application.objects.filter(user=request.user).select_related('job__company')
    return render(request, 'tracker/board.html', {'applications': applications})


@login_required
def application_create_view(request):
    return render(request, 'tracker/application_detail.html', {})


@login_required
def application_detail_view(request, pk):
    application = get_object_or_404(
        Application.objects.select_related('job__company', 'resume'),
        pk=pk,
        user=request.user,
    )
    return render(request, 'tracker/application_detail.html', {'application': application})


@login_required
def application_edit_view(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'tracker/application_detail.html', {'application': application})


@login_required
def application_delete_view(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        application.delete()
        return redirect('tracker:kanban-board')
    return render(request, 'tracker/application_detail.html', {'application': application})


@login_required
def reminder_list_view(request):
    reminders = Reminder.objects.filter(application__user=request.user).select_related('application')
    return render(request, 'tracker/board.html', {'reminders': reminders})


# ---------------------------------------------------------------------------
# API views
# ---------------------------------------------------------------------------


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects.filter(user=self.request.user)
            .select_related('job__company', 'resume')
            .prefetch_related('status_logs', 'reminders')
        )

    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)
        StatusLog.objects.create(
            application=application,
            old_status=None,
            new_status=application.status,
        )


class ApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects.filter(user=self.request.user)
            .select_related('job__company', 'resume')
            .prefetch_related('status_logs', 'reminders')
        )


class ApplicationStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        application = get_object_or_404(Application, pk=pk, user=request.user)
        new_status = request.data.get('status')
        valid_statuses = {choice[0] for choice in Application.STATUS_CHOICES}
        if new_status not in valid_statuses:
            return Response(
                {'detail': 'Invalid status value.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        old_status = application.status
        if old_status != new_status:
            application.status = new_status
            application.save(update_fields=['status'])
            StatusLog.objects.create(
                application=application,
                old_status=old_status,
                new_status=new_status,
            )
        return Response(ApplicationSerializer(application).data, status=status.HTTP_200_OK)


class KanbanBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = (
            Application.objects.filter(user=request.user)
            .select_related('job__company', 'resume')
            .prefetch_related('status_logs', 'reminders')
        )
        board = {choice[0]: [] for choice in Application.STATUS_CHOICES}
        for app in applications:
            if app.status in board:
                board[app.status].append(app)
        serializer = KanbanBoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReminderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(application__user=self.request.user)


class ReminderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(application__user=self.request.user)
