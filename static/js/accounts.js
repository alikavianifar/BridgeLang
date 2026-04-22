function togglePasswordVisibilitySignup() {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const passwordFieldType = passwordField.getAttribute('type');
    const toggleIcon = document.querySelector('.toggle-password');

    if (passwordFieldType === 'password') {
        passwordField.setAttribute('type', 'text');
        confirmPasswordField.setAttribute('type', 'text');
        toggleIcon.classList.remove('bi-eye-fill');
        toggleIcon.classList.add('bi-eye-slash-fill');
    } else {
        passwordField.setAttribute('type', 'password');
        confirmPasswordField.setAttribute('type', 'password');
        toggleIcon.classList.remove('bi-eye-slash-fill');
        toggleIcon.classList.add('bi-eye-fill');
    }
}

function togglePasswordVisibilityLogin(id = 'password') {
    const passwordField = document.getElementById(id);
    const passwordFieldType = passwordField.getAttribute('type');
    const toggleIcon = passwordField.nextElementSibling;

    if (passwordFieldType === 'password') {
        passwordField.setAttribute('type', 'text');
        toggleIcon.classList.remove('bi-eye-fill');
        toggleIcon.classList.add('bi-eye-slash-fill');
    } else {
        passwordField.setAttribute('type', 'password');
        toggleIcon.classList.remove('bi-eye-slash-fill');
        toggleIcon.classList.add('bi-eye-fill');
    }
}

document.getElementById('password').addEventListener('focus', function() {
    document.querySelector('.password-requirements-list').style.display = 'block';
});

document.getElementById('password').addEventListener('input', function() {
    const username = document.getElementById('username').value.toLowerCase();
    const password = this.value;

    if (username && password.toLowerCase().includes(username)) {
        document.querySelector('.requirement-non-repetitive').classList.add('invalid');
        document.querySelector('.requirement-non-repetitive').classList.remove('valid');
    } else {
        document.querySelector('.requirement-non-repetitive').classList.add('valid');
        document.querySelector('.requirement-non-repetitive').classList.remove('invalid');
    }

    if (password.length >= 8) {
        document.querySelector('.requirement-length').classList.add('valid');
        document.querySelector('.requirement-length').classList.remove('invalid');
    } else {
        document.querySelector('.requirement-length').classList.add('invalid');
        document.querySelector('.requirement-length').classList.remove('valid');
    }

    if (/[A-Z]/.test(password)) {
        document.querySelector('.requirement-uppercase').classList.add('valid');
        document.querySelector('.requirement-uppercase').classList.remove('invalid');
    } else {
        document.querySelector('.requirement-uppercase').classList.add('invalid');
        document.querySelector('.requirement-uppercase').classList.remove('valid');
    }

    if (/[a-z]/.test(password)) {
        document.querySelector('.requirement-lowercase').classList.add('valid');
        document.querySelector('.requirement-lowercase').classList.remove('invalid');
    } else {
        document.querySelector('.requirement-lowercase').classList.add('invalid');
        document.querySelector('.requirement-lowercase').classList.remove('valid');
    }

    if (/\d/.test(password)) {
        document.querySelector('.requirement-number').classList.add('valid');
        document.querySelector('.requirement-number').classList.remove('invalid');
    } else {
        document.querySelector('.requirement-number').classList.add('invalid');
        document.querySelector('.requirement-number').classList.remove('valid');
    }

    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {  // بررسی وجود کاراکتر خاص
        document.querySelector('.requirement-special').classList.add('valid');
        document.querySelector('.requirement-special').classList.remove('invalid');
    } else {
        document.querySelector('.requirement-special').classList.add('invalid');
        document.querySelector('.requirement-special').classList.remove('valid');
    }
});

let hideTimeout;

function checkPasswordRequirements() {
    const password = document.getElementById('password').value;
    const username = document.getElementById('username').value.toLowerCase();

    const lengthValid = password.length >= 8;
    const uppercaseValid = /[A-Z]/.test(password);
    const lowercaseValid = /[a-z]/.test(password);
    const numberValid = /\d/.test(password);
    const specialValid = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const nonRepetitiveValid = !password.toLowerCase().includes(username);

    const requirementList = document.querySelector('.password-requirements-list');

    if (lengthValid && uppercaseValid && lowercaseValid && numberValid && specialValid && nonRepetitiveValid) {
        if (hideTimeout) clearTimeout(hideTimeout);
        hideTimeout = setTimeout(() => {
            requirementList.classList.remove('show');
        }, 1000);
    } else {
        requirementList.classList.add('show');
        if (hideTimeout) clearTimeout(hideTimeout);
    }
}

document.getElementById('password').addEventListener('input', function() {
    const requirementList = document.querySelector('.password-requirements-list');
    requirementList.classList.add('show');
    
    checkPasswordRequirements();
});

document.getElementById('password').addEventListener('focus', function() {
    const requirementList = document.querySelector('.password-requirements-list');
    requirementList.classList.add('show');
});

/**
 * Messeges alert timer
 */
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach((alert, index) => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            // Remove the element from the DOM after the transition ends
            alert.addEventListener('transitionend', () => {
                alert.remove();
            });
        }, 1000 * index); // Adjust the timing as needed
    });
});
