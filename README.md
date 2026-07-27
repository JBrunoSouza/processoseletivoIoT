# Processo Seletivo – Intensivo Maker | IoT

## Identificação do Candidato

- **Nome:** José Bruno de Souza Alves
- **GitHub:** https://github.com/JBrunoSouza

---

# Visão Geral da Solução

## Objetivo

Desenvolver um sistema embarcado capaz de monitorar o tempo em que uma porta permanece aberta e identificar variações de temperatura, emitindo alertas sempre que os limites configurados forem ultrapassados.

## Funcionamento

O sistema monitora continuamente duas condições:

- Tempo em que a porta permanece aberta;
- Variação da temperatura medida pelo sensor MPU6050.

Caso a porta permaneça aberta por mais de **5 segundos** ou seja detectado um aumento de temperatura superior a **3 °C** em relação ao valor de referência, um alerta é enviado pela interface serial.

## Interação do Usuário

O usuário interage com o sistema através de:

- Um botão, que simula a abertura e o fechamento da porta;
- Alterações na temperatura do sensor MPU6050 durante a simulação no Wokwi.

---

# Arquitetura do Sistema Embarcado

Após a inicialização do ESP32, o firmware configura os pinos de entrada e a comunicação I2C utilizada pelo sensor MPU6050. Em seguida, entra em um laço principal (`while True`) responsável por monitorar continuamente os dispositivos.

O funcionamento do sistema é baseado em variáveis de estado que controlam quando um alerta deve ser emitido ou quando o sistema deve retornar ao estado normal.

Durante cada ciclo do programa são executadas as seguintes etapas:

1. Leitura do estado da porta (botão);
2. Leitura da temperatura atual do MPU6050;
3. Comparação dos valores com os limites definidos;
4. Emissão de alertas quando necessário;
5. Verificação das condições para normalização do sistema.

Para controlar o tempo de forma eficiente, foram utilizadas as funções `time.ticks_ms()` e `time.ticks_diff()`, evitando bloqueios na execução do programa.

---

# Componentes Utilizados

| Componente | Função |
|------------|--------|
| **ESP32 DevKit C v4** | Executa toda a lógica do sistema. |
| **Push Button (GPIO 14)** | Simula a abertura e o fechamento da porta. |
| **MPU6050 (I2C)** | Responsável pela leitura da temperatura utilizada pelo sistema. |

---

# Decisões Técnicas

Durante o desenvolvimento foram adotadas algumas decisões para tornar o código mais organizado e confiável.

### Organização do código

- Separação da leitura de temperatura em uma função específica;
- Utilização de constantes para os limites de tempo e temperatura;
- Uso de variáveis de estado para evitar alertas repetidos.

### Controle de tempo

O controle do tempo foi implementado utilizando `time.ticks_ms()` e `time.ticks_diff()`, permitindo que o sistema continue monitorando todos os sensores sem interromper a execução do programa.

### Tratamento de erros

A leitura do MPU6050 utiliza um bloco `try-except`. Caso ocorra alguma falha de comunicação, o sistema assume um valor padrão de temperatura e continua funcionando normalmente.

### Estabilização do sistema

Foi adicionado um tempo de estabilização de aproximadamente **1 segundo** antes de informar que o sistema voltou ao estado normal. Essa solução evitou mudanças rápidas de estado e melhorou a execução dos testes automatizados.

---

# Resultados Obtidos

O sistema foi capaz de:

- Detectar quando a porta permanece aberta por mais de 5 segundos;
- Detectar aumento de temperatura superior ao limite configurado;
- Emitir os alertas exatamente no formato esperado pelos testes automatizados;
- Retornar ao estado normal quando as condições seguras são restabelecidas;
- Executar corretamente na simulação do Wokwi e nas GitHub Actions.

---

# Comentários Finais

A principal dificuldade encontrada durante o desenvolvimento foi ajustar o comportamento do firmware para atender aos testes automatizados do Wokwi. Inicialmente ocorria um erro de *timeout*, pois o sistema retornava ao estado normal muito rapidamente.

Após analisar o funcionamento da simulação, foi adicionada uma pequena janela de estabilização antes da normalização do sistema. Essa alteração resolveu o problema e tornou o firmware mais confiável.

Este desafio permitiu aplicar na prática conceitos importantes de sistemas embarcados, comunicação I2C, controle por estados e integração contínua utilizando GitHub Actions e Wokwi.