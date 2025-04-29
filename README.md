# shulker_Processor
processador no Minecraft criado por leigos em teoria da computação
![Shulker](https://github.com/user-attachments/assets/8304734a-64c3-4dc3-8cc0-5d405a697192)

### Descrição

Este processador, concebido por entusiastas sem formação em teoria da computação, simula a arquitetura de Von Neumann dentro do Minecraft. Ele emprega um conjunto de instruções RISC (Reduced Instruction Set Computing). A Unidade Lógica Aritmética (ALU) opera com palavras de 16 bits, enquanto o barramento de memória utiliza 32 bits para transferência de dados. A memória implementada possui uma capacidade total de 65KB, utilizando um esquema de endereçamento de 16 bits, o que permite um espaço de endereçamento de 65.536 posições de memória. Cada posição de memória é composta por 2 bytes.

Recomenda-se a seguinte organização da memória para otimizar o uso:

*   **0x0000 - 0x2EE0:** Destinado ao armazenamento do código binário do programa. As instruções devem ser alinhadas em endereços pares.
*   **0x2EE1 - 0x4E20:** Reservado para dados dinâmicos e endereços virtuais utilizados pelos programas em execução.
*   **0x8CA0 - 0x10000:** Designado para dados de renderização, permitindo a manipulação visual dentro do ambiente Minecraft.

**Nota:** Para informações mais detalhadas sobre as instruções suportadas, acesse [Detalhes das Instruções](datalhesInstruções.md).