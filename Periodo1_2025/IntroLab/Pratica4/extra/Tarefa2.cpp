#include <Arduino.h>
#include <math.h> // Para log()

float tempo = 0.0; // Mude para float
unsigned long tempoInicial = 0;

double Beta1 = 3288.02; //Sem marcacao
double Beta2 = 3516.02; //Com marcacao

double Ref1 = 9597;
double Ref2 = 8043;

float calcularTemperatura(int valorAnalogico, double B, double ref){
  double voltage_ntc = valorAnalogico * (5.0 / 1023.0);
  double resistance_ntc = (voltage_ntc * 10000.0) / (5.0 - voltage_ntc);

  double T0 = 30.0 + 273.15; // Temperatura de referência (K)
  double temperature = 1.0 / ((log(resistance_ntc / ref) / B) + (1.0 / T0)); // Em Kelvin
  temperature -= 273.15; // Converte para Celsius

  return temperature;
}

void setup() {
  Serial.begin(9600);
  tempoInicial = millis();
}

void loop() {
    
  int analogValue = analogRead(A0);
    
  float temperature1 = calcularTemperatura(analogValue, Beta2, Ref2);
  
  // Faça a divisão por um número de ponto flutuante (1000.0f)
  tempo = (millis() - tempoInicial) / 1000.0f; 
  Serial.print(tempo, 1); // Imprime com 2 casas decimais
  Serial.print(" ");
  Serial.println(temperature1, 2);
  
  delay(500);
}
