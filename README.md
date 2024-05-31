# merlin_voice_assistant

A virtual voice assistant that listens to your voice commands and responds interactively.

Merlin is a voice-activated assistant powered by OpenAI's GPT-3.5 model. It listens for a wake word, captures the user's voice query, and then fetches a response from GPT-3.5, which it then speaks out loud.

## Features

- **Wake Word Detection**: Uses Picovoice's Porcupine for efficient wake word detection.
- **Voice Activity Detection**: Uses Picovoice's Cobra to detect when the user starts and stops speaking.
- **Speech-to-Text**: Converts the user's voice query into text.
- **Text-to-Speech**: Converts GPT-3.5's text response into speech using Google's Text-to-Speech.

## Prerequisites

- Python 3.x
- OpenAI API Key
- Picovoice Access Key (https://picovoice.ai/)

## Installation

1. Clone the repository:

```bash
cd <repository-directory>
```

```bash
git clone https://github.com/eliastsoukatos/merlin_voice_assistant.git
```

2. Install Python version 3.10.* if you don't have it:

```bash
# Update your system
sudo apt update && sudo apt upgrade -y

# Install required dependencies
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# Download Python 3.10 tarball
wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz

# Extract the tarball
tar -xf Python-3.10.*.tgz

# Navigate into the extracted directory
cd Python-3.10.*/

# Configure and optimize
./configure --prefix=/usr/local --enable-optimizations --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"

# Build Python
make -j$(nproc)
sudo make altinstall

# Verify installation
python3.10 --version
```

3. Install the required packages:

If you’re using Linux (specifically Debian/Ubuntu), you can install the Python 3 bindings for PyAudio with the following command:

```bash
sudo apt update && sudo apt install python3-pyaudio
```

Additionally, make sure you have the PortAudio library and FFMPEG installed. On Debian/Ubuntu, you can do this with:

```bash
sudo apt install portaudio19-dev ffmpeg

```

In Windows you can run PowerShell with Administrator Privileges and run using Chocolatery:

```bash

choco install ffmpeg


```

```

4. Create a new Python 3.10 environment:

```bash
python3.10 -m venv myenv
```

5. Activate the enviroment:

```bash
source myenv/bin/activate
```

6. Upgrade pip if necessary:

```bash
pip install --upgrade pip
```

7. Now install the requierements for the repo:

```bash
pip install -r requirements.txt
```

## Usage

1. Set your OpenAI API key, Picovoice Access Key, Wake Word and GTP model in a **.env** file inside the root folder:

```python
OPENAI_API_KEY='sk-proj-................'
PV_ACCESS_KEY='A.........................'
WAKE_WORD_FILE='Merlin_en_windows_v3_0_0.ppn'
GPT_MODEL='gpt-4o'
```

2. Run the script:

```bash
python3 main.py
```

3. Say the wake word "Merlin" to activate the assistant and then speak your query.


## ISSUES ON RASPBERRY PI 5:

1. Fat32 / could not mount during RPI-Imager writing. This is due to USB auto-suspend. 
Follow the answer from @mariuszbrz at https://github.com/raspberrypi/rpi-imager/issues/505

2. Because of 5A required for USB, the first-time booting requires another press the RESET/POWER button again 
## Customization

- **Wake Word**: You can change the wake word by replacing the `Merlin_en_linux_v2_2_0.ppn` file with another Porcupine keyword file and updating the `keyword_path` in the `wake_word()` function.

- **Prompts**: Customize the assistant's prompts by modifying the `prompt` list.

- **Assistant's Personality**: Adjust the assistant's behavior by changing the system message in the `chat_log`.

## Troubleshooting

If you encounter any API-related errors, ensure that:

- Your OpenAI API key is valid and has not exceeded its rate limits.
- Your Picovoice Access Key is valid.
- You have a stable internet connection.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
