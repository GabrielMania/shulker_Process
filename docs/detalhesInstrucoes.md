## Lista de Instruções
# Instruções Reais
### CPU

| Instrução | Mnemônico | Sintaxe | Descrição |
| :-------- | :-------- | :------ | :-------- |
| `nop`     | NOP       | `nop`   | Nenhuma operação |
| `add`     | ADD       | `add reg1,reg2,reg3` | Soma reg2 com reg3, resultado em reg1 |
| `bshift`  | BSHIFT    | `bshift reg2 right` | Deslocamento binário de reg2 para a direita |
| `not`     | NOT       | `not reg2` | NOT lógico de reg2 |
| `or`      | OR        | `or reg1,reg2,reg3` | OR lógico entre reg2 e reg3, resultado em reg1 |
| `xor`     | XOR       | `xor reg1,reg2,reg3` | XOR lógico entre reg2 e reg3, resultado em reg1 |
| `and`     | AND       | `and reg1,reg2,reg3` | AND lógico entre reg2 e reg3, resultado em reg1 |
| `sizeC`   | SIZEC     | `sizeC reg0,reg1,reg2` | Comparação de tamanho entre reg1 e reg2, resultado em reg0 (indica se maior ou menor por inversão de A,B) |
| `igual`   | IGUAL     | `igual reg0,reg1,reg2` | Compara igualdade de reg1 e reg2, resultado em reg0  |
| `Wtrue`   | TTRUE     | `Ttrue reg1,reg1` | Testa se reg1 é verdadeiro (pelo menos um bit ativo) e define reg1 como booleano (0 ou 1) |
| `limp`    | LIMP      | `limp reg1` | Limpa o registrador |
| `jump`    | JUMP      | `jump reg1` | Salta para endereço em reg1 |
| `jumpC`   | JUMPC     | `jumpC reg1,reg2` | Salto condicional para reg1 se reg2 verdadeiro |
| `dload`   | DLOAD     | `dload reg1 0xffac` | Carrega valor imediato (e.g., 0xffac) para reg1 |
| `inc`     | INC       | `inc reg1` | Incrementa reg1 |
| `push`    | PUSH      | `push reg1` | Salva o valor de reg1 em sua pilha |
| `pop`     | POP       | `pop reg1` | Carrega o valor de reg1 de sua pilha |
| `write`   | WRITE     | `write reg1,reg2` | Escreve o dado de reg2 no endereço especificado por reg1 |
| `read`    | READ      | `read reg1,reg2` | Lê o dado no endereço em reg1 e salva em reg2 |

### GPU

| Instrução | Mnemônico | Sintaxe | Descrição |
| :-------- | :-------- | :------ | :-------- |
| `drawP`   | DRAWP     | `drawP reg1` | Desenha pixel com base nos dados no endereço do ponteiro em reg1 |
| `drawS`   | DRAWS     | `drawS reg1` | Renderiza sprite na tela com dados no endereço do ponteiro em reg1 |
| `drawBg`  | DRAWBG    | `drawBg reg1` | Carrega background para tela com dados no endereço do ponteiro em reg1 |
| `RdrawBg` | RDRAWBG   | `RdrawBg` | Recarrega background |

# Instruções virtuais
 
### Estruturas de controle

### Exemplos de Uso

```assembly puro```
# Exemplo de syntax das instruções
nop                             # não faz nada por 1 ciclo de clock
add reg1,reg2,reg3              # reg1 = reg2 + reg3
bshift reg0 left                # desloca o binario em reg0 em 1 para esquerda
not reg1                        # realiza negação logica inverte os bits do binario
or                              # realiza um OR logico bitwise, para realizar word OR word ultilize Wtrue antes em ambos
xor                             # realiza um XOR logico bitwise, para realizar word XOR word ultilize Wtrue antes em ambos
and                             # realiza um AND logico bitwise, para realizar word AND word ultilize Wtrue antes em ambos
sizeC reg1,reg2,reg3            # Compara se reg1 > reg2, saida = 1:reg3|0:reg3
igual reg1,reg2,reg3            # Compara se reg1 = reg2, saida = 1:reg3|0:reg3
wtrue reg1,reg1                 # Testa se reg1 é verdadeiro (pelo menos um bit ativo) e define reg1 como booleano (0 ou 1), usado para operações bitwise e jumpC
limp reg1                       # limpa o reg1, define como 0
jump reg0                       # define o endereço no program conter como o valor de reg1
jumpc reg0,reg1                 # define o endereço no program conter como o valor de reg1 se reg2 for verdadeiro(primeiro bit 1)
dload reg0 0xffca               # Carrega o valor imediato 0xFFCA para reg0
inc reg0                        # incrementa em 1 o valor no registrador
push reg0                       # armazena o valor de reg0 na stack(profundidade de 8 por registrador e independentes)
pop reg0                        # recupera o valor da stack para reg0
write reg1,reg2                 # escreve o valor em reg2 no endereço em reg1
read reg1,reg2                  # le o valor do endereço armasenado em reg1 e salva em reg2
drawp reg1                      # densenha um pixel com os dados armasenados iniciando no endereço do ponteiro armasenado em reg1
draws reg1                      # desenha um sprite com os dados do arrey que e indicado pelo ponteiro em reg1
drawbg reg1                     # desenha o background com os dados do arrey indicado pelo ponteiro em reg1
rdrawbg                         # apaga os esprites e redesenha o background apagando apenas as camadas maiores que 0 da tela
