document.addEventListener('DOMContentLoaded', () => {
    const loanForm = document.getElementById('loanForm');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token

    loanForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(loanForm);
        const response = await fetch(loanForm.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken // Include CSRF token in headers
            },
            body: formData,
        });

        const responseData = await response.json();

        const successMessage = document.getElementById('successMessage');
        const errorMessage = document.getElementById('errorMessage');
        const messageContainer = document.getElementById('messageContainer');

        messageContainer.style.display = 'block'; // Show messages section

        if (response.ok) {
            successMessage.textContent = responseData.message; // Display success message
            successMessage.style.display = 'block';
            errorMessage.style.display = 'none';
            loanForm.reset(); // Clear the form after submission
            setTimeout(() => {
                window.location.href = responseData.redirect_url; // Redirect after success
            }, 2000); // Redirect after 2 seconds
        } else {
            errorMessage.textContent = responseData.error || 'An error occurred. Please try again.'; // Display error message
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        }
    });
});
