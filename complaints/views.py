from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .forms import RegistrationForm, EmailLoginForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ComplaintForm
from .models import Complaint


def home(request):
    recent = Complaint.objects.all()[:6]
    return render(request, 'complaints/home.html', {'recent': recent})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'complaints/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User = get_user_model()
            try:
                user_obj = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email')
                return render(request, 'complaints/login.html', {'form': form})

            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('password', 'Invalid password')
    else:
        form = EmailLoginForm()
    return render(request, 'complaints/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/submit_complaint.html', {'form': form})


@login_required
def complaint_list(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    if request.user.is_superuser:
        qs = Complaint.objects.all()
    else:
        qs = Complaint.objects.filter(user=request.user)

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if status:
        qs = qs.filter(status=status)

    categories = [c[0] for c in Complaint.CATEGORY_CHOICES]
    statuses = [s[0] for s in Complaint.STATUS_CHOICES]

    return render(request, 'complaints/complaint_list.html', {
        'complaints': qs,
        'q': q,
        'category': category,
        'status': status,
        'categories': categories,
        'statuses': statuses,
    })


@login_required
def profile(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaints/profile.html', {'complaints': complaints})


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # allow superuser to see all, others only their own
    if not request.user.is_superuser and complaint.user != request.user:
        return redirect('complaint_list')
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})
