import gpt_2_simple as gpt2
import discord
from discord.ext.tasks import loop
import asyncio
import sys
import functools
import random

import config


class Bot(discord.Client):
	def __init__(self):
		super().__init__()

		self.story_mode = random.random() < config.story_chance

	async def on_ready(self):
		print("-- LOGGED IN --")

	def generate_post(self):
		print("Loading GPT models...")
		self.gpt2_sess = gpt2.start_tf_sess()

		if self.story_mode:
			gpt2.load_gpt2(self.gpt2_sess, model_name=config.story_model)
		else:
			gpt2.load_gpt2(self.gpt2_sess, model_name=config.schizo_model)

		print("Generating post...")
		if self.story_mode:
			story = gpt2.generate(
				self.gpt2_sess,
				include_prefix=False,
				model_name=config.story_model,
				return_as_list=True,
				length=356,
				temperature=1.0,
				top_k=40
			)[0]
			story = story[:story.rfind("\n")]

			return story
		else:
			schizo_post = gpt2.generate(
				self.gpt2_sess,
				include_prefix=False,
				model_name=config.schizo_model,
				return_as_list=True,
				length=300,
				temperature=1.0,
				top_k=40
			)[0]
			schizo_post = schizo_post[:schizo_post.rfind(".")] + "."

			return schizo_post

	async def do_generate_post_async(self):
		return await self.loop.run_in_executor(None, self.generate_post)

	async def startup(self):
		await self.wait_until_ready()

		self.guild = await self.fetch_guild(config.guild_id)
		self.channel = await self.fetch_channel(config.channel_id)

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
	client.run(config.token)

if __name__ == "__main__":
	main()
