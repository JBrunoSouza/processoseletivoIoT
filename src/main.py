import time
from machine import Pin, I2C


btn1 = Pin(14, Pin.IN, Pin.PULL_UP)

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Parâmetros de Limite
LIMITE_TEMPO_X = 5000     
LIMITE_VARIACAO_Y = 3.0   

# Variáveis de Controle de Estado
tempo_abertura_porta = 0
porta_estava_aberta = False
alarme_porta_ativo = False
alarme_termico_ativo = False

temperatura_referencia = 20.0  
referencia_capturada = False

def ler_temperatura_mpu6050():

    try:
        # Endereço I2C padrão do MPU6050 é 0x68
        # Registrador de temperatura interna começa em 0x41 (2 bytes)
        dados = i2c.readfrom_mem(0x68, 0x41, 2)
        valor_bruto = int.from_data(dados, 'big' if hasattr(int, 'from_data') else 'big') 

        temp = (int.from_bytes(dados, 'big') / 340.0) + 36.53
        return temp
    except Exception:
        return 20.0

def main():
    global tempo_abertura_porta, porta_estava_aberta, alarme_porta_ativo, alarme_termico_ativo, temperatura_referencia, referencia_capturada

    
    print("Sistema de Monitoramento Inicializado")

    while True:
        # Fechado = 1,Aberto = 0
        estado_hardware = btn1.value()
        status_porta = 1 if estado_hardware == 0 else 0

        temperatura_atual = ler_temperatura_mpu6050()

        if status_porta == 1:
            if not referencia_capturada:
                temperatura_referencia = temperatura_atual
                referencia_capturada = True
        
     
        tempo_atual_ms = time.ticks_ms()
        
        if status_porta == 0:  # Porta Aberta
            if not porta_estava_aberta:
                tempo_abertura_porta = tempo_atual_ms
                porta_estava_aberta = True
            else:
                if not alarme_porta_ativo and (time.ticks_diff(tempo_atual_ms, tempo_abertura_porta) >= LIMITE_TEMPO_X):
                    print("ALERTA: Porta aberta por muito tempo!")
                    alarme_porta_ativo = True
        else:  # Porta Fechada
            porta_estava_aberta = False

        if referencia_capturada:
            delta_t = temperatura_atual - temperatura_referencia
            if delta_t >= LIMITE_VARIACAO_Y and not alarme_termico_ativo:
                print("ALERTA: Degradacao termica detectada!")
                alarme_termico_ativo = True

       
        delta_t_atual = temperatura_atual - temperatura_referencia if referencia_capturada else 0.0
        condicao_porta_segura = (status_porta == 1)
        condicao_termica_segura = (delta_t_atual < LIMITE_VARIACAO_Y)

        if (alarme_porta_ativo or alarme_termico_ativo) and condicao_porta_segura and condicao_termica_segura:
            print("Status: Sistema Normalizado.")
            alarme_porta_ativo = False
            alarme_termico_ativo = False
            referencia_capturada = False  

        # Pequeno atraso não-bloqueante para estabilização do ciclo de varredura
        time.sleep_ms(100)

if __name__ == "__main__":
    main()