# Viklund
Click [here](https://github.com/blgkv/viklund/tree/russian) for Russian version.

Viklund is Python bot (and a little bit of library). Its core functional is based on python273's vk_api library.

Viklund can:
* Send random and latests post from groups and pages using pre-configured .json file (see example.json);
* Search on Wikipedia;
* Translate using Google Translate API.
* Get user info;
* Show weather (coming soon)
* Even more, because Viklund was concieved as flexible bot, allowing users to change bot behaviour, abstracting from things like recieving user message and authorization.

## Table of contents
* [Requirements](https://github.com/blgkv/viklund#requirements)
* [Installation](https://github.com/blgkv/viklund#installation)
* [Setup](https://github.com/blgkv/viklund#setup)
* [License](https://github.com/blgkv/viklund#license)
* [Thanks to](https://github.com/blgkv/viklund#thanks-to)

## Requirements
* Linux (any POSIX-compatible OS might be supported). **Windows is not fully supported**, however, it works with some limitations.
* python3
* vk_api module
* wikipedia module (optional)
* googletrans module (optional)

## Installation

1. Install vk_api module: 
`# pip install vk_api`
    * 1.1 (Optional) Install wikipedia module to use bot's Wikipedia search
    * 1.2 (Optional) Install googletrans module to use bot's Google Translate translation. 
 2. Download Viklund: 
`$ git clone https://github.com/blgkv/viklund.git`

## Setup
1. Configure import json file (example at example.json)
2. Edit handle_response.py (if needed)
3. Launch `main.py` with needed arguments (`$ python main.py --help` for help)

## License
[GNU GPLv3](https://github.com/blgkv/viklund/blob/master/LICENSE)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Thanks to:
* github.com/python273, the creator of vk_api module
* github.com/goldsmith, the creator of wikipedia module
* github.com/ssut, the creator of googletrans module
