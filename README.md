# Viklund

Viklund is Python bot (and a little bit of library). Its core functional is based on python273's vk_api library.
Viklund can:
* Send random and latests post from groups and pages using pre-configured .json file (see example.json);
* Search on Wikipedia;
* Get user info;
* Show weather (coming soon)
* Even more, because Viklund was concieved as flexible bot, allowing users to change bot behaviour, abstracting from things like recieving user message and authorization.

## Requirements
* Linux (macOS/FreeBSD might be supported). **Windows is not supported!**
* python3
* vk_api module
* wikipedia module (optional)

## Installation

1. Install vk_api module: 
`# pip install vk_api`
  1.1. Install wikipedia module to use bot's Wikipedia search
 2. Download Viklund: 
`$ git clone https://github.com/blgkv/viklund.git`

## Setup
1. Configure import json file (example at example.json)
2. Edit handle_response.py (if needed)
3. Launch `main.py` with needed arguments (`$ python main.py --help` for help)