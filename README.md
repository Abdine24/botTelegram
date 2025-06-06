# Telegram Button Creator Bot

A Telegram bot that allows users to create posts with custom buttons and links.

## Features

- Create posts with text, photos, or audio
- Add custom buttons with links
- Edit existing posts
- Preview posts before publishing
- Multi-language support
- Database storage for posts and links

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python app.py
   ```

## Usage

1. Start the bot by sending `/start`
2. Use the main menu to:
   - Create a new post
   - Edit an existing post
   - View how to use the bot
   - Change language settings

## Database Structure

The bot uses SQLite with three main tables:
- `users`: Stores user information
- `links`: Stores button links created by users
- `posts`: Stores post content and metadata

## File Types Support

The bot supports the following file types:
- Text: .txt
- Photos: .jpg, .jpeg, .png
- Audio: .mp3, .wav
- Video: .mp4 