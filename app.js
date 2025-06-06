// Initialisation de l'application Telegram WebApp
const tg = window.Telegram.WebApp;

// Fonction pour valider l'email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Fonction pour valider le mot de passe
function validatePassword(password) {
    return password.length >= 8 && 
           /[A-Z]/.test(password) && 
           /[0-9]/.test(password);
}

// Fonction pour réinitialiser le formulaire
function resetForm() {
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
    document.getElementById('emailError').textContent = '';
    document.getElementById('passwordError').textContent = '';
}

// Gestionnaire de soumission du formulaire
document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    let isValid = true;
    
    // Réinitialiser les messages d'erreur
    document.getElementById('emailError').textContent = '';
    document.getElementById('passwordError').textContent = '';
    
    // Validation de l'email
    if (!validateEmail(email)) {
        document.getElementById('emailError').textContent = 'Veuillez entrer une adresse email valide';
        isValid = false;
    }
    
    // Validation du mot de passe
    if (!validatePassword(password)) {
        document.getElementById('passwordError').textContent = 'Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre';
        isValid = false;
    }
    
    if (isValid) {
        try {
            // Vérifier si Telegram WebApp est disponible
            if (window.Telegram && window.Telegram.WebApp) {
                // Préparer les données
                const data = {
                    email: email,
                    password: password
                };
                
                // Envoyer les données au bot
                window.Telegram.WebApp.sendData(JSON.stringify(data));
                
                // Réinitialiser le formulaire
                resetForm();
                
                // Afficher un message de succès
                alert('Inscription réussie!');
            } else {
                console.error('Telegram WebApp n\'est pas disponible');
                alert('Erreur: Telegram WebApp n\'est pas disponible');
            }
        } catch (error) {
            console.error('Erreur lors de l\'envoi des données:', error);
            alert('Une erreur est survenue lors de l\'envoi des données');
        }
    }
});

// Gestionnaire du bouton de fermeture
document.getElementById('closeButton').addEventListener('click', function() {
    tg.close();
}); 