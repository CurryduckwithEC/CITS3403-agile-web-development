document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting

        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;

        // Clear existing error messages
        var emailError = document.getElementById('emailError');
        var passwordError = document.getElementById('passwordError');

        if (emailError) {
            emailError.style.display = 'none';
        }
        if (passwordError) {
            passwordError.style.display = 'none';
        }

        // Validation with more specific error messages
        var hasError = false;
        if (email === '') {
            if (emailError) {
                emailError.textContent = "Email cannot be empty";
                emailError.style.display = 'block';
            }
            hasError = true;
        }
        if (password === '') {
            if (passwordError) {
                passwordError.textContent = "Password cannot be empty";
                passwordError.style.display = 'block';
            }
            hasError = true;
        }

        // Submit form only if there are no errors
        if (!hasError) {
            console.log("Form data is valid!");
            form.submit(); // Submit the form
        }
    });

    // Flash messages handling
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message) {
        // Show the message
        message.classList.add('show');

        // Set timeout to fade out the message
        setTimeout(function() {
            message.classList.remove('show');
            message.classList.add('fade');
            setTimeout(function() {
                message.style.display = 'none';
            }, 500);
        }, 5000); // Display for 5 seconds
    });
});