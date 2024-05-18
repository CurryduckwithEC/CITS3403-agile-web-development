console.log('profile.js loaded');

document.addEventListener('DOMContentLoaded', function () {
    // Get CSRF token from hidden field
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    console.log('CSRF Token:', csrfToken);

    // Check username uniqueness
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.addEventListener('input', function () {
            var username = this.value;
            console.log('Checking username:', username);
            console.log('Request URL:', '/check_username');
            console.log('Request Data:', JSON.stringify({ username: username }));
            fetch('/check_username', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({username: username})
            })
                .then(response => response.json())
                .then(data => {
                    var usernameCheck = document.getElementById('usernameCheck');
                    if (data.exists) {
                        usernameCheck.textContent = 'Username is already taken.';
                    } else {
                        usernameCheck.textContent = '';
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    // Check email uniqueness
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('input', function () {
            var email = this.value;
            fetch('/check_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({email: email})
            })
                .then(response => response.json())
                .then(data => {
                    var emailCheck = document.getElementById('emailCheck');
                    if (data.exists) {
                        emailCheck.textContent = 'Email is already taken.';
                    } else {
                        emailCheck.textContent = '';
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    // Check if passwords match
    const confirmPasswordInput = document.getElementById('confirm_password');
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function () {
            var password = document.getElementById('password').value;
            var confirmPassword = this.value;
            var passwordCheck = document.getElementById('passwordCheck');
            if (password !== confirmPassword) {
                passwordCheck.textContent = 'Passwords do not match.';
            } else {
                passwordCheck.textContent = '';
            }
        });
    }

    const form = document.getElementById('edit-profile-form');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            // Create FormData object to store form data
            const formData = new FormData(form);

            // Perform AJAX request to submit the form data
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Profile updated successfully
                        window.location.href = data.redirect_url;
                    } else {
                        // Handle error case
                        console.error('Error updating profile:', data.error);
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }
});