function togglePasswordVisibility(toggleId, passwordId, eyeIconId) {
    const togglePassword = document.getElementById(toggleId);
    const passwordField = document.getElementById(passwordId);
    const eyeIcon = document.getElementById(eyeIconId);

    togglePassword.addEventListener('click', function () {
        // Alternar el tipo del campo de contraseña entre 'password' y 'text'
        const type = passwordField.type === 'password' ? 'text' : 'password';
        passwordField.type = type;

        // Cambiar el ícono según el tipo
        if (type === 'password') {
            eyeIcon.classList.remove('fa-eye-slash');
            eyeIcon.classList.add('fa-eye');
        } else {
            eyeIcon.classList.remove('fa-eye');
            eyeIcon.classList.add('fa-eye-slash');
        }
    });
}

// Inicializar la funcionalidad para ambos campos
togglePasswordVisibility('togglePassword1', 'password', 'eye-icon1');
togglePasswordVisibility('togglePassword2', 'password_confirm', 'eye-icon2');
