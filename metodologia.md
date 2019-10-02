# Metodologia

## Aprendizado de Máquina
### Coleta de dados
Baseado nos artigos referências, os dados coletados devem ser oriundos de tráfego normal. Os tráfego será coletado usando o Pcap(biblioteca para análise de fluxo de redes), todos os dados coletados serão salvos em um arquivo CSV, no caso esses dados com fluxo normal servirá de referência para a IA análisa a anomalia, onde anomania não é exatamente um IDS(detecção de uma intrusão).

| Dados | Porcentagem |
|:------:|:-----------:|
| Normal | 80% |
| Maliciosa | 20% |
