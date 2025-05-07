#include <Arduino.h>

const int pinoLDR = A0;       // Pino analógico para o LDR
int leituraLDR = 0;
int threshold = 940; // AJUSTE SE NECESSÁRIO (valor que separa claro/escuro)
bool estadoEscuroAtual = false;
bool estadoEscuroAnterior = false;

unsigned long t_inicio_bloqueio_atual = 0; // Tempo (us) do início do bloqueio atual

void setup() {
  Serial.begin(9600);
  pinMode(pinoLDR, INPUT);
  Serial.println("Arduino pronto para enviar t_centro (us)"); // Informa o que será enviado

  // Leitura inicial para definir o estado anterior
  leituraLDR = analogRead(pinoLDR);
  estadoEscuroAnterior = (leituraLDR <= threshold);
}

void loop() {
  unsigned long tempoAtual_us = micros();
  leituraLDR = analogRead(pinoLDR);
  estadoEscuroAtual = (leituraLDR <= threshold);

  // Detecção de Mudança de Estado
  if (estadoEscuroAtual != estadoEscuroAnterior) {
    if (estadoEscuroAtual == true) {
      // Transição: Claro -> Escuro (Início do bloqueio)
      t_inicio_bloqueio_atual = tempoAtual_us;
    } else {
      // Transição: Escuro -> Claro (Fim do bloqueio)
      if (t_inicio_bloqueio_atual > 0) {
        unsigned long t_fim_bloqueio_atual = tempoAtual_us;
        // Calcula e envia o tempo central da passagem (em us)
        unsigned long t_centro_us = t_inicio_bloqueio_atual + (t_fim_bloqueio_atual - t_inicio_bloqueio_atual) / 2;
        Serial.println(t_centro_us);
        t_inicio_bloqueio_atual = 0; // Reseta para próxima detecção
      }
    }
    estadoEscuroAnterior = estadoEscuroAtual; // Atualiza estado anterior
  }
}

/* --- NOTA ---
 * Este código envia o tempo central (t_centro em microssegundos) de cada passagem.
 * O script Python deve ler este valor e calcular o período como T = t_centro[n] - t_centro[n-2].
 */