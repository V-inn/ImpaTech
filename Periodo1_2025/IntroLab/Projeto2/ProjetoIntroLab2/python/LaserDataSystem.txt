#Nota ao professor: Se for testar este código certifique-se de criar um diretório './data/' para os dados serem armazenados

#O programa da erro se for interrompido sem nenhuma entrada, fato que não se pôs necessário de ser corrigido

import serial
import time
import os
import math
from openpyxl import Workbook

microsOrMillis = True #True for Micros, false for Millis

"""
Valores fora dos valores esperados são dados por erros humanos,
ocasionando dados impossíveis e que não devem ser considerados.

Razões para estes erros são por exemplo errar o segundo laser,
ou bloquear o laser acidentalmente com a mão.
"""

distance = 1 #Distance in meters

filterThreshold = 100 #Value in milliseconds

COMPort = "COM3"
bandwidth = 9600

"""------------------------------------------
------vvvvv-------Não mudar-------vvvvv------
------------------------------------------"""

expectedValue = math.sqrt((2*distance)/9.81)*1000   #Rough estimate of time taken for an object to fall a
                                                    #certain distance at 9.81m/s²

workbook = Workbook()
sheet = workbook.active

arduino = serial.Serial(COMPort, bandwidth)

valores = []
average = 0
standartDeviation = 0
uncertainty = 0

i = 2 #Começa em dois para demarcar cabeçalhos
y = 0

sheet["A1"] = "Tempo"

try:
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            y = float(data)
            if(microsOrMillis):
                y = y/1000
            if(y <= expectedValue+filterThreshold and y >=  expectedValue-filterThreshold):
                print(i-1,y)
                sheet["A"+str(i)] = y
                valores.append(y);

                i += 1
            
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    arduino.close()

for v in valores:
    average = average+v

if len(valores) != 0:
    average = average/len(valores)

for v in valores:
    standartDeviation = (v-average)**2

standartDeviation = math.sqrt(standartDeviation/len(valores))

uncertainty = average/math.sqrt(len(valores))

sheet["C1"] = "Media"
sheet["C2"] = "{:.0f}".format(average)
sheet["D1"] = "Desvio Padrao"
sheet["D2"] = "{:.3f}".format(standartDeviation)
sheet["E1"] = "Gravidade"
sheet["E2"] = "{:.3f}".format((2*distance)/((average/1000)**2))
sheet["F1"] = "Incerteza de tempo"
sheet["F2"] = "±"+"{:.3f}".format(uncertainty)

fileNum = 0
while(os.path.exists("./data/sample" + str(fileNum) + ".xlsx")):
    fileNum+=1
    print("exists");

workbook.save("./data/sample" + str(fileNum) + ".xlsx")
print("created")