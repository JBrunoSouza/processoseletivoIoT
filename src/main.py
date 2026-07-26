import machine
import time

print("Sistema de Monitoramento Inicializado")


# Fechado = 1,Aberto = 0
btn1 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# Variáveis de controle de tempo para a porta aberta
tempo_abertura_inicio = 0
porta_estava_aberta = False
LIMITE_TEMPO_X = 5000

while True:
    agora = time.ticks_ms()
    estado_porta = btn1.value()

    # Lógica de Tempo de Porta Aberta
    if estado_porta == 0:  # Porta aberta
        if not porta_estava_aberta:
            tempo_abertura_inicio = agora
            porta_estava_aberta = True
        else:
            if time.ticks_diff(agora, tempo_abertura_inicio) >= LIMITE_TEMPO_X:
                print("ALERTA: Porta aberta por muito tempo!")
               
                tempo_abertura_inicio = agora
    else:
        porta_estava_aberta = False

    # Pausa não bloqueante para estabilizar o ciclo do CPU
    time.sleep(0.1)