# Arcoex Bot
![This is Arcoex!](http://i.imgur.com/oDU2O89.png)
A Discord bot aimed at arbitrary code execution.

## Features

- Easy to expand. Adding new languages is extremely simple!
- All languages work, even compiled ones. It doesn't matter how unknown is your language, this bot will be able to run it!
- It reacts to everything you throw at him:
  - There's a typo in your code or something goes wrong? The bot will give you the compiler output or the traceback.
  - Did you make an infinite loop? The bot will take care of it, kill the process and give you the last lines of output.
  - The language you're trying to use isn't supported? The bot will tell you.
  - The output is too long for Discord? The bot will upload it to [hastebin.com](https://hastebin.com) and give you the link.
- The sandboxed environment will protect the bot from malicious code! Say goodbye to fork bombs or trying to run `rm -rf --no-preserve-root /`.

## Get the bot

If you want to use this bot in your server without running it manually, you can invite it to your server [clicking here.](https://discordapp.com/oauth2/authorize?client_id=350327901788569612&scope=bot&permissions=0)

You can also check it out [by joining this Discord server.](https://discord.gg/yeZnCvc)

## Usage

Using the bot is really simple! If you want instructions, just mention the bot and he'll send you a PM with the full instructions. However, using this bot is as simple as mentioning him with the block of code you want to run, and mentioning the language the code is written in (either between the mention and the code block, or as a markdown language inside the code block, or even both if you feel like so!)

For more detailed instructions and example, just mention the bot.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to use this bot, among using Python 3.4+, you'll need the following software installed and working on your machine.

#### Discord modules

You'll need to have [discord.py](https://github.com/Rapptz/discord.py) and [hastebin.py](https://github.com/LyricLy/hastebin.py) installed. You can either use a virtualenv:
```
virtualenv .
cd bin
source activate
pip install discord.py && pip install hastebin.py
```

Or you can install them as user.
```
pip install --user discord.py && pip install --user hastebin.py
```

#### UMLBox

In order to have the arbitrary code properly sandboxed, this bot uses [UMLBox](https://bitbucket.org/GregorR/umlbox/wiki/Home). Here are [instructions about how to set up UMLBox.](https://bitbucket.org/GregorR/umlbox/src/73e732639635228f3eef6ddd8738d6947ed9837d/README?at=default&fileviewer=file-view-default)

This is an example using the linux kernel 4.12.9.
```
hg clone https://bitbucket.org/GregorR/umlbox
cd umlbox
wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.12.9.tar.xz
tar -xf linux-4.12.9.tar.xz
sed -i '6s/.*/LINUX=linux-4.12.9/' Makefile
make all && make install
```

in order to test umlbox, run the following command in your machine. If it outputs "It works", then everything should be set up correctly.
```
umlbox -B echo "It works"
```

#### Build tools

You'll also need to have the tools to run code in your local machine. This tools are different depending on the language that will be run. If you want more info regarding which tools you'll need, [You can check this.](languages)

### Installing

If you've installed the prerequisites and checked if they work properly, you are almost good to go. First of all, clone this repository.
```
git clone https://github.com/Kurolox/ArcoexBot
```

After that, modify auth.py with your text editor of choice, and add your Discord bot token. It should look like this:
```
bot_token = "MjA5MzE3MDM3MTgzNDY3NTIw.DIV9oA.UuTk8pA7WA6PFDvhJXVPnYUKX0I"
```

Once that's done, just run arcoex.py and everything should start to work.
```
python arcoex.py
```

## Deployment

In order to run this in a server, I'd recommend you to install `screen` and make a systemd unit file that will launch the bot at startup.

This is an example on how to do this. Since installing `screen` depends on your distribution, you should already know how to install packages and software in your machine.

First, create a file in `/etc/systemd/system`, called `arcoex-bot.service` (you may need root privileges to do this.) and edit it with your text editor of choice so it looks like this:
```
[Unit]
Description= Arcoex Bot for Discord

[Service]
RemainAfterExit=yes
ExecStart=/usr/bin/screen -S arcoex -dm python /path/to/arcoex.py
ExecStop=/usr/bin/screen -S arcoex -X quit
User=INSERTUSERHERE

[Install]
WantedBy=multi-user.target
```
Replace `INSERTUSERHERE` with the user you want the bot to be ran under, and replace `/path/to/arcoex.py` with the absolute path to `arcoex.py`

If you are using a virtualenv, replace `python` for `/path/to/virtualenv/bin/python`, being that path the absolute path to your virtualenv.

As a warning, you should be sure that the user you choose does have write permissions in the bot folder.

In order to activate the bot so it launches with your system, execute this command.
```
systemctl enable arcoex-bot.service
```

If you want to start, stop or restart the bot manually, you can do so with the following commands.
```
systemctl start arcoex-bot
systemctl stop arcoex-bot
systemctl restart arcoex-bot
```

## Contribute

If you want to contribute to this project, feel free to do so! Create an issue or fork the project and make a pull request, any help is appreciated and I'd be glad to know that someone out there wants to see this project grow.

## Built With

* [Discord.py](http://discordpy.readthedocs.io/en/latest/api.html) - Python discord API
* [UMLBox](https://bitbucket.org/GregorR/umlbox/wiki/Home) - User Mode Linux based sandboxing solution

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

