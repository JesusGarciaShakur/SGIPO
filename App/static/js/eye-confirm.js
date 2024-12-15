document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('password_confirm');
    const passwordFeedback = document.createElement('small');
    const confirmFeedback = document.createElement('small');
    passwordFeedback.className = 'text-danger';
    confirmFeedback.className = 'text-danger';

    // Inserta el mensaje de validación para la contraseña
    passwordInput.parentNode.appendChild(passwordFeedback);

    // Inserta el mensaje de validación para confirmar la contraseña
    confirmPasswordInput.parentNode.appendChild(confirmFeedback);

    // Validación de contraseña
    passwordInput.addEventListener('input', () => {
        const value = passwordInput.value;
        if (!value) {
            passwordFeedback.textContent = '';
        } else if (value.length < 8) {
            passwordFeedback.textContent = 'La contraseña debe tener al menos 8 caracteres.';
        } else if (!/[A-Za-z]/.test(value)) {
            passwordFeedback.textContent = 'La contraseña debe incluir al menos una letra.';
        } else if (!/\d/.test(value)) {
            passwordFeedback.textContent = 'La contraseña debe incluir al menos un número.';
        } else {
            passwordFeedback.textContent = '';
        }
    });

    // Validación de confirmación de contraseña
    confirmPasswordInput.addEventListener('input', () => {
        if (confirmPasswordInput.value !== passwordInput.value) {
            confirmFeedback.textContent = 'Las contraseñas no coinciden.';
        } else {
            confirmFeedback.textContent = '';
        }
    });
});