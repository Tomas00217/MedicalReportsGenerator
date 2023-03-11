# **Medical Records Generator**

## **Project description**
Automatic generation of medical reports from the RES-Q system. This project is used for bachelor's thesis.

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

If this directory is not present in your ```$PATH```, you can add it in order to invoke Poetry as poetry.

Alternatively, the full path to the poetry binary can always be used:

- ```~/Library/Application Support/pypoetry/venv/bin/poetry``` on MacOS.
- ```~/.local/share/pypoetry/venv/bin/poetry``` on Linux/Unix.
- ```%APPDATA%\pypoetry\venv\Scripts\poetry``` on Windows.
  
All of this information and more can be found on the [official website](https://python-poetry.org/docs/).

## **Running the generator**
Running via command line in the folder with the implementation 
- ```& ((poetry env info --path) + "\Scripts\activate.ps1")```
- ```python .\__main__.py```

Command line options:
- ```-h```, ```--help``` -> Shows the help screen
- ```-i```, ```--subject_id``` -> Specifies the id of the subject for which we want to generate the report. **None** by default, resulting in generating for every subject.
- ```-l```, ```--language``` -> Specifies the language file which we want to use for the generation process. **en_US** by default.
- ```--csv``` -> Option for test and showcase purposes reading from the csv instead of database.