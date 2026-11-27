from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

User = get_user_model()


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/admin_dashboard.html')


@login_required
def user_management_view(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_management.html', {'users': users})


@login_required
def analytics_view(request):
    return render(request, 'dashboard/admin_dashboard.html')
