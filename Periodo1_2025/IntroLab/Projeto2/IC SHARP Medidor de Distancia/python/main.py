#Nota ao professor: Se você for testar este código, certifique-se de criar um diretório './data/'

import serial
import os
from openpyxl import Workbook

filterThreshold = 100 #Value in milliseconds
startingValue = 20

alturaCaixa = 2

COMPort = "COM3"
bandwidth = 9600

workbook = Workbook()
sheet = workbook.active

arduino = serial.Serial(COMPort, bandwidth)

def number_to_letters(n):
    result = ""
    while n > 0:
        n -= 1 
        result = chr(n % 26 + 65) + result
        n //= 26
    return result


i = 2 #Começa em dois para demarcar cabeçalhos
j = 1
y = 0

initialTime = 0
finalTime = 0

try:
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            data = data.split("T")
            y = float(data[0])-startingValue
            curTime = float(data[1])

            letter1 = number_to_letters(j)
            letter2 = number_to_letters(j+1)
            resultColumn = number_to_letters(j+2)

            if(y == float(1000-startingValue)):
                sheet[letter1+"1"] = "Tempo(ms)"
                sheet[letter2+"1"] = "Distancia(cm)"
                sheet[resultColumn+"1"] = "Tempo de 0 a 100"
                sheet[resultColumn+"2"] = finalTime-initialTime

                j += 3
                i = 1
                finalTime = 0
                initialTime = 0
                print(((j-1)/3)+1)
            else:
                if(y > 0-alturaCaixa and initialTime == 0):
                    initialTime = curTime
                elif (y > 100 and finalTime == 0):
                    finalTime = curTime

                sheet[letter1+str(i)] = float(data[1])
                sheet[letter2+str(i)] = y
                print(data)

            i += 1
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    arduino.close()

fileNum = 0
while(os.path.exists("./data/sample" + str(fileNum) + ".xlsx")):
    fileNum+=1
    print("exists");

workbook.save("./data/sample" + str(fileNum) + ".xlsx")
print("created")