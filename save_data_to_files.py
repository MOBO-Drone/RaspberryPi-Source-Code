import serial
import time
from datetime import datetime
import requests
import json


try:
    arduino = serial.Serial('COM5', baudrate = 115200, timeout = 1)
except:
    print('Please Check Port')

time.sleep(3)

numPoints = 13
dataList = [0]*numPoints
#dataFile = open('dataFile.info','w')

def AskArduino():
    d = arduino.readline().decode().split('\r\n')
    return d[0]
    

def getValues():
    arduino.write(b'g')
    arduinoData = arduino.readline().decode().split('\r\n')
    
    return arduinoData[0]

    
while 1:

    d = AskArduino()

    if (d == 0):
        d = arduino.inWaiting()
    
    if (d == '1'):
        userInput = 'y'

        dataFile = open('dataFile.info','a+')

        if userInput == 'y':
            now = datetime.now()
            t = now.strftime("%d/%m/%Y %H:%M:%S  ")
            dataFile.write(t)
            for i in range (0,numPoints):
                data = getValues()
                dataFile.write(data + '/')
                #data = int(data)
                dataList[i] = data

            print (t)
            print (dataList)

            dataFile.write("\r\n")
            dataFile.close()

            iud = dataList[:1]
            vitesse = dataList[1:2]
            altitude = dataList[2:3]
            longitude = dataList[3:4]
            latitude = dataList[4:5]
            bat_pourcentage = dataList[5:6]
            bat_ontime = dataList[6:7]
            bat_autonomie = dataList[7:8]
            ping = dataList[8:9]
            attention = dataList[9:10]
            gps = dataList[10:11]
            gsm = dataList[11:12]
            signal = dataList[12:13]

            arduinoDone = 1


            if (arduinoDone == 1):

                url = "http://mobo-drone.com/query/dronecom.php"


                data = {
                    'uid': 999,
                    'vitesse': vitesse,
                    'altitude': altitude,
                    'longitude': longitude,
                    'latitude': latitude,
                    'bat_pourcentage': bat_pourcentage,
                    'bat_ontime': bat_ontime,
                    'bat_autonomie': bat_autonomie,
                    'ping': ping,
                    'attention': attention,
                    'gps': gps,
                    'gsm': gsm,
                    'signal': signal
                } 

                r = requests.post(url, data = data)
                text = r.text.encode('utf-8')
                textDec = json.loads(text)

                if (r.status_code == 200):
                    pass
                    name = textDec['nom']
                    group = textDec['groupe']
                    vol = textDec['vol']
                    note = textDec['note']
                    itin_id = textDec['itin_id']
                    dist_sol = textDec['dist_sol']

                    #print (name)
                    #print (group)
                    #print (vol)
                    #print (note)
                    #print (itin_id)
        
    #if userInput == 'n':
        
        #if userInput == 'n':
            #break
