# stakepool-blocks-discord-bot
Another Bot for discord to track when your stake pool made a new block XD


## How to use the bot

1. Clone the repo on the server/computer you will use to run the bot 24/7

2. Inside the stakepool-blocks-discord-bot folder create a environment variable file named `.env`

3. Now edit the `.env` file using your preferred text editor and add the following lines

```python
POOL_ID='stake pool bech_32 ID'
DISCORD_TOKEN='Discord Application Token'
DISCORD_GUILD='Discord Guild/Server Name'
CHANNEL_ID='Discord channel ID'
```
4. Now open your computer's terminal CLI and change to the folder and run the script by using following command.

	```python3 block_bot.py```