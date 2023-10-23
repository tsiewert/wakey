# wakey
Short workaround for a telegram wake-on-lan bot

!WORK IN PROGRESS!
# Introduction

This will hopefully become a short workaround for a wake-on-lan telegram bot, hosted on a machine within in the network.
The functions and specifications of the code should be:
- Overall layout in python
- Reachable from outside of the network
- Expandable server list
- high-availability

So far it is running as a python script, using a telegram bot with wakeonlan, running locally on a Raspberry Pi.
Dependencies, which worked so far:
- Python 3.11
- wakeonlan 3.0.0
- python-telegram-bot 20.6

# Usage

## Server list
Now we have to create a list of the servers, which we would like to wake up with the bot.
For that, create an empty json file like `server.json`:
```
{
  "<server name 1>" : "<mac addr. 1>",
  "<server name 2>" : "<mac addr. 2>",
  ...
}
```
Replace `<server name X>` and `<mac addr. X>` with your server names and the correspondig mac address with the format `FF:FF:FF:FF:FF:FF`.

## Telegram bot
First you have to create a new telegram bot for yourself. This can be easily done by using the BotFather bot in telegram.
Start the conversation with `/newbot`. The bot will ask you then to choose a name and  username for the bot.
After finding a free name and username, the BotFather will give you the HTTP API token to access your newly created bot.
The token should be placed in a txt file, which the python script will read in.

## Start and use the telegram bot
By simply running `$python3 wakey.py &` the bot will start on the local machine and can be accessed with the telegram bot via the following commands:
- `/wakey` will print the server list. By clicking one of them, the wol command will be send.
- `/update` will reload the `server.json` file and update the server list, accessible with `/wakey`.
- `/help` the usual help command, which will list the available commands.

# Outlook
I'm planning to implement the following things:
- Response if server is alive after wol
- Command to list which server are already alive (probably with a simple ping)
- Combine files of bot token and server list into a single config.json file
- Combine everything into a docker image
