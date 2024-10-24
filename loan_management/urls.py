from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('login/', views.user_login, name='login'),  # User login
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout
    path('register/', views.register, name='register'),  # User registration

    # Home and application routes
    path('', views.home, name='home'),  # Home page
    path('apply-for-loan/', views.apply_for_loan, name='apply_for_loan'),  # Loan application page

    # Loan status route for users to check their application status
    path('status/', views.loan_status, name='loan_status'),  # Loan status page

    # Admin route to change loan status (restricted to staff users)
    path('change-status/<int:application_id>/<str:new_status>/', 
         views.change_loan_status, name='change_loan_status'),  # Change loan status

    # New route for nonexistent URL
    path('nonexistent-url/', views.nonexistent_view, name='nonexistent_view'),  # New URL pattern
]
