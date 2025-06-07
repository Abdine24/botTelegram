from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import datetime
import os
import logging

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration du bot
TOKEN = '7174970942:AAERseUdYk9WBoztRjQbaOgIrCeRypldmfo'

# Fonction pour sauvegarder les données dans le fichier JSON
def save_user_data(user_data):
    try:
        # Chemin du fichier JSON
        json_file = 'users.json'
        
        # Créer le fichier s'il n'existe pas
        if not os.path.exists(json_file):
            logger.info(f"Création du fichier {json_file}")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Lire les données existantes
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Le fichier JSON était vide ou corrompu, création d'une nouvelle liste")
            data = []
        
        # Ajouter les nouvelles données
        data.append(user_data)
        
        # Sauvegarder les données
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        logger.info(f"Données sauvegardées avec succès: {user_data}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde: {e}")
        return False

# Gestionnaire de commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ouvrir l'application", web_app=WebAppInfo(url="https://abdine24.github.io/botTelegram/"))]
    ]
    await update.message.reply_text(
        "Bienvenue! Cliquez sur le bouton ci-dessous pour ouvrir l'application.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Gestionnaire des données du web app
async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Récupérer et parser les données JSON
        data = json.loads(update.effective_message.web_app_data.data)
        logger.info(f"Données reçues du web app: {data}")
        
        # Extraire les informations
        email = data.get('email', '')
        password = data.get('password', '')
        username = update.effective_user.username or "Unknown"
        
        logger.info(f"Email: {email}")
        logger.info(f"Password: {password}")
        logger.info(f"Username: {username}")
        
        # Validation de l'email
        if not '@' in email or not '.' in email:
            await update.message.reply_text("L'adresse email n'est pas valide.")
            return
        
        # Validation du mot de passe
        if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            await update.message.reply_text("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
            return
        
        # Création des données utilisateur
        user_data = {
            'telegram_username': username,
            'email': email,
            'password': password,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Sauvegarde des données
        if save_user_data(user_data):
            await update.message.reply_text("Informations enregistrées avec succès!")
        else:
            await update.message.reply_text("Une erreur est survenue lors de l'enregistrement des informations.")
            
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage JSON: {e}")
        await update.message.reply_text("Format de données invalide.")
    except Exception as e:
        logger.error(f"Erreur: {e}")
        await update.message.reply_text("Une erreur est survenue lors du traitement des données.")

def main():
    # Création de l'application
    application = Application.builder().token(TOKEN).build()
    
    # Ajout des gestionnaires
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data))
    
    # Démarrage du bot
    logger.info("Bot démarré")
    application.run_polling()

if __name__ == '__main__':
    main()
