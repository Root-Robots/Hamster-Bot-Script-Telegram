import os
import subprocess

# Paste Token Here if you don't wanna put it in an env. variable for some reason
TOKEN_INSECURE = "<PASTE YOUR TELEGRAM BOT TOKEN  HERE>"

if os.name == 'posix':
    TOKEN = subprocess.run(["printenv", "HAMSTER_BOT_TOKEN"], text=True, capture_output=True).stdout.strip()
elif os.name == 'nt':
    TOKEN = subprocess.run(["echo", "%HAMSTER_BOT_TOKEN%"], text=True, capture_output=True, shell=True).stdout.strip()
    TOKEN = "" if TOKEN == "%HAMSTER_BOT_TOKEN%" else TOKEN

TOKEN = TOKEN or TOKEN_INSECURE
AUTHORIZED_USERS = []
EXCLUSIVE = False

USE_PROXIES = False