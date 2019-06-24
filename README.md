# Trabalho de Redes de Computaores para Automação (DAS5314)

## Enunciado

### Transferência de Arquivos entre computadores usando comunicação UDP

Fazer um programa que use a API sockets em linguagem C, Java ou Python. Assuma a existência de duas estações: CLIENTE e SERVIDOR. A estação SERVIDOR começa a executar antes e fica aguardando requisições de clientes. A estação CLIENTE, ao executar, solicita que o SERVIDOR lhe envie um arquivo. SERVIDOR envia o arquivo em pacotes com, no máximo, 1000 bytes de dados. No final, SERVIDOR avisa CLIENTE que o envio está terminado.

Os pacotes enviados na comunicação deverão ter valores de checksum associados. Quem receber o pacote deverá enviar um pacote de ACK ou NAK. No caso de uma estação transmitir um pacote e receber um NAK, o pacote deverá ser retransmitido.

Durante a apresentação do trabalho para o professor é necessário provocar erros de comunicação “artificialmente” para que o protocolo seja testado retransmitindo pacotes.

Cada pacote, portanto, precisará ter um cabeçalho associado. Sugere-se que esse cabeçalho tenha um checksum verificação de erros, número de sequência para a numeração de pacotes, além da informação de ACK ou NAK, ou outros campos de acordo com o protocolo desenvolvido pelo grupo.

Sugere-se que os grupos sejam formados por 2 estudantes ou, no máximo, 3 estudantes. Todos os membros do grupo precisam apresentar o trabalho. Sugere-se que os trabalhos sejam apresentados na semana entre 1 a 5 de julho. Horário a combinar com prof. Montez.

## Referências

Links para ajudar no desenvolvimento do programa.

- [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
- [TCP](https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol)
- [The TFTP Protocol](https://tools.ietf.org/html/rfc1350)
- [TFTP Blocksize Option](https://tools.ietf.org/html/rfc2348)
- [python-udp-filetransfer](https://github.com/codyharrington/python-udp-filetransfer)
- [Pure Python TFTP library](https://github.com/msoulier/tftpy)