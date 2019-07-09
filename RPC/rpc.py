import os
import sys
import requests
import datetime
os.system("clear")

def help():
	print('||RPC: (RPC Path Cracker) 1.1||')
	print('\t-t  Target URL (ex: -t https://www.example.com)')
	print('\t-d  Select a dictionary (ex: -d dictionary1.txt)')
	print('\t-r  Uses recursive search')
	print('\t-h  Displays this menu')

def save(response, dirList):
	date = datetime.datetime.now()

	directoriesCollected = len(dirList)
	save = input('Do you want to save the report? (y/n):' )
	if(save == 'y'):
		filename = input('Save as: ')
		saveFile = open(filename, "w")
		saveFile.write('Report date: ' + date.strftime("%x") + '\tDirectories found: ' + str(int(directoriesCollected/2)) + '\n')
		for x in range (0,directoriesCollected,2):
			saveFile.write(str(dirList[x]) + ' ' + str(dirList[x+1]) +'\n')

		saveFile.close()

def search(url,dictonaryFilename,response,dirList,dirDepth,isRecursive):
	keepSearching = True
	directoryFound = False
	lastPos = len(dirList)-1
	if(keepSearching):
		try:
			dictonaryFile = open(dictonaryFilename, "r")
			try:
				for x in dictonaryFile:
					x = x[:-1] #removes newline
					response = requests.get(url+x)
					if(response or response.status_code == 403):
						directoryFound = True
						dirList.append(response.url)
						dirList.append(response.status_code)
						lastPos = len(dirList)-1

						if(dirDepth>1):
							print ('┃',' '*dirDepth,'┗━',dirList[lastPos-1], dirList[lastPos])
						else:
							print ('┣'+'━━'*dirDepth,dirList[lastPos-1], dirList[lastPos])

						if(isRecursive == True and response.status_code != 403): #Recursive search (-r)
							if(directoryFound == True):
								search(dirList[lastPos-1],dictonaryFilename,response,dirList,dirDepth+1,True)
				dictonaryFile.close()
			except:
				print('\nProgram stopped.')
				keepSearching = False
		except:
			print('\nInvalid filename: ', dictonaryFile, ' file not found')


isRecursive = False
dictonaryFilename = 'default'

if(len(sys.argv) == 1): #checks if the program recives no parameters
	help();
else:
	try:
		for x in sys.argv: #console parameters list
			if(x == '-h'):
				help()
			elif(x == '-r'):
				isRecursive = True
			elif(x =='-d'):
				dictonaryFilename = sys.argv[sys.argv.index('-d')+1]


		for x in sys.argv:
			if(x == '-t'):
				url = sys.argv[sys.argv.index('-t')+1]
				try:
					response = requests.get(url)
				except:
					print('Invalid URL (ex: -t https://www.example.com -d dictionary1.txt)')
					break
				dirList = [response.url, response.status_code]
				print ('┏',dirList[0], dirList[1])
				search(url,dictonaryFilename,response,dirList,1,isRecursive)
				try:
					save(response, dirList)
				except:
					print('\nAn error ocurred while saving.')
	except:
		print('Invalid format (ex: -t https://www.example.com -d dictionary1.txt)')
