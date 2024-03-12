# Communication Via Morse Vode (CVMC)

<b>Communicate Via Morse Code</b> (CVMC) is a project that helps people who can't see well, those who want to talk but can't, and those who feel uncomfortable in office settings. It helps them communicate with others and feel better by using Morse code. People with vision problems only need to learn Morse code and English. They can still talk to people who speak other languages. We also turned Morse code into a game to help people feel better in offices.

## What can it do?
- &nbsp;Can communicate with others through Morse code.
+ &nbsp;Quick chat system and a system that allows users to compose their own sentences.
- &nbsp;System that helps individuals with office syndrome change their working posture while seated.

## Hardware equipment
+ 2 x ESP32-S3 Devkit:
  - Board 1: Used for sending and receiving data from the Morse code to the IoT system via MQTT broker.
    
  - Board 2: Used for sending data to the IoT system via MQTT broker.
    
+ 2 x LDR: Used for character segmentation.
  
+ OLED Display: Used for visualization.
  
+ Switch: Used for creating Morse code.
  
+ Active Buzzer: Used for sound transmission.

+ PS2 XY Joystick: Used for system control.

## Directories
```md
❖(CVMC)❖
|
├── ⏍ source_code 
|    ├── board1.py       # Main board for getting and posting Morse code
|    └── board2.py       # Board for selecting Quick chat, Sentence, and OFSD mode
|
├── ⏍ Node-red
|    ├── flows1.json     # setting API Gemini Ai and Line notification
|    └── flows2.json     # Creat template chat and timer in OFSD
|
├── README.md            # Detail
|
└── LICENSE              # License
```


