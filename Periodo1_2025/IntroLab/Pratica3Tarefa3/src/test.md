#include <Arduino.h>

const int pinoLDR = A0;      // Usando pino analógico para testar a leitura do LDR
int leitura = 0;             // Variável para armazenar a leitura do LDR
int e = 1;                   // Variável para controlar a mudança de estado (claro/escuro)
unsigned long temp = 0;      // Variável para armazenar o tempo
unsigned long lastTime = 0;  // Variável para armazenar o tempo do último evento (claro/escuro)

int threshhold = 940;

void setup() {
  Serial.begin(9600);       // Inicializa a comunicação serial
  pinMode(pinoLDR, INPUT);  // Configura o pino do LDR como entrada
}

void loop() {
  String resultado = "";
  unsigned long currentTime = millis();  // Captura o tempo atual

  while(e == 1){
    leitura = analogRead(pinoLDR);         // Lê o valor do LDR

    // Verifica se o valor de leitura do LDR está abaixo de 1000 (escuro)
    if (leitura <= threshhold) {
      temp = currentTime - lastTime;
    
      // Calcula o intervalo de tempo desde o último evento
      resultado += String(temp)+"S"; //S serve como divisor

      lastTime = currentTime;  // Atualiza o último tempo registrado
      e = 0;                   // Atualiza o estado para escuro
    }
  }

  currentTime = millis();  // Captura o tempo atual
  while(e == 0){
    leitura = analogRead(pinoLDR);         // Lê o valor do LDR

    // Verifica se o valor de leitura do LDR está acima de 1000 (claro)
    if (leitura > threshhold) {
      temp = currentTime - lastTime;

      resultado += String(temp);

      lastTime = currentTime;  // Atualiza o último tempo registrado
      e = 1;                  // Atualiza o estado para claro
    }
  }

  Serial.println(resultado);
}