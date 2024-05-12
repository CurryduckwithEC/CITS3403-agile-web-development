document.querySelector('form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form from submitting

  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;

  // Clear existing error messages
  document.getElementById('usernameError').style.display = 'none';
  document.getElementById('passwordError').style.display = 'none';

  // Validation with more specific error messages
  var hasError = false;
  if (username === '') {
      document.getElementById('usernameError').textContent = "Username cannot be empty";
      document.getElementById('usernameError').style.display = 'block';
      hasError = true;
  }
  if (password === '') {
      document.getElementById('passwordError').textContent = "Password cannot be empty";
      document.getElementById('passwordError').style.display = 'block';
      hasError = true;
  }

  // Submit form only if there are no errors
  if (!hasError) {
      console.log("Form data is valid!");
      // Replace with your submission logic (e.g., send data to server)
  }
});
