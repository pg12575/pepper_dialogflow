# Pepper_Dialogflow

## Virtual Environments
For this code to run, there needs to be two python virtual environments:
- py2.7venv - Python2.7 virtual environment with modules listed in py2.7requirements.txt
  - Additionally, Pepper Python SDK needs to be installed for Python2.7. See link - http://doc.aldebaran.com/2-4/dev/python/install_guide.html
- py3venv - Python3 virtual environment with modules listed in py3requirements.txt

## Dialogflow Credentials
There also needs to be a credentials.json file in the root folder. See here - https://dialogflow.com/docs/reference/v2-auth-setup

There are currently four scripts, only main.py needs to be run using python2.7.

## Acknowledgements

A lot of the code is borrowed from https://medium.com/@pwc.emtech.eu/pepper-integration-with-dialogflow-1d7f1582da1a. However, Dialogflow and Pepper's Python SDK have been separated into Python3 and Python2.7 scripts, due to Dialogflow no longer supporting Python2.7.
