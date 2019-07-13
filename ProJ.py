from _thread import start_new_thread as thread
import json,network,urequests
from machine import Pin,ADC,DAC,PWM
from time import sleep

PIR = Pin(19,Pin.IN)
LED = Pin(5,Pin.OUT)
R = Pin(23,Pin.OUT)
G = Pin(22,Pin.OUT)
B = Pin(2,Pin.OUT)
Laser = Pin(21,Pin.OUT)
LDR = Pin(4,Pin.IN)
HS = Pin(25,Pin.IN)

Buzzer = PWM(Pin(18))
Buzzer.freq(10)
Buzzer.deinit()


statEnt = 'Out'
statDetect = 'Detect'
statHit = 0
count = 0


ssid='exceed16_8'
pwd='12345678'
station=network.WLAN(network.STA_IF)
station.active(True)




def testPIR():
  global PIR,LED
  while(1):
    LED.value(PIR.value())

def testIR():
  global LDR,Laser
  Laser.value(1)
  while(1):
    print(LDR.value())
    sleep(0.5)

def TestHS():
  global HS
  while(1):
    print(HS.value())
    sleep(0.05)

 
def isEntrance():
  global statEnt
  global count
  Laser.value(1)
  while(1):
    #print(LDR.value())
    if LDR.value() == 1:
      count+=1
    if count % 2 == 1 :
      statEnt = 'In'
      print('now In')
      sleep(1)
    else:
      statEnt = 'Out'
      print('now Out')
      sleep(1)
  
def isDetect():
  global statDetect
  while(1):
    LED.value(PIR.value())
    if PIR.value()==1:

      statDetect='Detect'
      sleep(1)
    else:
      statDetect='nonDetect'
 
def isHit():
  global statHit
  while(1):
    
    if HS.value()==0:
      statHit = int(statHit) + 1
      print('HIT',statHit)
      sleep(1)

def ToNetwork():
  global statDetect,statEnt,statHit,data,r,r1
  status = 'Basic'
  alertStatus = 'Off'
  startEnt = 0
  startDetect = 0
  url = 'https://exceed.superposition.pknn.dev/data/eight'
  data = {'statEnt':statEnt,'statDetect':statDetect,'statHit':statHit,'status':status,'alertStatus':alertStatus,'startEnt':startEnt,'startDetect':startDetect}
  headers = {'content-type':'application/json'}
  R = Pin(23,Pin.OUT)
  G = Pin(22,Pin.OUT)
  B = Pin(2,Pin.OUT)
  while(1):
    
    while not station.isconnected():
      station.connect(ssid,pwd)
      print('Connecting ...')
      sleep(1)
      if station.isconnected():
        print('Connected')
    
    r1 = urequests.get(url).json()
    status = r1['status']
    alertStatus = r1['alertStatus']
    startEnt = r1['startEnt']
    startDetect = r1['startDetect']
    #statHit = int(r1['statHit'])
    if station.isconnected():
      if status == 'Alert':
        for i in range(5):
          
          Buzzer = PWM(Pin(18))
          Buzzer.freq(10)
          R.value(1)
          G.value(0)
          B.value(0)
          sleep(0.5)
          Buzzer.deinit()
        
          Buzzer = PWM(Pin(18))
          Buzzer.freq(20)
          R.value(0)
          G.value(0)
          B.value(1)
          sleep(0.5)
          Buzzer.deinit()
        statHit = 0
      
      r1 = urequests.get(url).json()
      #statHit = int(r1['statHit'])
      status = r1['status']
      if status == 'Basic':
        R.value(0)
        G.value(0)
        B.value(0)
    
    r1 = urequests.get(url).json()
    status = r1['status']
    #statHit = int(r1['statHit'])
    data = {'statEnt':statEnt,'statDetect':statDetect,'statHit':statHit,'status':status,'alertStatus':alertStatus,'startEnt':startEnt,'startDetect':startDetect}
    js = json.dumps({'data':data})
    r = urequests.post(url,data=js,headers=headers)
    results = r.json()
    print(results)
    sleep(0.5)


thread(isDetect,())
thread(isEntrance,())
thread(isHit,())
thread(ToNetwork,())









