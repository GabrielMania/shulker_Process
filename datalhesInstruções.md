# Mapas Versionados

Todos os mapas versão a versão estão disponíveis no Drive:

[Link para o Google Drive](https://drive.google.com/drive/folders/1Ebdu63KJPf-L2AKmwXlmZI4NaxptC99T?usp=sharing)

## Log de Atualização

Atualmente implementando as instruções e definindo métodos para renderização.

## Lista de Instruções

### CPU

| Instrução | Descrição                                  | check list |
| :-------- | :----------------------------------------- | :------------ |
| `add`     | Adição                                     | ✅            |
| `or`      | Operação OR                                | ✅            |
| `xor`     | Operação XOR                               | ✅            |
| `not`     | Operação NOT                               | ✅            |
| `no-op`   | Nenhuma operação                           | ✅            |
| `sizeC(>,<)` | Comparação de tamanho (maior, menor)     | ✅            |
| `igual(=)`| Igualdade                                  | ✅            |
| `Ttrue`   | Verdadeiro = Verdadeiro                    | ✅            |
| `limp`    | Limpar                                     | ✅            |
| `jump`    | Saltar                                     | ✅            |
| `Dload`   | Carregar dados                             | ✅            |
| `increment` | Incrementar                                | ✅            |
| `stack(save-load)` | Salvar/Carregar da pilha                 | ✅            |
| `jumpC`   | Saltar condicional                         | ✅            |
| `dataLoad` | Carrega dados de um endereço em um registrador para outro registrador | ❌            |
| `dataSave` | Salva dados de um registrador no endereço em outro registrador | ❌            |

### GPU

| Instruções  | Descrição                                       | Check List |
| :---------- | :---------------------------------------------- | :--------- |
| `loadBackground` | Carrega dados do Background e carrega para tela | ✅         |
| `ReloadBackground` | Recarrega o Background apagando os sprites   | ✅         |
| `drawSprite`   | Renderiza um sprite em uma coordenada da tela  | ✅         |
| `drawPixel`    | Pinta o pixel na coordenada na cor informada   | ✅         |

### Descrição