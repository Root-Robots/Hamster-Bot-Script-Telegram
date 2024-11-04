# Hamster-Key-Telegram-Bot

This is a simple telegram bot you can host on your own computer to generate 
Hamster Kombat keys.

![image](https://github.com/user-attachments/assets/52d2ef28-9fca-4d34-b927-3d2dc178312f)


## Update

1. All settings have been moved to **"config.py.default"**. You should rename this file to
**"config.py"** before you use the bot. With this change, once you set your token in config.py, 
you don't have to reset it everytime there is an update to the bot. 

2. Proxies have been added. They are disabled by default, but you can enable them in config.py
by changing `USE_PROXIES = False` to `USE_PROXIES = True`. Free proxies are fetched automatically
from proxyscrape.com, but if you have your own proxies, you can specify them in **"proxies.txt"**.
Free proxies are, however, really unreliable, so I recommend you use paid proxies and put them in
proxies.txt

3. Keys are now sent to the client immediately as they are generated instead of waiting for all
requested keys to be generated. This is because the addition of proxies makes requests highly 
volatile. Some keys might generate quicker, and some might be really slow, so this makes sure
that, at least the generated keys don't just sit on the server, and are sent to the client.

4. New entries in requirements.txt that need to be installed using pip. 


## Getting Started

The first thing you have to do is go talk to the [BotFather](https://t.me/BotFather) on telegram.
After you do _/newbot_, It will ask you a series of simple questions and all you
have to do is give it the name, and username of your bot and it will give you
an **API TOKEN**. This token is how you will access the telegram API. The bot
won't work without it.

Now, clone this repo:
```sh
git clone https://github.com/Emperor-One/Hamster-Key-Telegram-Bot.git
```
You will need to [download](https://www.python.org/downloads/) python if you don't have it on your system.

Next, you have to rename config.py.default to config.py, and you will open the config.py file with your text editor of choice.
Now, copy paste your **API TOKEN** to the following variable:
```python
TOKEN_INSECURE = "<PASTE YOUR TELEGRAM BOT TOKEN  HERE>"
```
It should look something like this:
```python
TOKEN_INSECURE = "7461996478:AAG7j04LJ8m6fmXLjarmyiRU9S2AhTg6Lot7iiw"
```
---
**Warning:** It is highly recommended that you do not save your API TOKEN in plain text
in the code. If you want to be secure you should save your Token in an environment
variable named HAMSTER\_BOT\_TOKEN. See the [Environment Variables](#environment-variables)
section below.

---

Once you have saved your token to config.py or to an environment variable, install the required packages with this command:
```sh
pip install -r requirements.txt
```

Optionally, here, you could also create a [virtual environment](#virtual-envrionemnts), but it is not required.

Finally, you can run the bot, and enjoy your keys.
```sh
python bot.py
```

## Stealth

It is important to note that this bot is intended to be used by multiple users at a time, and is not stealthy at all.
If, however. you are interested in a stealthy and accurate method of generating keys, you should check out this [repo](https://github.com/Emperor-One/StealthyHamster).
It is much slower than this bot, but you have a smaller chance of being detected as a key generator. It still has flaws, like
most games are not supported and it needs to support TLS fingerprint spoofing to be fully undetectable, 
but it completely emulates the supported games in all other aspects.
It will be updated, slowly, as I figure out how the keys are actually being generated for each game.

## Proxies

Proxy support has been added to the bot as of 09-05-2024. Proxies are disabled by default. If you want to enable them you
need to change the `USE_PROXIES` variable **config.py** to 
```python
USE_PROXIES = True
```
Free proxies are fetched automatically from proxyscrape.com, but if you have your own proxies, you can specify them in **proxies.txt**. 
Free proxies are, however, really unreliable, so I recommend you use paid proxies and put them in proxies.txt.

## Exclusive Mode
This bot can be set to exclusive mode meaning you can make it so that only the people you authorize can use
the bot.
In order to do this, set the EXCLUSIVE variable in config.py to True:
```python
EXCLUSIVE = True
```
Then, add your Telegram User ID to the AUTHORIZED_USERS list:
```python
AUTHORIZED_USERS = [
    <Your User ID>,
    <Your Friends User ID>
]
```
You can get your User ID values from the console, as they are printed out every time
someone sends a command to the bot.

## Environment Variables
Saving your tokens to environment variables is not necessary (especially if you don't plan to share your code), 
but it is a recommended practice.

If you are on windows, open command prompt and type:
```batch
setx %HAMSTER_BOT_TOKEN% <YOUR TOKEN HERE>
```
If you are on Linux or macOS, open your terminal and type:
```sh
export HAMSTER_BOT_TOKEN=<YOUR TOKEN HERE>
```

**Note:** After you set the environment variable, you will have to close the current shell, and open a new one
for the changes to take effect. This change will persist until you reboot your computer
or log out. You have to run the above command again to reset the environment variable.

To make the environment variable persist after reboots, on **Linux/macOS**, you can add the above command
to your ~/.bashrc or ~/.zshrc file.

On **Windows**, run cmd as Administrator and type this command:
```batch
setx %HAMSTER_BOT_TOKEN% <YOUR TOKEN HERE> /M
```

## Virtual Envrionments
Python virtual environments are beneficial because they isolate project dependencies, preventing version conflicts and ensuring that each project has a consistent, controlled setup. This makes it easier to manage and deploy multiple projects with different requirements on the same system.

To set it up on **Windows:**
```batch
python -m venv venv
.\venv\Scripts\activate.bat
```
On **Linux/macOS:**
```sh
python -m venv venv
bash -c "source ./venv/bin/activate"
```
