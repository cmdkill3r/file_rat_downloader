import os
import shutil
import time
import difflib
from datetime import datetime, timedelta

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# ===== WORKING DIRECTORY =====
ROOT_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(ROOT_DIR, exist_ok=True)

# Prepopulate folders and files
for folder in ["Documents", "Pictures", "Projects"]:
    os.makedirs(os.path.join(ROOT_DIR, folder), exist_ok=True)
for file in ["example.txt", "report.pdf", "notes.docx"]:
    open(os.path.join(ROOT_DIR, file), "w").write(f"Content of {file}")

cwd = ROOT_DIR

# ===== MESSAGING =====
def send_message(text):
    print(f"[MESSAGE] {text}")

def send_file(file_path):
    if os.path.exists(file_path):
        send_message(f"✅ Uploaded: {os.path.basename(file_path)}")
    else:
        send_message(f"❌ File not found: {file_path}")

def download_file(file_id, save_dir=cwd):
    filename = os.path.join(save_dir, f"file_{file_id}.txt")
    with open(filename, "w") as f:
        f.write(f"Downloaded file {file_id}")
    send_message(f"✅ Downloaded: {os.path.basename(filename)} → {save_dir}")

# ===== UTILITIES =====
def match_name(partial, directory, want_dir=False):
    try:
        candidates = os.listdir(directory)
        if want_dir:
            candidates = [c for c in candidates if os.path.isdir(os.path.join(directory, c))]
        else:
            candidates = [c for c in candidates if os.path.exists(os.path.join(directory, c))]
    except Exception:
        return None, []

    for c in candidates:
        if c.lower() == partial.lower():
            return c, []

    matches = [c for c in candidates if c.lower().startswith(partial.lower())]
    if len(matches) == 1:
        return matches[0], []
    elif len(matches) > 1:
        return None, matches

    close = difflib.get_close_matches(partial, candidates, n=1, cutoff=0.3)
    if close:
        return close[0], []

    return None, []

# ===== CHROME HISTORY =====
CHROME_HISTORY = [
    "2025-09-03 14:00:00 - Google - https://www.google.com/",
    "2025-09-03 15:30:12 - GitHub - https://github.com/",
    "2025-09-03 16:20:45 - StackOverflow - https://stackoverflow.com/",
]

def get_chrome_history(hours=12):
    send_message("🖥 Chrome History for last 12h:\n" + "\n".join(CHROME_HISTORY))

# ===== COMMAND HANDLER =====
def handle_command(cmd):
    global cwd
    parts = cmd.split(" ", 2)
    base = parts[0].lower()

    if base == "pwd":
        send_message(f"📂 {cwd}")

    elif base == "ls":
        try:
            entries = os.listdir(cwd)
            entries.sort()
            send_message("\n".join(entries) if entries else "📂 (Empty folder)")
        except Exception as e:
            send_message(f"❌ {e}")

    elif base == "cd":
        if len(parts) >= 2:
            target_input = parts[1]
            if target_input == "..":
                cwd = os.path.abspath(os.path.join(cwd, ".."))
                send_message(f"📂 Moved to parent: {cwd}")
                return
            target, options = match_name(target_input, cwd, want_dir=True)
            if target:
                cwd = os.path.abspath(os.path.join(cwd, target))
                send_message(f"📂 Moved to: {cwd}")
            elif options:
                send_message(f"❓ Multiple matches: {', '.join(options)}")
            else:
                send_message("❌ No matching folder")
        else:
            send_message("❌ Usage: cd <folder>")

    elif base in ["upload", "send", "rm", "cp", "mv", "run", "exec", "cat", "head", "tail", "history"]:
        if base == "history":
            if len(parts) >= 2 and parts[1].lower() == "chrome":
                get_chrome_history(12)
            else:
                send_message("❌ Usage: history chrome")
            return

        if len(parts) >= 2:
            target, options = match_name(parts[1], cwd, want_dir=False)
            if not target and options:
                send_message(f"❓ Multiple matches: {', '.join(options)}")
                return
            if not target:
                send_message("❌ No matching file")
                return
            full_target = os.path.join(cwd, target)

            if base in ["upload", "send"]:
                send_file(full_target)
            elif base == "rm":
                send_message(f"🗑 Deleted: {target}")
            elif base == "cp" and len(parts) == 3:
                dest = os.path.join(cwd, parts[2])
                send_message(f"✅ Copied {target} → {dest}")
            elif base == "mv" and len(parts) == 3:
                dest = os.path.join(cwd, parts[2])
                send_message(f"✅ Moved {target} → {dest}")
            elif base in ["run", "exec"]:
                send_message(f"✅ Executed: {target}")
            elif base == "cat":
                with open(full_target, "r") as f:
                    content = f.read(4000)
                    send_message(f"📄 {target}:\n{content}" + ("\n… (truncated)" if f.read(1) else ""))
            elif base in ["head", "tail"]:
                n = int(parts[2]) if len(parts) == 3 and parts[2].isdigit() else 10
                with open(full_target, "r") as f:
                    lines = f.readlines()
                    if base == "head":
                        send_message(f"📄 Head {n} lines of {target}:\n{''.join(lines[:n])}")
                    else:
                        send_message(f"📄 Tail {n} lines of {target}:\n{''.join(lines[-n:])}")
        else:
            send_message(f"❌ Usage: {base} <file> [dest]")

    elif base == "mkdir":
        if len(parts) == 2:
            os.makedirs(os.path.join(cwd, parts[1]), exist_ok=True)
            send_message(f"📂 Created folder: {parts[1]}")
        else:
            send_message("❌ Usage: mkdir <folder>")

    elif base == "help":
        send_message("""
📂 FILE MANAGER BOT 📂

pwd                 → Show current directory
ls                  → List files/folders
cd <dir>            → Change directory
upload <file>       → Upload file
send <file>         → Alias of upload
cp <src> <dst>      → Copy file
mv <src> <dst>      → Move/Rename file
rm <file>           → Delete file
mkdir <folder>      → Create folder
run/exec <file>     → Execute file
cat <file>          → Read first 4k chars
head <file> [n]     → Show first n lines
tail <file> [n]     → Show last n lines
history chrome      → Get last 12h Chrome history
exit                → Shut down bot
""")

# ===== MAIN LOOP =====
def bot_loop():
    send_message("🤖 File Manager Bot Online. Type 'help' for commands.")
    while True:
        cmd = input(">> ").strip()
        if cmd.lower() == "exit":
            send_message("🛑 Shutting down.")
            break
        else:
            handle_command(cmd)

# ===== ENTRY POINT =====
if __name__ == "__main__":
    print("Starting Bot… ready for commands 😏")
    time.sleep(2)
    bot_loop()
