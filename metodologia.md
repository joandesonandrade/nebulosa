# Metodologia

## Aprendizado de Máquina
### Coleta de dados
Baseado nos artigos referências, os dados coletados devem ser oriundos de tráfego normal. Os tráfego será coletado usando o Pcap(biblioteca para análise de fluxo de redes), todos os dados coletados serão salvos em um arquivo CSV, no caso esses dados com fluxo normal servirá de referência para a IA análisa a anomalia, onde anomania não é exatamente um IDS(detecção de uma intrusão), por esse motivo iremos contar com um classificador que irá tomar a decisão de dropar a conexão com esse cliente. Para treinamento do classificador será salvo um fluxo de dados de ataques conhecidos como: Scanners, Reverse TCP, DDoS. Esses dados servirão para o classificar os ataques.

| Dados | Porcentagem |
|:-----------------------------------------------------------------:|:---------------------------------------:|
| Normal | 80% |
| Maliciosa | 20% |

### Modelos
Baseado nos artigos referências, foi escolhido os melhores modelos para essa tarefa, estão listados na tabela abaixa:

| Nome do modelo | Descrição |
|:-----------------------------:|:---------------------------------------------------------------------------:|
| RNN-LSTM | A LSTM é uma arquitetura de rede neural recorrente (RNN) que “lembra” valores em intervalos arbitrários. A LSTM é bem adequada para classificar, processar e prever séries temporais com intervalos de tempo de duração desconhecida. A insensibilidade relativa ao comprimento do gap dá uma vantagem à LSTM em relação a RNNs tradicionais (também chamadas “vanilla”), Modelos Ocultos de Markov (MOM) e outros métodos de aprendizado de sequências. |
| Naive Bayes | O Naive Bayes é um algoritmo probabilístico simples baseado no teorema de Bayes, este utiliza dados de treino para formar um modelo probabilístico baseado na evidência das features nos dados. Atualmente, o algoritmo se tornou popular na área de Aprendizado de Máquina (Machine Learning) para categorizar textos baseado na frequência das palavras usadas, e assim pode ser usado para identificar se determinado e-mail é um SPAM ou sobre qual assunto se refere determinado texto, por exemplo. |

### Coleta de dados
1. Dados Normais: os dados normais serão coletados através de um software que irá ouvir o tráfego, e salvará tudo em um arquivo CSV, nessa fase o sistema deverá funcionar normalmente, esses dados servirão de referência para a IA.
2. Dados Maliciosos: os dados maliciosos serão coletados em um ambiente controlado no caso uma VM, da mesma forma que o tráfego normal, porém ela servirá para treinar o modelo de classificação de ataque.

### Processamento dos dados
Baseado nos artigos referências, foi escolhidos algumas formas de processamento dos dados coletados:

1. Soma de todos os bytes do payload do pacote, dividido pela porta destino;
2. Tamanho do pacote, dividido pela porta destino;
3. Porta destino;
4. Porta de origem;
5. Protocolo UDP/TCP/ICMP...;
6. Frequência de acesso;
7. Entrada/Saída.

## Interface de Usuário
### Gráfico
O gráfico será desenvolvido em formato Time Line & Area: Framework em javascript disponível no arquivo uteis.md

### API
A API do lado do cliente será desenvolvido usando websocket com o framework em javascript disponível no arquivo uteis.md

### Backend
O software principal irá interceptar o tráfego, trata-lo, e irá submeter o analisador de anomalias, caso alguma anomalia seja encontrada, essa informação será salva em um arquivo de anomalias, essa informação irá passar pelo classificador quando for constado um ataque real, é aplicado regras iptables para bloquear o acesso. E todos os dados serão enviados para o lado do cliente conectado com o socket onde irá exibir os resultados.
