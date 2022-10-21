import os

from dotenv import load_dotenv
load_dotenv()

CONFIG = {
  "DISCORD_TOKEN": "",
  "DISCORD_GUILD_ID": "",
  "DISCORD_CHANNEL_ID": "",

  "ODIN_USER": "",
  "ODIN_PASS": "",

  "ODIN_STORY_MODEL": "morella-full-500",
  "ODIN_STORY_LENGTH": 256,

  "ODIN_SCHIZO_MODEL": "",
  "ODIN_SCHIZO_LENGTH": 256,

  "STORY_CHANCE": 0.5,
}

for key, value in CONFIG.items():
  # If key has no default value, it's required
  if value == "":
    if key not in os.environ:
      print(f"ERROR: '{key}' is a required environment variable!")
      os._exit(1)

    CONFIG[key] = os.environ[key]
  else:
    # Overwrite default values if present in environment
    if key in os.environ:
      CONFIG[key] = os.environ[key]
