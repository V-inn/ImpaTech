import serial
import time
import os
import math
from openpyxl import Workbook
import numpy as np

COMPort = "COM3"
bandwidth = 9600

pi = math.pi

workbook = Workbook()
sheet = workbook.active

try:
    arduino = serial.Serial(COMPort, bandwidth, timeout=1) # Timeout para não bloquear indefinidamente
    print(f"Conectado a {COMPort}...")
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial {COMPort}: {e}")
    exit()

valores_tempo = []
valores_temperatura = []

i = 2 # Linha inicial da planilha Excel (após cabeçalho)

sheet["A1"] = "Tempo (s)"
sheet["B1"] = "Temperatura (°C)"

print("Aguardando dados do Arduino...")

try:
    while True:
        if arduino.in_waiting > 0:
            try:
                data = arduino.readline().decode('utf-8').strip()
                if not data:
                    continue # Ignora linhas vazias


                data = data.split(" ")

                tempo = float(data[0])
                temperatura = float(data[1])

                print(f"Leitura {i-1}: T: {tempo:.1f} | {temperatura:.2f} °C")
                sheet["A"+str(i)] = tempo
                sheet["B"+str(i)] = temperatura
                valores_tempo.append(tempo)
                valores_temperatura.append(temperatura)
                
                i += 1

            except ValueError:
                print(f"Erro ao converter dado: '{data}'. Linha ignorada.")
            except Exception as e:
                print(f"Ocorreu um erro inesperado ao processar dados: {e}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")
finally:
    if arduino.is_open:
        arduino.close()
        print("Porta serial fechada.")

# --- Salvar Arquivo Excel ---
save_dir = "./data/tarefa2/"
if not os.path.exists(save_dir):
    try:
        os.makedirs(save_dir)
        print(f"Diretório '{save_dir}' criado.")
    except OSError as e:
        print(f"Erro ao criar diretório '{save_dir}': {e}")
        save_dir = "." # Tenta salvar no diretório atual

save_path_template = os.path.join(save_dir, "sample{}.xlsx")

fileNum = 0
while os.path.exists(save_path_template.format(fileNum)):
    fileNum += 1

try:
    save_path = save_path_template.format(fileNum)
    workbook.save(save_path)
    print(f"Arquivo salvo como: {save_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel em {save_path}: {e}")