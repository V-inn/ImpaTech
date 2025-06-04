#include <Arduino.h>

// Definições do pino e do resistor fixo
const int NTC_PIN = A0;
const float REFERENCE_RESISTOR = 10000.0; // Valor do resistor fixo em Ohms (ex: 10k)
const float SUPPLY_VOLTAGE = 5.0;      // Tensão de alimentação do Arduino/ESP32 (normalmente 5.0V ou 3.3V)

void setup() {
  Serial.begin(9600);
  Serial.println("Leitura de Resistencia do Termistor NTC");
  Serial.println("---------------------------------------");
}

void loop() {
  // Leitura do valor analógico do pino A3
  int analogValue = analogRead(NTC_PIN);

  // Converte o valor analógico (0-1023) para tensão (0-5V)
  double voltage_ntc = analogValue * (SUPPLY_VOLTAGE / 1023.0);

  // Calcula a resistência do NTC usando a fórmula do divisor de tensão
  // Esta fórmula é para a configuração com o NTC na parte inferior do divisor
  double resistance_ntc = (voltage_ntc * REFERENCE_RESISTOR) / (SUPPLY_VOLTAGE - voltage_ntc);

  // Exibe os valores no Monitor Serial
  Serial.print("Analog Read: ");
  Serial.print(analogValue);
  Serial.print(" | Tensao no NTC (V): ");
  Serial.print(voltage_ntc, 3); // 3 casas decimais
  Serial.print(" | Resistencia do NTC (Ohms): ");
  Serial.println(resistance_ntc, 2); // 2 casas decimais

  Serial.println("-----------------------");
  delay(1000); // Espera 1 segundo antes da próxima leitura
}