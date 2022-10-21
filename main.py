import discord
from discord.ext.tasks import loop
import asyncio
import functools
import sys
import random
import requests

from config import CONFIG

class Bot(discord.Client):
	def __init__(self):
		super().__init__()

		self.story_mode = random.random() < float(CONFIG["STORY_CHANCE"])

		# -- initialize ODIN
		response = requests.post("https://odin.deadtired.me/api/auth", json={
			"username": CONFIG["ODIN_USER"],
			"password": CONFIG["ODIN_PASS"],
		})
		try:
			data = response.json()
			self._odin_token = data["token"]
		except:
			print("ERROR:")
			print(response.text)
			sys.exit(1)

	async def on_ready(self):
		print("-- LOGGED IN --")

	def generate_post(self):
		model_name = ""
		text_length = 0
		if self.story_mode:
			model_name = CONFIG["ODIN_STORY_MODEL"]
			text_length = int(CONFIG["ODIN_STORY_LENGTH"])
		else:
			model_name = CONFIG["ODIN_SCHIZO_MODEL"]
			text_length = int(CONFIG["ODIN_SCHIZO_LENGTH"])

		print("Generating post...")
		response = requests.post(f"https://odin.deadtired.me/api/models/{model_name}",
			json={
				"include_prefix": False,
				"length": text_length,
				"temperature": 1.0,
				"top_k": 40,
			},
			headers={
				"X-API-KEY": self._odin_token,
			},
		)

		try:
			data = response.json()
			content = data["data"][0]
		except:
			print("ERROR GENERATING TEXT:")
			print(response.text)
			sys.exit(1)

		print(content)

		if self.story_mode:
			return content[:content.rfind("\n")]
		else:
			return content[:content.rfind(".")] + "."

	async def do_generate_post_async(self):
		return await self.loop.run_in_executor(None, self.generate_post)

	async def startup(self):
		await self.wait_until_ready()

		self.guild = await self.fetch_guild(CONFIG["DISCORD_GUILD_ID"])
		self.channel = await self.fetch_channel(CONFIG["DISCORD_CHANNEL_ID"])

		async with self.channel.typing():
			response = await self.do_generate_post_async()
			hashed = hex(abs(hash(response)) % (10 ** 16))
			header = f"IDENTIFIER {hashed}"

			try:
				await self.channel.send(header)
				await self.channel.send(response)
			finally:
				await self.close()

def main():
	client = Bot()
	client.loop.create_task(client.startup())
	client.run(CONFIG["DISCORD_TOKEN"])

if __name__ == "__main__":
	main()
