#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // Objeto para o BMP280

void setup() {
    pinMode(2, INPUT_PULLUP);
  Serial.begin(9600); // Inicia a comunicação serial
  if (!bmp.begin(0x76)) { // Endereço I2C do BMP280
    Serial.println("Erro: BMP280 não encontrado!");
    while (1);
  }
}

void loop() {
  if (digitalRead(2) == LOW){
    float temp = bmp.readTemperature(); // Temperatura em °C
    float pressao = bmp.readPressure(); // Pressão em Pa

    // Envia os dados no formato CSV: temperatura,pressao,altitude
    Serial.print(temp);
    Serial.print(" ");
    Serial.println(pressao);

    delay(1000); // Aguarda 1 segun
  }
}