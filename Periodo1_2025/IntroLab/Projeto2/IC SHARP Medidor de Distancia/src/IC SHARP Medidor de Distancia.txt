#include <Arduino.h>

const int sensorPin = A2;
const int pinoLDR = A0; // pino onde o LDR está conectado
const int pinoPotentiometer = A1;
const int debugLed = 8;

int leitura = 0; // variável para armazenar o valor lido pelo ADC

unsigned long startPass = 0;
unsigned long nowTime = 0;

int oldThreshold = 0;
int threshold = 0;

int sensorValue = 0;
int cmValue = 0;

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(pinoLDR, INPUT); // pino A0
  pinMode(pinoPotentiometer, INPUT);
  pinMode(debugLed, OUTPUT);

  digitalWrite(debugLed, HIGH);

  Serial.begin(9600);
}

void loop() {
  cmValue = 0;

  leitura = analogRead(pinoLDR);
  threshold = analogRead(pinoPotentiometer);

  leitura = map(leitura, 0, 1023, 0, 255);
  threshold = map(threshold, 0, 1023, 0, 255);

  digitalWrite(debugLed, HIGH);

  if ((threshold >= oldThreshold + 5 || threshold <= oldThreshold + -5)){
    oldThreshold = threshold;
  }

  if (leitura <= threshold) {
    startPass = millis();
    digitalWrite(debugLed, LOW);

    while(cmValue < 125){
      sensorValue = analogRead(sensorPin);
      cmValue = 10650.08 * pow(sensorValue,-0.935) - 10;
      
      nowTime = millis();

      Serial.print(cmValue);
      Serial.print("T");
      Serial.println(nowTime - startPass);
      delay(1);
    }

    Serial.println("1000T0");
  }
}