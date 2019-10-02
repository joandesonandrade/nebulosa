# Metodologia

## Aprendizado de Máquina
### Coleta de dados
Baseado nos artigos referências, os dados coletados devem ser oriundos de tráfego normal. Os tráfego será coletado usando o Pcap(biblioteca para análise de fluxo de redes), todos os dados coletados serão salvos em um arquivo CSV, no caso esses dados com fluxo normal servirá de referência para a IA análisa a anomalia, onde anomania não é exatamente um IDS(detecção de uma intrusão), por esse motivo iremos contar com um classificador que irá tomar a decisão de dropar a conexão com esse cliente. Para treinamento do classificador será salvo um fluxo de dados de ataques conhecidos como: Scanners, Reverse TCP, DDoS. Esses dados servirão para o classificar os ataques.

| Dados | Porcentagem |
|:-----------------------------------------------------------------:|:---------------------------------------:|
| Normal | 80% |
| Maliciosa | 20% |

### Modelos
Baseado nos artigos referências, foi escolhido os melhores modelos para essa tarefa, estão listadas na tabela abaixa.

| Nome do modelo | Descrição |
|:-----------------------------:|:---------------------------------------------------------------------------:|
| RNN-LSTM | A LSTM é uma arquitetura de rede neural recorrente (RNN) que “lembra” valores em intervalos arbitrários. A LSTM é bem adequada para classificar, processar e prever séries temporais com intervalos de tempo de duração desconhecida. A insensibilidade relativa ao comprimento do gap dá uma vantagem à LSTM em relação a RNNs tradicionais (também chamadas “vanilla”), Modelos Ocultos de Markov (MOM) e outros métodos de aprendizado de sequências. |
| Naive Bayes | O Naive Bayes é um algoritmo probabilístico simples baseado no teorema de Bayes, este utiliza dados de treino para formar um modelo probabilístico baseado na evidência das features nos dados. Atualmente, o algoritmo se tornou popular na área de Aprendizado de Máquina (Machine Learning) para categorizar textos baseado na frequência das palavras usadas, e assim pode ser usado para identificar se determinado e-mail é um SPAM ou sobre qual assunto se refere determinado texto, por exemplo. |
