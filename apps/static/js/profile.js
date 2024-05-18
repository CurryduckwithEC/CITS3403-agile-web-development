$(document).ready(function() {
    $('#username').on('input', function() {
        var username = $(this).val();
        $.post('/check_username', { username: username }, function(data) {
            if (data.exists) {
                $('#usernameCheck').text('Username is already taken.');
            } else {
                $('#usernameCheck').text('');
            }
        });
    });

    $('#email').on('input', function() {
        var email = $(this).val();
        $.post('/check_email', { email: email }, function(data) {
            if (data.exists) {
                $('#emailCheck').text('Email is already taken.');
            } else {
                $('#emailCheck').text('');
            }
        });
    });

    $('#confirm_password').on('input', function() {
        var password = $('#password').val();
        var confirm_password = $(this).val();
        if (password !== confirm_password) {
            $('#passwordCheck').text('Passwords do not match.');
        } else {
            $('#passwordCheck').text('');
        }
    });
});