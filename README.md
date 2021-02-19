# RAPTUS Discord Bot
## Installation Instructions
1. Clone the repo into your system, then `cd` into it.
2. Ensure the proper GPT2 models are on your system, and then symlink the directory with `ln -s <path_to_models> models`.
3. Copy `config.example.py` to `config.py` and fill out the fields.
4. Run `sudo bash install.sh` to install pip packages, and set up the systemd service and timer.
