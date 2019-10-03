# Detecção de anomalias em uma redes utilizando inteligência artificial

Com a evolução acentuada das soluções de comunicação e arquitetura na área de redes de
computadores, em parte devido ao crescimento e importância comercial da Internet, há um natural
aumento da probabilidade de falhas sistêmicas e do crescimento exponencial das atividades
maliciosas. Assim, com o objetivo do controle e administração do uso dos recursos compartilhados,
faz-se necessária uma atividade de monitoramento eficaz das redes de computadores. O
monitoramento de um sistema, em sua essência, visa a identificação de desvios na operação
normal deste e, se possível, definir o agente ou causa de tal desvio, possibilitando assim
sua classificação e atuação corretiva posterior. A este desvio do padrão de operação normal
se denomina anomalia do sistema. Logo, uma anomalia é caracterizada quando temos o
desvio do comportamento padrão histórico de um conjunto de variáveis observáveis do
sistema. O projeto trata-se de um software ouvindo uma rede usando o Pcap (interface de
programação de aplicativos para capturar o tráfego de rede), e um software com modelo de Machine
Learning (aprendizado de máquina) treinado usando dados de ataque reais em um ambiente
controlado, ambos vinculados por uma API que faz a integração entre si. Por fim, na interface do
usuário onde é exibido os resultados dos softwares, um gráfico estilo linha do tempo, Com efeito de
previsão de um ataque o software pode tomar a decisão de dar drop na conexão, ou até mesmo
bloquear o acesso.

### Instalar dependências
python>=3.6

Execute o comando abaixo para instalar as bibliotecas necessárias.

`pip3 install -r requeriments.txt`
