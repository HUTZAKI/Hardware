
from machine import Pin, ADC, I2C,PWM
import time
from time import sleep
import network
import ssd1306
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)

from umqtt.simple import MQTTClient

dic_morse = {'.-':'A', '-...':'B','-.-.':'C','-..':'D',
             '.':'E','..-.':'F','--.':'G','....':'H','..':'I',
             '.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
             '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S',
             '-':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
             '-.--':'Y','--..':'Z','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5',
             '-....':'6','--...':'7','---..':'8','----.':'9','-----':'0','..-..':' '}
reverse_dic_morse = {value: key for key, value in dic_morse.items()}
new_time = 0
old_time = 0
newest_time = 0
oldest_time = 0
buzzer = PWM(Pin(12))
buzzer.duty(0)
RED_GPIO = 42
YELLOW_GPIO = 41
GREEN_GPIO = 40
LDR_GPIO = 4
TOPIC_LIGHT = f'{TOPIC_PREFIX}/light/u1'
TOPIC_LED_RED = f'{TOPIC_PREFIX}/led/red'
TOPIC_LED_YELLOW = f'{TOPIC_PREFIX}/led/yellow'
TOPIC_LED_GREEN = f'{TOPIC_PREFIX}/led/green'
TOPIC_TEXT = f'{TOPIC_PREFIX}/display/text'
TOPIC_SWITCH = f'{TOPIC_PREFIX}/switch'
TOPIC_MOSS = f'{TOPIC_PREFIX}/MOSS'
TOPIC_T_MOSS = f'{TOPIC_PREFIX}/TEXT/MOSS'
TOPIC_OF = f'{TOPIC_PREFIX}/of'
TOPIC_ST_KEY = f'{TOPIC_PREFIX}/skey'
TOPIC_KEY = f'{TOPIC_PREFIX}/key'
TOPIC_O_OF = f'{TOPIC_PREFIX}/out_of'
TOPIC_AD = f'{TOPIC_PREFIX}/ad'
TOPIC_TEST1 = f'{TOPIC_PREFIX}/test1'
TOPIC_TEST2 = f'{TOPIC_PREFIX}/test2'
TOPIC_PAGE = f'{TOPIC_PREFIX}/page'
test = 0
new_ls = []
x = 0
space = 0
keep_text = ''
count = 0
state_of = 0
st_key = 0
key = ''
time_on = 1
text_ad = ''
ls_ad = []
num_ls_ad = []
voice_st = 0
voice_id = 0
state_voice = True
def connect_wifi():
    mac = ':'.join(f'{b:02X}' for b in wifi.config('mac'))
    print(f'WiFi MAC address is {mac}')
    wifi.active(True)
    print(f'Connecting to WiFi {WIFI_SSID}.')
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        print('.', end='')
        time.sleep(0.5)
    print('\nWiFi connected.')




def connect_mqtt():
    print(f'Connecting to MQTT broker at {MQTT_BROKER}.')
    mqtt.connect()
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(TOPIC_LED_RED)
    mqtt.subscribe(TOPIC_AD)
    #mqtt.subscribe(TOPIC_LED_YELLOW)
    mqtt.subscribe(TOPIC_LED_GREEN)
    mqtt.subscribe(TOPIC_TEXT)
    mqtt.subscribe(TOPIC_ST_KEY)
    mqtt.subscribe(TOPIC_KEY)
    mqtt.subscribe(TOPIC_O_OF)
    #mqtt.subscribe(TOPIC_SWITCH)
    mqtt.subscribe(TOPIC_OF)
    mqtt.subscribe(TOPIC_LIGHT)
    print('MQTT broker connected.')




def mqtt_callback(topic, payload):
    global test
    global new_one
    global ls
    global new_ls
    global x
    global space
    global keep_text
    global ls_text
    global dic_morse
    global count
    global state_of
    global st_key
    global key
    global time_on
    global text_ad
    global ls_ad
    global num_ls_ad
    n = 0
    
    if topic.decode() == TOPIC_O_OF:
        time_on = int(payload)
        
    elif topic.decode() == TOPIC_TEXT:
        display.fill(0)
        display.text(payload, 0, 0, 1)
        display.show()
    elif topic.decode() == TOPIC_AD:
        text_ad = str(payload)[2:-1].upper()
        ls_ad = []
        num_ls_ad = []
        for i in range(len(text_ad)):
            try:
                ls_ad.append(reverse_dic_morse[text_ad[i]]+ ' ')
                num_ls_ad.append(len(ls_ad[-1]))
            except KeyError:
                pass
        num_ls_ad[0] += 1
        ls_ad[0] =  ' '+ ls_ad[0]
        #print(ls_ad,num_ls_ad)
        
    elif topic.decode() == TOPIC_LIGHT:
        #display.fill(0)
        #display.text(payload,10,10,1)
        #display.show()
        #print(int(payload))
        if int(payload) == 0:
            if len(new_one) != 0:
                display.fill(0)
                display.text('WELLCOME',25,5,1)
                display.text('_._._._.',25,8,1)
                if new_one == '......':
                    ls_text = ls_text[:-1]
                    new_ls.pop()
                elif new_one == '......-':
                    ls_text = ''
                    new_ls = []
                elif new_one == '......-.':
                    mqtt.publish(TOPIC_T_MOSS, ls_text)
                    display.text('SUCCESS',25,40,1)
                    ls_text = ''
                    new_ls = []
                else:
                    if new_one in dic_morse:
                        if state_of == 0:
                            #print('gg')
                            ls_text += dic_morse[new_one]
                            new_ls.append(new_one)
                        elif state_of == 1:
                            #print('ggez')
                            if st_key < len(key[2:-1]):
                                if key[2:-1][st_key] == dic_morse[new_one]:
                                    st_key += 1
                                    mqtt.publish(TOPIC_ST_KEY,str(st_key))
                            
                    else:
                        display.fill(0)
                    
                #display.text(ls_text,128,35,1)
                #print(count)
                new_one = ''
                space = 0
                display.show()
                
    elif topic.decode() == TOPIC_OF:
        state_of = int(payload)
    
    elif topic.decode() == TOPIC_ST_KEY:
        st_key = int(payload)
    
    elif topic.decode() == TOPIC_KEY:
        key = str(payload)
    
def change_ad():
    global ls_ad
    global buzzer
    global new_time
    global old_time
    global voice_st
    global voice_id
    global num_ls_ad
    global newest_time
    global oldest_time
    global state_voice
    global time_check_1
    #print(ls_ad,voice_st,voice_id)
    #print(ls_ad[voice_st][voice_id])
    #print(new_time)
    if ls_ad[voice_st][voice_id] == '.' and state_voice:
        new_time = time.ticks_ms()
        buzzer.duty_u16(100)
        buzzer.freq(300)
        if new_time - old_time >= 200:
            buzzer.duty(0)
            old_time = new_time
            if voice_id < num_ls_ad[voice_st]-1:
                voice_id += 1
                    
    elif ls_ad[voice_st][voice_id] == '-' and state_voice:
        new_time = time.ticks_ms()
        buzzer.duty_u16(100)
        buzzer.freq(100)
        if new_time - old_time >= 1000:
            buzzer.duty(0)
            old_time = new_time
            if voice_id < num_ls_ad[voice_st]-1:
                voice_id += 1
    elif ls_ad[voice_st][voice_id] == ' ' and voice_id == 0:
        voice_id += 1
    if not (voice_id < num_ls_ad[voice_st]-1):
        new_time = time.ticks_ms()
        if new_time - old_time >= 2000:
            voice_st += 1
            if voice_st < len(ls_ad):
                voice_id = 0
                old_time = new_time
            else:
                time_check_1 = 1
                ls_ad = []
                voice_id = 0
                voice_st = 0
            state_voice = True
        else:
            state_voice = False
            
        
    


############
# setup
############
ldr = ADC(Pin(LDR_GPIO), atten=ADC.ATTN_11DB)
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

connect_wifi()
connect_mqtt()
last_publish = 0

i2c = I2C(sda=Pin(48), scl=Pin(47))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
sw = Pin(2, Pin.IN, Pin.PULL_UP)
sw_on = False
new_one = ''
ls = []
ls_text = ''
num = 0
time_check_1 = 1
state_ldr = True
############
# loop
############
while True:
    mqtt.check_msg()
    display.fill(0)
    display.text('WELLCOME',25,5,1)
    display.text('_._._._.',25,8,1)
    display.text(new_one,1,20,1)
    level = 100 - int(ldr.read()*100/4095)
    switch = abs(sw.value() - 1)
    #mqtt.publish(TOPIC_LIGHT, str(level))
    print(level)    
                    
    if state_of == 0:
        display.text(ls_text,count,35,1)
        if count == -5*len(ls_text):
            count = 128
        else:
            count -= 1
        #print(count)
    elif state_of == 1:
        #print(key[2:-1],st_key)
        if st_key < len(key[2:-1]):
            if st_key%2 == 1 and not time_on:
                buzzer.duty_u16(500)
                buzzer.freq(100)
                display.text(key[2:-1][st_key],50,35,1)
            else:
                buzzer.duty(0)
        else:
            buzzer.duty(0)
            mqtt.publish(TOPIC_TEST1, str(1))
            mqtt.publish(TOPIC_TEST2,str(1))
            mqtt.publish(TOPIC_PAGE,str(2))
    #if level == 0:
        #ls.append(new_one)
        #new_one = ''
    
    if switch == 1:
        num += switch
    elif switch == 0:
        if num > 0 and num < 5:
            display.text('.',120,20,1)
            display.show()
            new_one += '.'
            space += 1
        elif num >= 5:
            display.text('_',120,20,1)
            display.show()
            new_one += '-'
            space += 1
        num = 0
    if len(ls_ad) != 0:
        change_ad()
        if time_check_1 == 1:
            old_time = time.ticks_ms()
            time_check_1 = 0
    #print(level)
    if level == 0 and state_ldr:
        if len(new_one) != 0:
            display.fill(0)
            display.text('WELLCOME',25,5,1)
            display.text('_._._._.',25,8,1)
            if new_one == '......':
                ls_text = ls_text[:-1]
                new_ls.pop()
            elif new_one == '......-':
                ls_text = ''
                new_ls = []
            elif new_one == '......-.':
                mqtt.publish(TOPIC_T_MOSS, ls_text)
                display.text('SUCCESS',25,40,1)
                ls_text = ''
                new_ls = []
            else:
                if new_one in dic_morse:
                    if state_of == 0:
                        #print('gg')
                        ls_text += dic_morse[new_one]
                        new_ls.append(new_one)
                    elif state_of == 1:
                        #print('ggez')
                        if st_key < len(key[2:-1]):
                            if key[2:-1][st_key] == dic_morse[new_one]:
                                st_key += 1
                                mqtt.publish(TOPIC_ST_KEY,str(st_key))
                            
                else:
                    display.fill(0)
                    
        new_one = ''
        space = 0
        display.show()
        state_ldr = False
        
    elif level != 0:
        state_ldr = True
    display.show()
            






