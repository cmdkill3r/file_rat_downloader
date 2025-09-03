📂 File Manager Bot

Warning: This bot is designed for educational and pentesting purposes only. Never run on machines you do not own. Contact the author to test the full tool in controlled environments.

🚀 Features

Navigate and manage files in a terminal-style interface.

Upload and send files.

Copy, move, rename, and delete files.

Execute files (simulated safely).

Read file contents with cat, head, and tail.

Retrieve last 12h Chrome history across profiles.

Fully interactive command loop, mimicking a real remote file manager.

🛠 Commands
Command	Description
pwd	Show current directory
ls	List files and folders
cd <dir>	Change directory
upload <file>	Upload file
send <file>	Alias for upload
cp <src> <dst>	Copy file
mv <src> <dst>	Move or rename file
rm <file>	Delete file
mkdir <folder>	Create new folder
run <file> / exec <file>	Execute file (simulated)
cat <file>	Show first 4k characters
head <file> [n]	Show first n lines
tail <file> [n]	Show last n lines
history chrome	Show last 12h Chrome history
exit	Shut down bot
⚡ Installation
git clone https://github.com/YOUR_USERNAME/file-manager-bot.git
cd file-manager-bot
python bot.py


Requires Python 3.8+

No external dependencies needed for safe mode

🎯 Usage

Launch the bot:

python bot.py


Type commands exactly like the table above.

File uploads/downloads happen in the local downloads folder—fully sandboxed.

Chrome history displays realistic-looking entries for demonstration.

💡 Notes

This repo is completely safe—no real data is affected.

To test the full live functionality in a controlled lab environment, reach out directly:

📬 Contact: GitHub DM

The bot behaves exactly like a real remote file manager, perfect for pentesting demos and training.

🤝 Contributing

Pull requests for new safe commands or enhancements are welcome.

Do not include malicious code—repo is for educational purposes.

🔥 Showcase

Example commands, screenshots, and outputs included for clarity.

Fully realistic terminal interface to give the feel of an actual remote access tool.
