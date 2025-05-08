# Mapas Versionados

Todos os mapas versão a versão estão disponíveis no Drive:

[Link para o Google Drive](https://drive.google.com/drive/folders/1Ebdu63KJPf-L2AKmwXlmZI4NaxptC99T?usp=sharing)

## Log de Atualização

Atualmente implementando as instruções e definindo métodos para renderização.

## Lista de Instruções

### CPU

| Instrução | Mnemônico | Sintaxe | Descrição | check list |
| :-------- | :-------- | :------ | :-------- | :--------- |
| `add`     | ADD       | `add reg1,reg2,reg3` | Soma reg2 com reg3, resultado em reg1 | ✅ |
| `or`      | OR        | `or reg1,reg2,reg3`  | OR lógico entre reg2 e reg3 | ✅ |
| `xor`     | XOR       | `xor reg1,reg2,reg3` | XOR lógico entre reg2 e reg3 | ✅ |
| `not`     | NOT       | `not reg1`       | NOT lógico de reg2 | ✅ |
| `no-op`   | NOP       | `nop`                  | Nenhuma operação | ✅ |
| `sizeC(>,<)` | SIZEC  | `sizeC reg1,reg2,reg3`    | Comparação de tamanho (maior, menor) | ✅ |
| `igual(=)`| IGUAL     | `igual reg1,reg2,reg3`     | Compara igualdade | ✅ |
| `Ttrue`   | TTRUE     | `Ttrue reg1,reg2`          | Testa se reg1 é verdadeiro | ✅ |
| `limp`    | LIMP      | `limp reg1`           | Limpa o registrador | ✅ |
| `jump`    | JUMP      | `jump reg1`           | Salta para endereço em reg1 | ✅ |
| `Dload`   | DLOAD     | `dload reg1`    | Carrega dados de reg2 para reg1 | ✅ |
| `increment` | INC      | `inc reg1`            | Incrementa reg1 | ✅ |
| `stack(save-load)` | PUSH/POP | `push reg1` ou `pop reg1` | Salva/Carrega da pilha | ✅ |
| `jumpC`   | JUMPC     | `jumpC reg1,reg2`          | Salto condicional para endereço em reg1 | ✅ |
| `dataLoad` | read    | `read reg1,reg2`    | Carrega dados de um endereço em reg2 para reg1 | ❌ |
| `dataSave` | write    | `write reg1,reg2`    | Salva dados de reg1 no endereço em reg2 | ❌ |

### GPU

| Instruções | Mnemônico | Sintaxe | Descrição | Check List |
| :--------- | :-------- | :------ | :-------- | :--------- |
| `loadBackground` | LDBG | `drawBg reg1` | Carrega dados do Background para tela | ✅ |
| `ReloadBackground` | RLDBG | `RdrawBg` | Recarrega o Background apagando sprites | ✅ |
| `drawSprite` | DRWS | `drawS reg1` | Renderiza sprite na coordenada da tela | ✅ |
| `drawPixel` | DRWP | `drawP reg1` | Pinta pixel na coordenada especificada | ✅ |

### Exemplos de Uso

```assembly
# Exemplo de soma
add reg1, reg2, reg3    # reg1 = reg2 + reg3

# Exemplo de comparação
sizeC reg1,reg2,reg3        # Compara se reg1 > reg2 1:reg3|0:reg3
jumpC reg2,reg3              # Salta se a comparação for verdadeira

# Exemplo de manipulação de pilha
push reg1               # Salva reg1 na pilha r1
pop reg1                # Carrega valor da pilha r1 para reg1

# Exemplo de desenho
drawP reg1              # Desenha pixel usando coordenadas em reg1
drawS reg2              # Desenha sprite usando dados em reg2