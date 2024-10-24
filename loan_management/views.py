from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, JsonResponse
from .models import Application, CustomUser  # Ensure this matches your model names
from .forms import ApplicationForm, CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse
from django.contrib import messages

# Home view (only accessible after login)
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  # Redirect to login if unauthenticated

    # Check if the user has already applied for a loan
    loan = Application.objects.filter(user=request.user).first()
    
    # Render the home page with loan data if available
    return render(request, 'home.html', {'loan': loan})

# User registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically
            return HttpResponseRedirect(reverse('home'))  # Redirect to home on success
        else:
            return render(request, 'registration/register.html', {
                'form': form,
                'error': 'Registration failed. Please correct the errors below.'
            })
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home
            return render(request, 'registration/login.html', {
                'form': form,
                'error': 'Invalid username or password'
            })
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Loan application view (only for authenticated users)
def apply_for_loan(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  # Redirect to login if unauthenticated

    # Check for existing application
    existing_application = Application.objects.filter(user=request.user).first()

    if existing_application:
        if existing_application.status == 'rejected':
            messages.info(request, 'You can reapply for a loan now.')
        else:
            messages.info(request, 'You have already applied. Check your loan status.')
            return redirect('loan_status')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Create or update the application based on the status
            if existing_application and existing_application.status == 'rejected':
                existing_application.amount = form.cleaned_data['amount']
                existing_application.duration = form.cleaned_data['duration']
                existing_application.purpose = form.cleaned_data['purpose']
                existing_application.status = 'pending'
                existing_application.save()
                message = 'Your reapplication has been submitted successfully.'
            else:
                application = form.save(commit=False)
                application.user = request.user
                application.status = 'pending'
                application.save()
                message = 'Your loan application has been submitted successfully.'

            # Send success message and return JSON response
            return JsonResponse({'message': message, 'redirect_url': reverse('loan_status')})

        # Handle form errors
        return JsonResponse({'error': 'Invalid data. Please try again.'}, status=400)

    # Display loan form
    form = ApplicationForm()
    return render(request, 'loan_application/apply_for_loan.html', {'form': form})

# Loan status view
def loan_status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  # Redirect to login if unauthenticated

    # Retrieve loan application for the user
    loan = Application.objects.filter(user=request.user).first()

    if loan:
        status_message = ''
        if loan.status == 'approved':
            status_message = 'Your application has been approved!'
        elif loan.status == 'rejected':
            status_message = 'Your application was rejected. You can <a href="' + reverse('apply_for_loan') + '">reapply</a>.'
        else:
            status_message = 'Your application is still pending.'

        return render(request, 'loan_application/status.html', {'loan': loan, 'status_message': status_message})
    
    return render(request, 'loan_application/status.html', {'loan': None, 'status_message': 'No loan application found.'})

# Admin-only view to change loan status
def change_loan_status(request, application_id, new_status):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect('login')  # Restrict access to admins

    try:
        application = Application.objects.get(id=application_id)
        application.status = new_status
        if new_status == 'rejected':
            application.can_reapply = True  # Allow reapplication on rejection
        application.save()
        messages.success(request, f'The loan status has been updated to {new_status}.')
        return redirect('home')
    except Application.DoesNotExist:
        raise Http404("Application not found")

# Nonexistent view for demonstration
def nonexistent_view(request):
    return render(request, 'nonexistent_template.html')
