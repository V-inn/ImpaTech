#include <Arduino.h>
#include <math.h> // Para log()

const int termistorFrioPin = A1;
const int termistorQuentePin = A0;

const float Vcc = 5.0;
const float Rref_divisor = 10000.0; // Resistor de pull-up de 10k no divisor de tensão

// Parâmetros dos Termistores (R0 e Beta devem ser para a mesma T0!)
// Termistor 1 (lado frio)
const float R0_1 = 9597.0;    // Resistência a 30°C (ou T0 definida)
const float Beta_1 = 3288.02; // Beta do termistor 1

// Termistor 2 (lado quente)
const float R0_2 = 8043.0;    // Resistência a 30°C (ou T0 definida)
const float Beta_2 = 3516.0;  // Beta do termistor 2

// Temperatura de referência T0 (em Kelvin) para os valores de R0
const float T0_Kelvin = 30.0 + 273.15; // 30°C em Kelvin

unsigned long tempoInicial = 0;
float tempo_decorrido = 0.0;
// Função para calcular temperatura usando o modelo Beta
float calcularTemperaturaBeta(int leituraAnalogica, float R0_termistor, float Beta_termistor) {
  float V_ntc = leituraAnalogica * Vcc / 1023.0;

  // Proteção contra valores extremos para evitar divisão por zero ou log de zero/negativo
  if (V_ntc >= Vcc - 0.001) V_ntc = Vcc - 0.001;
  if (V_ntc <= 0.001) V_ntc = 0.001; // Evita log(0)

  float R_ntc = Rref_divisor * V_ntc / (Vcc - V_ntc);

  // Fórmula Steinhart-Hart simplificada (modelo Beta)
  float invT = (1.0 / T0_Kelvin) + (1.0 / Beta_termistor) * log(R_ntc / R0_termistor);
  float T_Kelvin = 1.0 / invT;

  return T_Kelvin - 273.15; // Converte para Celsius
}

void setup() {
  Serial.begin(9600);
  tempoInicial = millis(); // Inicializa o contador de tempo
}

void loop() {
  int leituraFrio = analogRead(termistorFrioPin);
  int leituraQuente = analogRead(termistorQuentePin);

  float tempFrio = calcularTemperaturaBeta(leituraFrio, R0_1, Beta_1);
  float tempQuente = calcularTemperaturaBeta(leituraQuente, R0_2, Beta_2);

  // Calcula o tempo decorrido em segundos com casas decimais
  tempo_decorrido = (millis() - tempoInicial) / 1000.0f;

  // Saída no formato "tempo temperatura_frio temperatura_quente"
  Serial.print(tempo_decorrido, 1); // Tempo com 1 casa decimal
  Serial.print(" ");
  Serial.print(tempFrio, 2); // Temperatura Frio com 2 casas decimais
  Serial.print(" ");
  Serial.println(tempQuente, 2); // Temperatura Quente com 2 casas decimais

  delay(500); // Intervalo de 500ms
}