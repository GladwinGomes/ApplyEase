from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def mock_form_a_view(request):
    return render(request, 'mock_forms/form1.html')


@login_required
def mock_form_b_view(request):
    return render(request, 'mock_forms/form2.html')


@login_required
def mock_form_c_view(request):
    return render(request, 'mock_forms/form3.html')
