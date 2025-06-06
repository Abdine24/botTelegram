from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import datetime
import requests
import os

# Configuration du bot
TOKEN = '7174970942:AAERseUdYk9WBoztRjQbaOgIrCeRypldmfo'

# Fonction pour obtenir l'emplacement à partir de l'IP
def get_location_from_ip(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
    except:
        return "Location unknown"

# Fonction pour sauvegarder les données dans le fichier JSON
def save_user_data(user_data):
    try:
        with open('user_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    data.append(user_data)
    
    with open('user_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Gestionnaire de commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ouvrir l'application", web_app=WebAppInfo(url="https://votre-username.github.io/votre-repo"))]
    ]
    await update.message.reply_text(
        "Bienvenue! Cliquez sur le bouton ci-dessous pour ouvrir l'application.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Gestionnaire des données du web app
async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    
    # Validation de l'email
    if not '@' in data['email'] or not '.' in data['email']:
        await update.message.reply_text("L'adresse email n'est pas valide.")
        return
    
    # Validation du mot de passe (au moins 8 caractères, une majuscule, un chiffre)
    if len(data['password']) < 8 or not any(c.isupper() for c in data['password']) or not any(c.isdigit() for c in data['password']):
        await update.message.reply_text("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
        return
    
    # Création des données utilisateur
    user_data = {
        'telegram_username': update.effective_user.username,
        'email': data['email'],
        'password': data['password'],  # Dans un cas réel, il faudrait hasher le mot de passe
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'location': get_location_from_ip(update.effective_message.from_user.id)
    }
    
    # Sauvegarde des données
    save_user_data(user_data)
    
    await update.message.reply_text("Informations enregistrées avec succès!")

def main():
    # Création de l'application
    application = Application.builder().token(TOKEN).build()
    
    # Ajout des gestionnaires
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data))
    
    # Démarrage du bot
    application.run_polling()

if __name__ == '__main__':
    main()
