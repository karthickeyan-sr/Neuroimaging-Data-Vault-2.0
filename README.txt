README:

(i)Pre-requisities:
	Kindly install the following software and dependencies before running the code:

	1. Operating System:
		a. Windows 11

	2. Windows Software:
		a. PostgreSQL 14.5:
			Download and install from below link:
				https://www.postgresql.org/download/windows/
		b. Python 3.7:
			Download and install from below link:
				https://www.python.org/downloads/
		c. Anaconda with Spyder
			https://www.anaconda.com/products/distribution

	3. Libraries for python:
		a. os:
			For installation run the follwowing in the command line:
				pip install pandas
		b. psycopg2:
			For installation run the follwowing in the command line:
				pip install psycopg2
		c. pandas:
			For installation run the follwowing in the command line:
				pip install pandas
		d. matplotlib:
			For installation run the follwowing in the command line:
				pip install matplotlib



(ii) Running the code:
	Kindly follow the below instructions to run the code:
	
	1.	The 'dataVault.sql' file can be run by follwing the below instructions:
		a. First connect to postgresql as user 'smd' with password 'smd2022'.
		b. Run 'dataVault.sql' by running the following \i command:
			\i '/SMD2022_Project/code/dataVault.sql'
		The database, schema and tables must be created now.
	
	2. 	Please change the path of the datasets in 'staging.py' python file in 'path' and 'path2' variables which are assigned to VM dataset and Pre-autism dataset respectively.
		The 'staging.py' can by found in the following path: '\SMD2022_Project\code\staging.py'. This can be edited by opening 'staging.py' in Spyder from Anaconda.
	
	3.  The 'staging.py' python file can be run by follwing the below instructions:
		a. First open the 'staging.py' file from '\SMD2022_Project\code\staging.py' using the Spyder (Anaconda) file-->open tab.
		b. After making sure that step 2 has been completed and the correct path of the datasets have been set, click on Run File(F5).


