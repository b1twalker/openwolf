# OpenWolf 🐺 - Your Open-Source Discord assistant

🌐 **[Українська версія](README_uk.md)**

OpenWolf is an open-source Discord bot designed for small communities and open-source enthusiasts. Its primary focus is server moderation, but it also serves as a customizable base for forking and tailoring to specific needs.

## Who Is This Project For? 🎯
OpenWolf is perfect for:
- **Small Discord communities** looking for a reliable, lightweight moderation bot. 🛡️
- **Open-source enthusiasts** who value autonomy and want full control over their bot. 🌐
- **Developers** interested in forking and customizing a bot to fit their unique server needs. 💻

## Key Features ✨
- **Moderation**: Ban, kick, timeout, message clearing, and channel lockdown/unlock functionalities. 🚨
- Extensible base for customization through forks to meet specific community requirements. 🔧
- Utility features like fixing messages typed in the wrong keyboard layout. ⌨️

## Technical Details 🛠️
- **Programming Language**: Python
- **Libraries**: discord.py and standard Python modules (e.g., `json`, `os`, `configparser`)
- Built with flexibility in mind for future enhancements and community contributions.

## Installation and Setup 📦
1. Ensure Python (version 3.8 or higher) is installed.
2. (Recommended for Linux/macOS) Create a virtual environment:
   ```bash
   python -m venv .venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```
3. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications) and obtain its token.
5. Run `main.py`. On first launch, follow the setup wizard to configure the `openwolf.ini` file.

## Configuration and Customization ⚙️
Currently, configuration options are limited (e.g., language selection, log level, debug mode), but you can:
- Contribute to the main project via pull requests. 🙌
- Create a fork to customize the bot for your specific needs. 🍴
We welcome community suggestions and improvements!

## Support and Documentation 📚
Documentation is not yet available, but you can reach out to the author for assistance:
- **Discord**: @b1twalker
- **Email**: meb1twalker@proton.me  
We encourage the community to contribute to creating documentation and guides.

## License 📜
This project is licensed under the MIT License. For more details, please refer to LICENSE file

## Contributing 🤝
Contributions are welcome via pull requests on GitHub. Feel free to enhance the bot or add new features!  
How to contribute:
- Review the code in `main.py`.
- Add new commands or improve existing ones.

## Contact 📬
- **Discord**: @b1twalker
- **Email**: meb1twalker@proton.me