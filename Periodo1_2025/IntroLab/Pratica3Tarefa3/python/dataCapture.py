import serial
import time
import os
import math
from openpyxl import Workbook
import numpy as np

# True se Arduino envia microssegundos, False se envia milissegundos.
microsFromArduino = True # O Arduino modificado envia MICROSSEGUNDOS.

tamanhoPendulo = float(input("Digite o tamanho do pêndulo em metro (e.g. 1.215): "))
L = tamanhoPendulo

# --- Filtro Opcional ---
g_esperado = 9.7864 # Valor aproximado para Rio de Janeiro (baseado na localização atual)
T_teorico_s = 2 * math.pi * math.sqrt(L / g_esperado)
T_teorico_ms = T_teorico_s * 1000
filtro_percentual = 0.10 # Aceita períodos +/- 10% do teórico
limite_inferior_ms = T_teorico_ms * (1 - filtro_percentual)
limite_superior_ms = T_teorico_ms * (1 + filtro_percentual)
print(f"Período Teórico Esperado: {T_teorico_ms:.1f} ms")
print(f"Aceitando períodos entre: {limite_inferior_ms:.1f} ms e {limite_superior_ms:.1f} ms")
usar_filtro = True # Defina como False para não usar o filtro
# --- Fim Filtro ---

COMPort = "COM3" # CONFIRME SUA PORTA COM
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

valores_periodo_ms = [] # Armazena os períodos válidos em milissegundos

# Variáveis para cálculo T = t_n - t_{n-2}
t_centro_anterior_us = 0
t_centro_antepenultimo_us = 0
contador_passagens = 0
i = 2 # Linha inicial da planilha Excel (após cabeçalho)

sheet["A1"] = "Periodo Calculado (ms)"

print("Aguardando dados do Arduino...")

try:
    while True:
        if arduino.in_waiting > 0:
            try:
                data = arduino.readline().decode('utf-8').strip()
                if not data:
                    continue # Ignora linhas vazias

                t_centro_atual_us = int(data) # Lê o tempo central (us)
                contador_passagens += 1

                # Precisa de 3 passagens para calcular o primeiro período
                if contador_passagens >= 3:
                    periodo_us = t_centro_atual_us - t_centro_antepenultimo_us # Calcula T em microssegundos
                    periodo_ms = periodo_us / 1000.0 # Converte para milissegundos

                    # Aplica Filtro (se habilitado)
                    periodo_valido = True
                    if usar_filtro:
                        if not (limite_inferior_ms <= periodo_ms <= limite_superior_ms):
                            print(f"Dado Descartado (fora dos limites): {periodo_ms:.1f} ms")
                            periodo_valido = False

                    if periodo_valido:
                        print(f"Periodo {i-1}: {periodo_ms:.1f} ms")
                        sheet[f"A{i}"] = periodo_ms
                        valores_periodo_ms.append(periodo_ms)
                        i += 1

                # Atualiza histórico para próximo cálculo
                t_centro_antepenultimo_us = t_centro_anterior_us
                t_centro_anterior_us = t_centro_atual_us

            except ValueError:
                print(f"Erro ao converter dado: '{data}'. Linha ignorada.")
            except Exception as e:
                print(f"Ocorreu um erro inesperado ao processar dados: {e}")

        time.sleep(0.01) # Evita uso excessivo de CPU

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")
finally:
    if arduino.is_open:
        arduino.close()
        print("Porta serial fechada.")

# --- Cálculos Estatísticos ---
if len(valores_periodo_ms) > 0:
    average_ms = sum(valores_periodo_ms) / len(valores_periodo_ms)
    standartDeviation_ms = np.std(valores_periodo_ms, ddof=1) if len(valores_periodo_ms) > 1 else 0 # Desvio padrão amostral
    uncertainty_ms = standartDeviation_ms / math.sqrt(len(valores_periodo_ms)) if len(valores_periodo_ms) > 0 else 0 # Incerteza da média
    average_s = average_ms / 1000.0 # Média em segundos para cálculo de g

    # Calcula gravidade
    valorTemp = 4 * (pi**2) * L
    gravity = valorTemp / (average_s**2) if average_s > 0 else 0

    # Calcula incerteza da gravidade (dg = 2 * g * dT / T)
    gravityUncertainty = 2 * gravity * (uncertainty_ms / 1000.0) / average_s if average_s > 0 else 0

    # Exibe resultados
    print("\n--- Resultados ---")
    print(f"Número de períodos válidos: {len(valores_periodo_ms)}")
    print(f"Período Médio: {average_ms:.3f} ms")
    print(f"Desvio Padrão Amostral do Período: {standartDeviation_ms:.3f} ms")
    print(f"Incerteza da Média do Período: ± {uncertainty_ms:.3f} ms")
    print(f"Gravidade Calculada (g): {gravity:.4f} m/s²")
    print(f"Incerteza da Gravidade (dg): ± {gravityUncertainty:.4f} m/s²")

    # Escreve estatísticas na planilha
    sheet["C1"] = "Numero de Amostras"
    sheet["C2"] = len(valores_periodo_ms)
    sheet["D1"] = "Periodo Medio (ms)"
    sheet["D2"] = f"{average_ms:.3f}"
    sheet["E1"] = "Desvio Padrao Amostral (ms)"
    sheet["E2"] = f"{standartDeviation_ms:.3f}"
    sheet["F1"] = "Incerteza Periodo Medio (ms)"
    sheet["F2"] = f"±{uncertainty_ms:.3f}"
    sheet["G1"] = "Gravidade (m/s^2)"
    sheet["G2"] = f"{gravity:.4f}"
    sheet["H1"] = "Incerteza Gravidade (m/s^2)"
    sheet["H2"] = f"±{gravityUncertainty:.4f}"
else:
    print("\nNenhum dado válido foi coletado para calcular as estatísticas.")

# --- Salvar Arquivo Excel ---
save_dir = "./data/"
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