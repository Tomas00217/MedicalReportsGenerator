# **Medical Reports Generator** <!-- omit in toc -->

## **Contents** <!-- omit in toc -->
- [**Project description**](#project-description)
- [**Installation**](#installation)
  - [**Python**](#python)
  - [**Poetry**](#poetry)
  - [**Postgresql**](#postgresql)
- [**Project download**](#project-download)
- [**Preparing the database**](#preparing-the-database)
- [**Running the generator**](#running-the-generator)
- [**Writing report structure**](#writing-report-structure)


## **Project description**
Automatic generation of medical reports from the RES-Q system. This project is used for bachelor's thesis.
The production version of generator requires connection to a postgres database. For showcase purposes reading from csv with cmd option ```--csv``` is possible. 
The prepared .csv contains 7 records that can be generated. If you wish to only use the ```--csv``` option, you can skip the installation of [postgresql](#postgresql) as well as skip the preparation of the database [part](#preparing-the-database) and setting the env variables.

## **Installation**

### **Python**
Required **Python 3.7** or higher.

Python can be downloaded from their [official website](https://www.python.org/downloads/). To install python, follow the instruction in the setup wizard, make sure to add python to PATH during the installation.

### **Poetry**
Next up is installing poetry, which is a tool for dependency management.  

On Windows (Powershell)
```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

On Linux, macOS, Windows (using WSL)
```
curl -sSL https://install.python-poetry.org | python3 -
```

**Add Poetry to your PATH**

The installer creates a poetry wrapper in a well-known, platform-specific directory:

- ```$HOME/.local/bin``` on Unix.
- ```%APPDATA%\Python\Scripts``` on Windows.

If this directory is not present in your ```$PATH```, you can add it in order to invoke Poetry as poetry. After adding poetry to PATH, restart of the computer is required. To check if the poetry is installed, run ```poetry --version```.

Alternatively, the full path to the poetry binary can always be used:

- ```~/Library/Application Support/pypoetry/venv/bin/poetry``` on MacOS.
- ```~/.local/share/pypoetry/venv/bin/poetry``` on Linux/Unix.
- ```%APPDATA%\pypoetry\venv\Scripts\poetry``` on Windows.
  
All of this information and more can be found on the [official website](https://python-poetry.org/docs/).

### **Postgresql**
This step can be skipped if you only want to test the application with ```--csv``` option.

Download version 15.2 from this [link](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) and install by following the instruction in wizard.

## **Project download**
The project can be downloaded from [github](https://github.com/Tomas00217/MedicalRecordsGenerator).

Clone the project to the designated folder with running the command:
```
git clone https://github.com/Tomas00217/MedicalRecordsGenerator.git
```

In case you do not have git installed, follow the instructions on this [link](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## **Preparing the database**
This step can be skipped if you only want to test the application with ```--csv``` option.

1. Open **cmd** and navigate to the bin folder of postgresql e.g. ```C:\Program Files\PostgreSQL\15\bin```

2. Create empty database by running command (input the password of your user specifed by -U if required): 
    ```
    createdb.exe -U <username> -E UTF8 -T template0 --locale=en_US.UTF-8 <database name>
    ```
    ```<username>``` is the user name under which u want to connect to database (usually postgres)

    ```<database name>``` is the name of the database you want to use

    Example: ```createdb.exe -U postgres -E UTF8 -T template0 --locale=en_US.UTF-8 strokemodel```

3. Restore the database by running command (input the password of your user specifed by -U if required):
   ```
   pg_restore.exe -U <username> -d <database name> <path\strokemodel_backup.tar>
   ```
    ```<username>``` is the user name under which u want to connect to database (usually postgres)

    ```<database name>``` is the name of the database from previous step.

    ```<path>``` is the path where you have clonned the project, from there we want the file **strokemodel_backup.tar**

    Example: ```pg_restore.exe -U postgres -d strokemodel "C:\MedicalRecordsGenerator\strokemodel_backup.tar"```

## **Running the generator**
To run the implementation we first need to install the dependecies, that can be done running command via command line in the folder we clonned the project to.
- ```poetry install```

**Set environment variables for database**

This can be skipped if you decided not to prepare the database.

Activate the virtual environment by running:
- ```poetry shell```

Then set the env variables for database, set the following:
- ```SET EMS_DB_USER=<username>```
- ```SET EMS_DB_PASSWORD=<password>```
- ```SET EMS_DB_HOST=<host>```
- ```SET EMS_DB_NAME=<database name>```

where
- ```<username>``` - user name used for authentication when creating db
- ```<password>``` - password used for authentication
- ```<host>``` - host address of the database
- ```<database name>``` - database name used when creating db

Example:
- ```SET EMS_DB_USER=postgres```
- ```SET EMS_DB_PASSWORD=Heslo.1```
- ```SET EMS_DB_HOST=localhost```
- ```SET EMS_DB_NAME=strokemodel```

**Run the program**

Running the implementation is possible via command line

- ```py medicalrecordgenerator``` while in virtual environment 
- ```poetry run py medicalrecordgenerator``` when outside virtual environment

Accessing the virtual environment is possible with ```poetry shell```

Leave virtual environment with ```exit``` 

Command line options:
-  ```-h, --help``` -> show this help message and exit
-  ```-c [CSV], --csv [CSV]``` ->
                        Specify whether to load data from csv instead of
                        database, value supplied with this option specifies
                        the csv file, when omitted default csv is used
-  ```-l LANGUAGE, --language LANGUAGE``` ->
                        Specify the language which to use for the generation
                        process. en_US by default.
-  ```-i SUBJECT_ID, --subject_id SUBJECT_ID``` ->
                        Specify the id of the subject for which to generate
                        the report. None by default, resulting in generation
                        for every subject.
-  ```-t TEMPLATE, --template TEMPLATE``` ->
                        Specify the path to report definition template to be
                        used
-  ```--list``` ->                Lists the available subject ids and exits
-  ```-s [STORE], --store [STORE]``` ->
                        Specify whether to store the result to txt file,value
                        supplied with this option specifies the file path,
                        when omittedresult is stored to project root.


## **Writing report structure**
The rules for writing the structure for reports is described [here](reports_format.md).
