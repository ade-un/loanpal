from django.contrib import admin
from .models import CustomUser, Application

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

# Admin view for Applications
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'purpose', 'status', 'submission_date', 'review_date')
    list_filter = ('status', 'submission_date', 'amount')
    search_fields = ('user__username', 'purpose', 'status')
    ordering = ('-submission_date',)  # Order applications by submission date, most recent first

    # Custom action to approve selected applications
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')  # Change status for selected applications
    approve_applications.short_description = "Approve selected applications"

    # Custom action to reject selected applications
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')  # Change status for selected applications
    reject_applications.short_description = "Reject selected applications"

    actions = [approve_applications, reject_applications]  # Add custom actions to admin

    # Read-only fields
    readonly_fields = ('submission_date', 'review_date', 'employer_name', 'job_title', 'monthly_income', 'amount', 'duration', 'purpose')  # Add any other fields you want to make read-only

    # Organizing fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('user', 'amount', 'purpose', 'status')  # Fields admins can change
        }),
        ('Application Details', {
            'fields': ('employer_name', 'job_title', 'monthly_income', 'duration'),  # Read-only fields displayed in details
        }),
        ('Dates', {
            'fields': ('submission_date', 'review_date')
        }),
    )

# If you want to use inlines for application details, uncomment the below lines and define the ApplicationDetail model
# class ApplicationDetailInline(admin.TabularInline):
#     model = ApplicationDetail  # Assuming there's a model for application details
#     extra = 1  # How many empty forms to display for new entries
#     fields = ('field1', 'field2')  # Specify fields to display in inline
#     readonly_fields = ('field1',)  # Make any fields read-only
#     can_delete = False  # Prevent deletion of inline entries

#     # Uncomment the below line if ApplicationDetail is defined
#     # inlines = [ApplicationDetailInline]  

