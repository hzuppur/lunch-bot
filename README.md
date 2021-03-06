# Lunch-bot
Script and an optional Discord bot for choosing lunch options from [päevapakkumised.ee](https://xn--pevapakkumised-5hb.ee/). 

All offers from selected restaurants will be scraped and each restaurant will be assigned an emoji. This can be used to select the preferred location, using message reactions in Slack or Discord.  

You can run the script and copy the output manually or set up a Discord integration that posts all selected lunch offers every workday 11:40 to a selected channel.

## Configure
### Required
- Create a copy of `config/user.example.ini` and rename it to `config/user.ini`.
- Copy the city part from url and replace `location_url` with your location.
- Replace `location` with a comma-separated list of the names of all restaurants you are interested in. Make sure to use exactly the spelling used on the website.
- Delete optional rows you are not using, make sure to leave no placeholder values, like `XXX` for Discord bot token.
### Optional
- Configure optional values, like custom reaction emoji or Discord bot integration. If no Discord bot is configured, the application will just print current offers to console and quit.

## Run using Docker
Refer to Docker documentation for running containers on your platform. Use the provided `Dockerfile`. This is the preferred way of running Lunch-bot, since it avoids having to manage Python environment and dependencies yourself.

## Run locally
Not recommended unless you plan to develop Lunch-bot. Install Python 3.10, install pipenv, install dependencies from `Pipfile.lock` and then run `src/main.py`.

## Run as Discord bot
- Create a Discord application https://discord.com/developers/applications
- Create a Discord bot user and save the token to file `config/user.ini` as `discord_bot_token = YOUR_TOKEN_HERE`
- Find out the channel id where you would like to post lunch offers
  - copy the channel url and select the last part of the url https://discord.com/channels/XXXXXX/CHANNEL_ID
  - save the channel id you found out to file `config/user.ini` as `discord_channel_id = CHANNEL_ID`
- offers will be posted at 11:40
  - optionally, you can specify a timezone as `discord_bot_timezone`, example: Europe/Tallinn
  - UTC will be used if no timezone is configured

If you are hosting the bot yourself, run normally using Docker.

If you are using managed hosting, this option may not be available. An autogenerated `requirements.txt` file is provided for this use case that should work for most managed hosts. Upload the files, create and edit the user config file, set entry point as `src/main.py`.  

----


## Example output of the script is shown below

## Päevapakkumised 21.märts 
### 1️⃣ Delta kohvik:
* Pardi-confit kartulite/riisi/tatra, kastme ja salatiga. 5,80€
* Rebitud sealiha kartulite/tatra, kastme ja salatiga. 5,50€
* Kapsakotlet kartulite/riisi/tatra, kastme ja salatiga (V). 4,90€
* Kana poolkoib kartulite/tatra, kastme ja salatiga. 4,80€
* Köögivilja püreesupp. 3,00/2,00€
### 2️⃣ Cafe Naiiv:
* Krõbekana kauss. 4,90€
* Falafeli kauss. 4,50€
### 3️⃣ The Grill:
* Gruusia Odzahuri: praetud sealiha kartulitega, paprika ja sibulaga, kaste, leib, maitsevesi. 5,00€
