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

		self.story_mode = random.choice([True, False, False, False, False, False])

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

			return story
		else:
			schizo_post = gpt2.generate(
				self.gpt2_sess,
				include_prefix=False,
				model_name=config.schizo_model,
				return_as_list=True,
				length=256,
				temperature=1.0,
				top_k=40
			)[0]

			return schizo_post

	async def do_generate_post_async(self):
		return await self.loop.run_in_executor(None, self.generate_post)

	async def startup(self):
		await self.wait_until_ready()

		self.guild = await self.fetch_guild(config.guild_id)
		self.channel = await self.fetch_channel(config.channel_id)

		async with self.channel.typing():
			if self.story_mode:
				header = "Today, I have a story. "
				if random.choice([True, False]):
					header += "I would {} for you to listen.".format(random.choice(["love", "like"]))
				else:
					header += "Sit down {}".format(random.choice(["for a while and listen.", "and listen.", "for a bit."]))
				header += "\n"

				await self.channel.send(header)
			else:
				header = "ENTRY 0x{}\n".format(random.randrange(1000, 9999))

				await self.channel.send(header)

			response = await self.do_generate_post_async()
			response = response[:response.rfind("\n")]

			try:
				await self.channel.send(response)
			finally:
				await self.close()


def main():
	client = Bot()
	client.loop.create_task(client.startup())
	client.run(config.token)

if __name__ == "__main__":
	main()
