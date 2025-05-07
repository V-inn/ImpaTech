#Nota ao professor: Se for testar este código certifique-se de criar um diretório './data/' para os dados serem armazenados

#O programa da erro se for interrompido sem nenhuma entrada, fato que não se pôs necessário de ser corrigido

import serial
import time
import os
import math
from openpyxl import Workbook

microsOrMillis = False #True for Micros, false for Millis

tamanhoPendulo = float(input("Digite o tamanho do pêndulo em metro (e.g. 1.215): "))

"""
Valores fora dos valores esperados são dados por erros humanos,
ocasionando dados impossíveis e que não devem ser considerados.

Razões para estes erros são por exemplo errar o segundo laser,
ou bloquear o laser acidentalmente com a mão.
"""

#filterThreshold = 100 #Value in milliseconds

COMPort = "COM3"
bandwidth = 9600

"""------------------------------------------
------vvvvv-------Não mudar-------vvvvv------
------------------------------------------"""

pi = 3.14159

workbook = Workbook()
sheet = workbook.active

arduino = serial.Serial(COMPort, bandwidth)

valores = []
average = 0
standartDeviation = 0
uncertainty = 0
gravidade = 0

i = 2 #Começa em dois para demarcar cabeçalhos
periodo = 0
periodoAnterior = 0

ida = True

firstTime = True

sheet["A1"] = "Tempo"

try:
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            data = list(map(int,data.split("S")))

            periodo = data[0]/2 + data[1] #Calcula metade do valor do sensor obstruído com o periodo de meia oscilação

            if(microsOrMillis):
                periodo = periodo/1000

            #if(y <= expectedValue+filterThreshold and y >=  expectedValue-filterThreshold):

            if(not firstTime):
                if(ida == False):
                    print(i-1,periodo+periodoAnterior)
                    sheet["A"+str(i)] = periodo+periodoAnterior
                    valores.append(periodo+periodoAnterior);
                    ida = True

                    i += 1
                else:
                    periodoAnterior = periodo
                    ida = False
            else:
                firstTime = False
            
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

valorTemp = 4*(pi**2)*tamanhoPendulo
gravity = valorTemp/((average/1000)**2)
gravityUncertainty = gravity - (valorTemp/(((average+uncertainty)/1000)**2))

sheet["C1"] = "Media"
sheet["C2"] = "{:.0f}".format(average)
sheet["D1"] = "Desvio Padrao"
sheet["D2"] = "{:.3f}".format(standartDeviation)
sheet["E1"] = "Incerteza de tempo"
sheet["E2"] = "±"+"{:.3f}".format(uncertainty)
sheet["F1"] = "Gravidade"
sheet["F2"] = "{:.3f}".format(gravity)
sheet["G1"] = "Incerteza Gravidade"
sheet["G2"] = "±"+"{:.3f}".format(gravityUncertainty)



fileNum = 0
while(os.path.exists("./data/sample" + str(fileNum) + ".xlsx")):
    fileNum+=1
    print("exists");

workbook.save("./data/sample" + str(fileNum) + ".xlsx")
print("created")