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
}

// Gestionnaire de soumission du formulaire
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Validation des champs
    if (!validateEmail(email)) {
        alert('Veuillez entrer une adresse email valide.');
        return;
    }
    
    if (!validatePassword(password)) {
        alert('Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.');
        return;
    }
    
    // Préparation des données
    const formData = {
        email: email,
        password: password
    };

    // Envoi des données au bot Telegram
    tg.sendData(JSON.stringify(formData));
    
    // Réinitialiser le formulaire
    resetForm();
    
    // Afficher un message de confirmation
    alert('Données envoyées avec succès!');
});

// Gestionnaire du bouton de fermeture
document.getElementById('closeButton').addEventListener('click', function() {
    tg.close();
}); 