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

## Library
- ssd1306 for display OLED [`ssd1306`](https://github.com/micropython/micropython-esp32/blob/esp32/drivers/display/ssd1306.py)

## Directories
```md
❖(CVMC)❖
|
├── ⏍ source_code 
|    ├── board1.py       # Main board for getting and posting Morse code
|    └── board2.py       # Board for selecting Quick chat, Sentence, and OFSD mode
|
├── ⏍ Node-red
|    ├── flows1.json     # Setting API Gemini Ai and Line notification
|    └── flows2.json     # Creat template chat and timer in OFSD
|
├── ⏍ configure
|    └── config.h        # Connected to MQTT broker
|
├── README.md            # Detail
|
└── LICENSE              # License
```
## Configuration

- Node-red
    - Flows1
      - Get the API key from Gemini
      - Get API line notification from [`API-Line_noti`](https://notify-bot.line.me/doc/en/)
      - `npm install node-red-contrib-google-translate-fixed` for translate node
        
    - Flow2
      - set a new file for storing a log chat and updating the status of table OFSD in the server
      - `npm install node-red-contrib-countdown` for count time in OFSD mode

- Board1
    - set config.h
    - connected buzzer
  
- Board2
    - set config.h
    - connected buzzer and joystick

## Developed by

&nbsp;&nbsp;<b>Project members</b>\
&nbsp;&nbsp;&nbsp;1.) &nbsp;Sirapat Panmoon - 6610502226\
&nbsp;&nbsp;&nbsp;2.) &nbsp;
