#include <Arduino.h>

const int pinoLDR = A0; // pino onde o LDR está conectado
const int pinoPotentiometer = A1;
const int debugLed = 8;

const int minimumInterval =50;

int leitura = 0; // variável para armazenar o valor lido pelo ADC

unsigned long startPass = 0;
unsigned long endPass = 0;

int oldThreshold = 0;
int threshold = 0;

void setup() {
  // Inicia e configura a Serial
  Serial.begin(9600); // 9600bps

  // configura o pino com LDR como entrada
  pinMode(pinoLDR, INPUT); // pino A0
  pinMode(pinoPotentiometer, INPUT);
  pinMode(debugLed, OUTPUT);

  digitalWrite(debugLed, HIGH);

  //Aguarda enquanto não há luminosidade o suficiente
  while (analogRead(pinoLDR) <= analogRead(pinoPotentiometer)){
    delay(1);
  }
}

void loop() {
  // le o valor de tensão no pino do LDR
  leitura = analogRead(pinoLDR);
  threshold = analogRead(pinoPotentiometer);

  leitura = map(leitura, 0, 1023, 0, 255);
  threshold = map(threshold, 0, 1023, 0, 255);

  if (threshold >= oldThreshold + 5 || threshold <= oldThreshold + -5){
    oldThreshold = threshold;
    //Serial.print("Current threshold: ");
    //Serial.println(threshold);
  }

  if (leitura <= threshold) {
    digitalWrite(debugLed, LOW);

    startPass = micros();

    while (analogRead(pinoLDR) <= analogRead(pinoPotentiometer)){}

    digitalWrite(debugLed,HIGH);

    delay(minimumInterval);

    while(analogRead(pinoLDR) > analogRead(pinoPotentiometer)){}

    digitalWrite(debugLed,LOW);
    
    endPass = micros();
    unsigned long timePassed = endPass - startPass;

    //Serial.print("Time interval: ");
    Serial.println(timePassed);

    //Serial.println("Ended");

    while (analogRead(pinoLDR) <= analogRead(pinoPotentiometer)){
      delay(1);
    }

    delay(500);
    digitalWrite(debugLed, HIGH);
  }
}