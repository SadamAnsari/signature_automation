Extra-Scripts Package 

Version 1.0.0

System Requirements
	Python 2.7 and above
	Linux operating system

Python Libraries
	cx_Oracle
	The following steps are configured before installing cx_oracle python package on linux.
	
	1. Dependencies
		Install the following packages:
			apt-get install python-dev build-essential libaio1
	
	2. Download Instant Client for Linux (32 bit/64 bit)
		- Download the following files from Oracle's download site:
			For example:  instantclient-basic-linux.x64-11.2.0.4.0.zip
						  instantclient-sdk-linux.x64-11.2.0.4.0.zip
	
	3. Extract the zip files
		Unzip the downloaded zip files to some directory, I'm using:
			>> /opt/oracle
	
	4. Add environment variables
		Create a file in /etc/profile.d/oracle.sh that includes
			export ORACLE_HOME=/opt/oracle/instantclient_11_2
			export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
		Create a file in /etc/ld.so.conf.d/oracle.conf that includes
			/opt/oracle/instantclient_11_2
		Execute the following command
			>> sudo ldconfig
		Note: you may need to reboot to apply settings
	
	5. Create a symlink
		>> cd $ORACLE_HOME ln -s libclntsh.so.11.1 libclntsh.so
	
	6. Install cx_Oracle python package
		- You may install using pip
			>> pip install cx_Oracle
		
		- Or install manually
			Download the cx_Oracle source zip that corresponds with your Python and Oracle version. Then expand the archive, and run from the extracted directory:
			>>	python setup.py build 
			>>	python setup.py install
			
	The following steps are configured before installing cx_oracle python package for Windows.
	
	1. Download Instant Client for Windows (32 bit/64 bit)
		- Download the following files from Oracle's download site:
		    http://www.oracle.com/technetwork/topics/winx64soft-089540.html
			For example:   instantclient-basic-win-x86-64-11.2.0.1.0.zip
						   instantclient-sdk-win-x86-64-11.2.0.1.0.zip
	
	2. Extract the zip files
		Unzip the downloaded zip files to some directory, I'm using (C drive):
			>> /Oracle
	
	3. Add environment variables
		- GOTO Control Panel\All Control Panel Items\System\Advanced System settings
		Set the following details:
				variable name: 		  	ORACLE_HOME
				variable value:			C:\Oracle\instantclient_11_2
	
	4. Install cx_Oracle python package
	
	
Installation
	- Extract the module to a location
	1. checkpoint_signature.py -s <<oracle server>> -u <<oracle db username>> -p <<oracle db passoward>> 
							-d <<device_type_id>>  -c <<csv_file>>
		- The output of this script goes into "CheckPoint_Signature" directory inside "extra-scripts"
	2. paloalto_signature.py -s <<oracle server>> -u <<oracle db username>> -p <<oracle db passoward>> 
							-d <<device_type_id>>  -c <<csv_file>>
		- The output of this script goes into "PaloAltoIPS_Signature" directory inside "extra-scripts"
	3. TPTI_DV.py -f <<File_Name>>
		- <<File_Name>> must be in html format.
		- The output of this script goes into "TPTI_DV" directory inside "extra-scripts"
	
		