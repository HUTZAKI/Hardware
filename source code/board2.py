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
import random

from umqtt.simple import MQTTClient


dic_morse = {'.-':'A', '-...':'B','-.-.':'C','-..':'D',
             '.':'E','..-.':'F','--.':'G','....':'H','..':'I',
             '.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
             '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S',
             '-':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
             '-.--':'Y','--..':'Z','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5',
             '-....':'6','--...':'7','---..':'8','----.':'9','-----':'0','..-..':' '}

RED_GPIO = 42
YELLOW_GPIO = 41
GREEN_GPIO = 40
LDR_GPIO = 4
TOPIC_LIGHT = f'{TOPIC_PREFIX}/light'
TOPIC_LED_RED = f'{TOPIC_PREFIX}/led/red'
TOPIC_TEXT = f'{TOPIC_PREFIX}/display/text'
TOPIC_SWITCH = f'{TOPIC_PREFIX}/switch'
TOPIC_MOSS = f'{TOPIC_PREFIX}/MOSS'
TOPIC_T_MOSS = f'{TOPIC_PREFIX}/TEXT/MOSS'
TOPIC_ST_KEY = f'{TOPIC_PREFIX}/skey'
TOPIC_O_OF = f'{TOPIC_PREFIX}/out_of'
TOPIC_TEST1 = f'{TOPIC_PREFIX}/test1'
TOPIC_TEST2 = f'{TOPIC_PREFIX}/test2'
TOPIC_PAGE = f'{TOPIC_PREFIX}/page'
page = 0
state_key = 0
state = True
sw_page = 0
state2 = True
state3 = True
state4 = True
page2 = 0
state_c = True
num_choice = 2
test1 = 0
test4 = 0
of_set = 0
ls_page = [[('1.Quick chat',(12,15),(8, 10, 105, 18, 1)),('2.Select Mode',(12,30),(8, 25, 115, 18, 1)),('-1-',(50,57))],[('1.love you',(0,0),(100, 4, 15, 2, 1)),('2.Hungry!!',(0,10),(100, 12, 15, 2, 1)),('3.Help me!!',(0,20),(100,22,15,2,1)),('4.Toilet',(0,30),(100,34,15,2,1)),('-2-',(50,57),(45,56,35,20,1))],[('1.sentence',(12,15),(8, 10, 95, 18, 1)),('2.OFSD',(12,30),(8, 25, 55, 18, 1)),('-2-',(50,57),(45,56,35,20,1))] ]
ls_sub_page =[[('I',(10,0),(12, 12, 6, 1)),('You',(25,0),(25,12, 25, 1)),('We',(60,0),(60, 12, 15, 1)),('they',(88,0),(88, 12, 32, 1)),('He',(20,18),(20, 30, 16, 1)),('She',(45,18),(45, 30, 24, 1)),('It',(78,18),(78, 30, 17, 1)),('-3-',(50,57),(45,56,35,20,1))]]
ls_sub_page1 = [[('can',(2,0),(2, 12, 23, 1)),('will',(32,0),(32,12, 28, 1)),('want',(70,0),(70, 12, 30, 1)),('to',(110,0),(110, 12,15 , 1)),('go',(20,18),(20, 30, 16, 1)),('walk',(45,18),(45, 30,30, 1)),('talk',(83,18),(83, 30, 30, 1)),('-4-',(50,57),(45,56,35,20,1))]]
test2 = 0
test3 = 0
slice_ls = ''

test = 0
new_ls = []
x = 0
space = 0
keep_text = ''
count = 0

new_one = ''
ls = []
ls_text = ''
num = 0

key = ''
time_on = 1

vx = ADC(Pin(10))
vy = ADC(Pin(11))
buzzer_1 = PWM(Pin(12))
buzzer_1.duty(0)
sw_j = Pin(9, Pin.IN, Pin.PULL_UP)
vy.atten(ADC.ATTN_11DB)
vx.atten(ADC.ATTN_11DB)
#print(vy,vx)
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
    mqtt.subscribe(TOPIC_TEXT)
    mqtt.subscribe(TOPIC_O_OF)
    mqtt.subscribe(TOPIC_ST_KEY)
    #mqtt.subscribe(TOPIC_SWITCH)
    mqtt.subscribe(TOPIC_LIGHT)
    mqtt.subscribe(TOPIC_O_OF)
    print('MQTT broker connected.')




def mqtt_callback(topic, payload):
    global test
    global test1
    global test2
    global page
    global new_one
    global ls
    global new_ls
    global x
    global space
    global keep_text
    global ls_text
    global dic_morse
    global count
    global state_key
    global key
    global time_on
    if topic.decode() == TOPIC_LED_RED:
        try:
            red.value(int(payload))
        except ValueError:
            pass
    elif topic.decode() == TOPIC_ST_KEY:
        state_key = int(payload)
    
    elif topic.decode() == TOPIC_O_OF:
        time_on = int(payload)
    
    elif topic.decode() == TOPIC_TEST1:
        test1 = int(payload)
    
    elif topic.decode() == TOPIC_TEST2:
        test2 = int(payload)
    
    elif topic.decode() == TOPIC_PAGE:
        page = int(payload)
        
    elif topic.decode() == TOPIC_LIGHT:
        print(int(payload))
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
                    #print('Hello')
                    mqtt.publish(TOPIC_T_MOSS, ls_text)
                    display.text('SUCCESS',25,40,1)
                    ls_text = ''
                    new_ls = []
                else:
                    if new_one in dic_morse:
                        if key[state_key] == dic_morse[new_one]:
                            if state_key < len(key):
                                state_key += 1
                                mqtt.publish(TOPIC_ST_KEY,str(state_key))
                        else:
                            pass      
                        #ls_text += dic_morse[new_one]
                        #new_ls.append(new_one)
                    else:
                        display.fill(0)
                    
                #display.text(ls_text,128,35,1)
                #print(count)
                new_one = ''
                space = 0
                display.show()


def joy_select():
    global test1
    global page
    global page2
    global state3
    global vy
    global vx
    global sw_j
    global state4
    r_vx = vx.read()
    r_vy = vy.read()
    #print(r_vy,state2)
    if r_vy >= 4000 and state3:
        if page2 < num_choice-1:
            page2 = page2 + 1
            #print(page2)
        state3 = False
        
    elif 1700 < r_vy < 3500:
        state3 = True
    
    elif r_vy < 100 and state3:
        if page2 > 0:
            page2 = page2 - 1
        state3 = False
        
    if  sw_j.value() == 0 and state4:
        page = (page + 1)%6
        state4 = False
        
    elif sw_j.value() == 1:
        state4 = True
    
    
def check_page():
    global ls_page
    global page2
    global page
    global ls_sub_page
    global test1
    global num_choice
    global mqtt
    global test2
    global test3
    global test4
    global slice_ls
    global ls_sub_page1
    global of_set
    global key
    
    TOPIC_QUICK = f'{TOPIC_PREFIX}/qc'
    TOPIC_OF = f'{TOPIC_PREFIX}/of'
    TOPIC_KEY = f'{TOPIC_PREFIX}/key'
    display.fill(0)
    if page == 0:
        for i in ls_page[0]:
            display.text(i[0],i[1][0],i[1][1])
        display.rect(ls_page[0][page2][2][0],ls_page[0][page2][2][1],ls_page[0][page2][2][2],ls_page[0][page2][2][3],ls_page[0][page2][2][4])
        test1 = page2
    elif page == 1:
        if test1 == 0:
            num_choice = 5
            for i in ls_page[1]:
                display.text(i[0],i[1][0],i[1][1])
            display.rect(ls_page[1][page2][2][0],ls_page[1][page2][2][1],ls_page[1][page2][2][2],ls_page[1][page2][2][3],ls_page[1][page2][2][4])
            test2 = page2
        elif test1 == 1:
            num_choice = 3
            for i in ls_page[2]:
                display.text(i[0],i[1][0],i[1][1])
            display.rect(ls_page[2][page2][2][0],ls_page[2][page2][2][1],ls_page[2][page2][2][2],ls_page[2][page2][2][3],ls_page[2][page2][2][4])
            test2 = page2
    
    elif page == 2:
        if test1 == 0:
            num_choice = 2
            page2 = 0
            if test2 != 4:
                mqtt.publish(TOPIC_QUICK, ls_page[1][test2][0])
            page = 0
        elif test1 == 1:
            if test2 != 2:
                if test2 == 0:
                    num_choice = 8
                    for i in ls_sub_page[0]:
                        display.text(i[0],i[1][0],i[1][1])
                    if page2 < 7:
                        display.hline(ls_sub_page[0][page2][2][0],ls_sub_page[0][page2][2][1],ls_sub_page[0][page2][2][2],ls_sub_page[0][page2][2][3])
                    elif page2 == 7:
                        display.rect(ls_sub_page[0][page2][2][0],ls_sub_page[0][page2][2][1],ls_sub_page[0][page2][2][2],ls_sub_page[0][page2][2][3],ls_sub_page[0][page2][2][4])
                    test3 = page2
                    #print('ggez')
                    display.text(slice_ls,15,40)
                elif test2 == 1:
                    of_set = 1
                    state_key = 0
                    mqtt.publish(TOPIC_ST_KEY,str(state_key))
                    key = gen_key()
                    mqtt.publish(TOPIC_KEY,key)
                    mqtt.publish(TOPIC_OF, str(of_set))
                    page = 6
                    
                #display.text('ggez',0,0,1)
            elif test2 == 2:
                num_choice = 2
                page2 = 0
                page = 0
                
    elif page == 3:
        if test3 == 7:
            num_choice = 2
            page2 = 0
            page = 0
        elif test3 < 7:
            #print(ls_sub_page[0][test3][0])
            slice_ls += ls_sub_page[0][test3][0] + ' '
            num_choice = 8
            page2 = 0
            page = 4
            
    elif page == 4:
        for i in ls_sub_page1[0]:
            display.text(i[0],i[1][0],i[1][1])
        if page2 < 7:
            display.hline(ls_sub_page1[0][page2][2][0],ls_sub_page1[0][page2][2][1],ls_sub_page1[0][page2][2][2],ls_sub_page1[0][page2][2][3])
        elif page2 == 7:
            display.rect(ls_sub_page1[0][page2][2][0],ls_sub_page1[0][page2][2][1],ls_sub_page1[0][page2][2][2],ls_sub_page1[0][page2][2][3],ls_sub_page1[0][page2][2][4])
        display.text(slice_ls,15,40)
        test4 = page2
    
    elif page == 5:
        if test4 != 7:
            slice_ls += ls_sub_page1[0][test4][0] + ' '
            num_choice = 8
            page2 = 0
            page = 4
        elif test4 == 7:
            mqtt.publish(TOPIC_QUICK, slice_ls)
            slice_ls = ''
            num_choice= 2
            page2 = 0
            page = 0
            
    elif page == 6:
        pass
        
            
        

            
    #print(page2)
    #print(slice_ls)
 #   elif page2 == 2:
 #       display.text('1.Quick chat',12,15,1)
 #       display.text('2.Select Mode',12,30,1)
 #       display.rect(46, 55, 32,50, 1)
 #   display.text('-1-',50,57,1)
    display.show()
    

def level_change():
    global page
    global state
    global state2
    global page2
    global num_choice
    level = 100 - int(ldr.read()*100/4095)
    if level == 0 and state:
        page = (page + 1)%6
        state = False
    elif level >= 3:
        state = True
    
    if sw.value() == 0 and state2:
        page2 = (page2 + 1) % num_choice
        state2 = False
    elif sw.value() == 1:
        state2 = True
    #print(page)
        
def gen_key():
    ls = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    new_str = ''
    number = random.choice(range(5,8))
    for i in range(number):
        new_str += random.choice(ls)
    return new_str
############
# setup
############
red = Pin(RED_GPIO, Pin.OUT)
yellow = Pin(YELLOW_GPIO, Pin.OUT)
green = Pin(GREEN_GPIO, Pin.OUT)
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
last_publish = 0
sw = Pin(2, Pin.IN, Pin.PULL_UP)
sw_on = False

############
# loop
############
while True:
    # check for incoming subscribed topics
    mqtt.check_msg()
    if of_set == 1:
        mqtt.check_msg()
        display.fill(0)
        display.text('WELLCOME',25,5,1)
        display.text('_._._._.',25,8,1)
        display.text(new_one,1,20,1)
        level = 100 - int(ldr.read()*100/4095)
        switch = abs(sw.value() - 1)
        mqtt.publish(TOPIC_LIGHT, str(level))
        #print(key,state_key)
        if state_key < len(key):
            if state_key%2 == 0 and (not time_on):
                buzzer_1.duty_u16(500)
                buzzer_1.freq(100)
                display.text(key[state_key],50,35,1)
            else:
                buzzer_1.duty(0)
                
        else:
            test1 = 1
            test2 = 1
            page = 2
            check_page()
        if count == -5*len(ls_text):
            count = 128
        else:
            count -= 1
        #print(count)
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
        display.show()
        sleep(0.05)
    else:
        level = 100 - int(ldr.read()*100/4095)
        print(f'Publishing light value: {level}')
        mqtt.publish(TOPIC_LIGHT, str(level))
        check_page()
        level_change()
        joy_select()
        print()
        #print(sw.value())
        #print(slice_ls)



