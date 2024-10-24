from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model to include user roles
class CustomUser(AbstractUser):
    email = models.EmailField()  # Removed unique constraint on email
    role = models.CharField(
        max_length=20,
        choices=(('normal', 'Normal User'), ('admin', 'Admin')),
        default='normal'
    )

    # Define custom related names for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Ensure this is unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Ensure this is unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username  # Display the username when printing the user

# Loan application model
class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=100, default="")
    job_title = models.CharField(max_length=100, default="")
    monthly_income = models.IntegerField(null=True)
    amount = models.FloatField()
    duration = models.IntegerField(null=True)  # Duration field (in months or any relevant unit)
    purpose = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')),
        default='pending'
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(null=True, blank=True)
    can_reapply = models.BooleanField(default=True)  # Field to track reapplication status

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
