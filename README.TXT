Signature Automation Package

Version 1.0.0

System Requirements
	Python 2.7 and above
	Linux operating system/Windows

Python Libraries
	requests
	beautifulsoup (bs4)
	selenium
	
Other Package Installation
	- PhantomJs (For linux/ Windows)
		- Refer URL: http://phantomjs.org/download.html 
		- Download the specific package for linux (either 32bit or 64 bit)
		- Extract content of downloaded PhantomJs package
		- Download the installation software (phantomjs.exe) for Windows (either 32bit or 64 bit)
	
Installation
	- Extract the module to a location
	- Create a directrory "phantomjs" at rootlevel and give the executable permission to it.
	- For linux, Copy files of extracted content of PhantomJs into "phantomjs" directory
	- For Windows, put the phantomjs.exe inside "phantomjs" directory
	- Run SignatureAutomation.py
	- The script will generate output files inside "data/Signatures/<<DateFolder>>/<<Product Name>>/"