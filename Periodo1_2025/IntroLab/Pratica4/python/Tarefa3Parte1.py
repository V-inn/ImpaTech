import pyvisa
import serial
import time
import os
from openpyxl import Workbook

# === Configurações do usuário ===
tensao_v = 12
corrente_a = 2
tempo_segundos = 30
canal = 1

COMPort = "COM3"
bandwidth = 9600

# === Inicia comunicação com o Arduino ===
try:
    arduino = serial.Serial(COMPort, bandwidth, timeout=1)
    print(f"Conectado a {COMPort}...")
    time.sleep(2)  # Dá tempo para a porta estabilizar
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial {COMPort}: {e}")
    exit()

# === Conecta com a fonte via PyVISA ===
rm = pyvisa.ResourceManager()
devices = rm.list_resources()

if not devices:
    raise Exception("Nenhum dispositivo VISA encontrado.")

print("Dispositivos VISA encontrados:")
for i, dev in enumerate(devices):
    print(f"[{i}] {dev}")


dp932u = rm.open_resource(devices[0])
dp932u.timeout = 5000
dp932u.read_termination = '\n'
dp932u.write_termination = '\n'

# Configura canal e ativa saída
dp932u.write(f"INST:NSEL {canal}")
dp932u.write(f"VOLT {tensao_v}")
dp932u.write(f"CURR {corrente_a}")
dp932u.write("OUTP ON")
print("Fonte ligada.")

# === Preparar planilha Excel ===
workbook = Workbook()
sheet = workbook.active
sheet["A1"] = "Tempo (s)"
sheet["B1"] = "Lado Quente (°C)"
sheet["C1"] = "Lado Frio (°C)"
sheet["D1"] = "Tensão Real (V)"
sheet["E1"] = "Corrente Real (A)"
sheet["F1"] = "Potência Real (W)"

valores_tempo = []
valores_temperatura_fria = []
valores_temperatura_quente = []

i = 2  # linha inicial após cabeçalho
print("Aguardando dados do Arduino...")

try:
    while True:
        if arduino.in_waiting > 0:
            try:
                data = arduino.readline().decode('utf-8').strip()
                if not data:
                    continue

                data = data.split(" ")

                tempo = float(data[0])
                temperatura1 = float(data[1])
                temperatura2 = float(data[2])

                # Leitura da fonte
                dp932u.write(f"INST:NSEL {canal}")
                tensao_real = float(dp932u.query("MEAS:VOLT?"))
                corrente_real = float(dp932u.query("MEAS:CURR?"))
                potencia_real = tensao_real * corrente_real

                # Registro
                print(f"Leitura {i-1}: T: {tempo:.2f}s | Quente: {temperatura1:.2f}°C | Frio: {temperatura2:.2f}°C | "
                      f"V: {tensao_real:.2f}V | I: {corrente_real:.2f}A | P: {potencia_real:.2f}W")

                sheet[f"A{i}"] = tempo
                sheet[f"B{i}"] = temperatura1
                sheet[f"C{i}"] = temperatura2
                sheet[f"D{i}"] = tensao_real
                sheet[f"E{i}"] = corrente_real
                sheet[f"F{i}"] = potencia_real

                valores_tempo.append(tempo)
                valores_temperatura_quente.append(temperatura1)
                valores_temperatura_fria.append(temperatura2)

                i += 1

                if tempo >= tempo_segundos:
                    print("Tempo de aquisição atingido.")
                    break

            except ValueError:
                print(f"Erro ao converter dado: '{data}'. Ignorado.")
            except Exception as e:
                print(f"Erro inesperado: {e}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")

finally:
    if arduino.is_open:
        arduino.close()
        print("Porta serial fechada.")

    dp932u.write("OUTP OFF")
    dp932u.close()
    print("Fonte desligada e conexão encerrada.")

    # Salvar Excel
    save_dir = "./data/tarefa3/parte1/"
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
            print(f"Diretório '{save_dir}' criado.")
        except OSError as e:
            print(f"Erro ao criar diretório '{save_dir}': {e}")
            save_dir = "."

    fileNum = 0
    save_path_template = os.path.join(save_dir, "sample{}.xlsx")
    while os.path.exists(save_path_template.format(fileNum)):
        fileNum += 1

    save_path = save_path_template.format(fileNum)
    try:
        workbook.save(save_path)
        print(f"Arquivo salvo como: {save_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
