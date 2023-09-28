function validatePassword() {
    const oldPassword = document.getElementById('old_password').value;
    const newPassword = document.getElementById('new_password').value;
    const errorMessage = document.getElementById('error_message');
    const submitButton = document.getElementById('submit_button');
    const passwordRules = document.getElementById('password_rules');

    // Reset error message and styles
    errorMessage.textContent = '';
    passwordRules.style.color = '';

    // Check if new password meets the rules
    if (newPassword.length < 5 || newPassword.length > 32) {
        errorMessage.textContent = '密码长度必须至少为5位且最多为32位';
        passwordRules.style.color = 'red';
    } else if (newPassword === oldPassword) {
        errorMessage.textContent = '新密码不能与旧密码相同';
        passwordRules.style.color = 'red';
    } else {
        // Additional rules can be added here
    }

    // Enable or disable submit button based on password validity
    submitButton.disabled = errorMessage.textContent !== '';
}