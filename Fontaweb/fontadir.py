#!/usr/bin/python

import os
import sys

version = "1.0"

def banner():
	print "     ____                                     X                                  "
	print "    /XXXX\   _       _   __              _    _   ___                            "
	print "    |XX|_   / \  |\  X|  \X\      /\    | \  | | |   \                           "
	print "    |  __\ / X \ |X\ X| |-X-|    /  \   |  \ | | | __/                           "
	print "    |  |   \ X / |X \X|  |X|_   / XX \  |  / | | |   \                           "
	print "    |_/     \_/  |X  \|  \___\ /_    _\ |_/  |_| |/ \_\                          "
	print "" 
	print "                                     Version " + version + "                     "
	print ""
	print "    Way to use: python2 fontadir.py http://www.site.com                          "
	print "\n"
	
def getHiddenCodes():
	return "404,403"
	
def getExtensions():
	return "php,asp,txt,bkp,pdf,doc,docx"

def validaHttp(url):
	
	url = url.replace("/","")
	
	if (url.count("http:") == 0 and url.count("https:") == 0):
		url = "https://" + url
	else:
		if url.count("http:") != 0:
			url = url.replace("http:","http://")
		if url.count("https:") != 0:
			url = url.replace("https:","https://")
	
	print "[+] URL: " + url
	
	return url
	
def runbuster(directory,url,controller):
	if controller == True:
		scanUrl = url + directory
	
		print "\n[+] Scanning: " + scanUrl
		print "---------------------------------------------------"
		
		dir = url.replace("http://","")
		dir = url.replace("https://","")
		baseDir = dir
		
		dir = dir + "_" + directory
		dir = dir.replace("/","-")
		
		extensions = getExtensions()
		hiddenCodes = getHiddenCodes()
		
		os.system("mkdir " + baseDir + " 2>/dev/null")
		
		os.system("mkdir " + baseDir + "/allDirectories 2>/dev/null")
		
		#command = "gobuster dir -q -e -u " + scanUrl + " -w /usr/share/wordlists/dirb/big.txt -x " + extensions + " -b '" + hiddenCodes + "' -o " + baseDir + "/allDirectories/fontadir_" + dir
		command = "gobuster dir -q -e -u " + scanUrl + " -w /usr/share/wordlists/dirb/small.txt -b '" + hiddenCodes + "' -o " + baseDir + "/allDirectories/fontadir_" + dir
		
		os.system(command)
		
		# adiciona no arquivo com todos os diretorios encontrados
		os.system("cat "  + baseDir + "/allDirectories/fontadir_" + dir + " >> "  + baseDir + "/fontadir_final")
		
		# adiciona no arquivo de urls ja escaneadas
		os.system(" echo '" + scanUrl + "' >> "  + baseDir + "/fontadir_urlsDone")
		
		# pega os diretorios gerados
		command = 'cat '  + baseDir + '/allDirectories/fontadir_' + dir + ' | grep "\[-->" | cut -d ">" -f 2 | cut -d " " -f 2 | cut -d "]" -f 1 >> ' + baseDir + '/diretorios_' + baseDir
		#command = 'cat '  + baseDir + '/allDirectories/fontadir_' + dir + ' | grep "\[-->" | cut -d " " -f 1 >> ' + baseDir + '/diretorios_' + baseDir
		
		os.system(command)
		
		print "---------------------------------------------------"
		
		next = nextUrl(baseDir + '/diretorios_' + baseDir, baseDir + "/fontadir_urlsDone")
		
		if (next != ""):
			nextPath = next.replace(url,"")
			runbuster(nextPath,url,True)
			
		
def nextUrl(urlsToDo,urlsDone):

	print "[+] Getting next URL..."

	testUrl = ""
	
	controller = True
	
	while controller:
	
		with open(urlsToDo) as myfile:
	    		total_lines = sum(1 for line in myfile)

		if total_lines>0:

			with open(urlsToDo) as f:
		    		testUrl = f.readline().rstrip()
		    		
		    	print "[-] Testing: " + testUrl
		    	
		    	os.system("sed -e 1d " + urlsToDo + " > " + urlsToDo + ".new")
		    	os.system("mv " + urlsToDo + ".new " + urlsToDo)
	    	
		    	# valida se a url ja nao foi scaneada antes
		    	with open(urlsDone,  'r') as f:
				for line in f:
					if testUrl.lower() == line.lower().strip():
				    		break
			    		else:
						controller = False
			
		else:
			# se acabou as linhas para validar, seta controler como false para quebrar o loop
			testUrl = ""
			controller = False
    	
    	print "[+] URL found!"
    	
    	return testUrl

def __main__():
	banner()
	
if len(sys.argv) < 2:
	banner()
	sys.exit()
else:
	url = sys.argv[1]
	__main__()
	
	# verify http
	url = validaHttp(url)
	
	# start burpsuite
	runbuster("/",url,True)
