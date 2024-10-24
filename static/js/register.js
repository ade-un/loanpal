// register.js

document.addEventListener("DOMContentLoaded", function () {
    const registrationForm = document.querySelector("form");  // Select the registration form

    registrationForm.addEventListener("submit", function (event) {
        // Prevent default form submission to handle validation
        event.preventDefault();

        // Get the values from the form
        const username = document.getElementById("id_username").value;  // Get username
        const email = document.getElementById("id_email").value;      // Get email
        const password1 = document.getElementById("id_password1").value;  // Get password
        const password2 = document.getElementById("id_password2").value;  // Confirm password

        // Basic validation
        if (username === "" || email === "" || password1 === "" || password2 === "") {
            alert("All fields are required!");
            return;
        }

        if (password1 !== password2) {
            alert("Passwords do not match!");
            return;
        }

        // If validation passes, submit the form
        registrationForm.submit();
    });
});
