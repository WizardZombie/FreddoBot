# FreddoBot
FreddoBot is a bot to inform you just how terrible the economy is. At 30 pence a pop, freddos are now *outrageously* expensive, do cadbury think I'm made of money?!

FreddoBot takes your local currency and tells you just how many Freddos you can buy with it, as well as how many you could have bought at their initial price

Use £convert [value] [currency] to find this out. Currency defaults to USD if none provided

Use £currentrates to list all availible currencies and the current exchange rate stored as compared to GBP. This is updated a maximum of once every 24 hours to not abuse the API. Thanks to https://exchangeratesapi.io for providing the exchange rates.

To set up your own instance:
  Download the files in this repo, and save them in a new folder
  Navigate to said folder through your teminal 
  Run `python3 main.py`
  On initial start, you will be prompted for a token for a bot. Paste it in, the bot will then start up.
  
  Requires Python 3.6, discord.py, aiohttp
 
If you want to use my instance:
  Click this link: https://discordapp.com/oauth2/authorize?client_id=544997787713142796&scope=bot&permissions=8 
  *This has admin permissions because I'm lazy. If you don't want that, feel free to change the permissions to whatever you     wish. Simply copy the link, and change the 8 on the end to whatever you want to grant it.*
