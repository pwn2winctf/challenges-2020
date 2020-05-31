# Trechos de códigos

Explorando o seguinte comando:

```
0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?H.=151:N.:V.23;1,12;0;0;0
```

Comandos sem resultado, mesmo que o anterior.

- `0` - Nada acontece
- `0$` - ERRO: `No such variable`
- `0$H` - ERRO: `No such variable`
- `0$H.` - ERRO: `Mistake`
- `0$H.=` - ERRO: `No such variable`
- `0$H.="` - ERRO: `Missing "`
- `0$H.=" 7s35zn17s35 5/%5"` - Escreve ` 7s35zn17s35 5/%5`
    - `"` delimita string
    - `H.` é a saída padrão
- `0$H.=""` - ERRO: `Missing "`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"` - Escreve ` 7s35zn17s35 5/%5"&45/%5 s3sq}ye3£3! +r5&d5l/7o5 pss3>m)eup5 5|45/*£t0p  usq5`
    - `""` é interpretado como `"` dentro de string
    - `#` é interpretado como `£` dentro de string
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+` - ERRO: `No such variable`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1` - Escreve ` 7s35zn17s35 5/%5"&45/%5 s3sq}ye3£3! +r5&d5l/7o5 pss3>m)eup5 5|45/*£t0p  usq5` seguido de um quadrado branco
    - `0$H.=CHR$-1` - Desenha um quadrado branco
    - `0$H.=CHR$-1+CHR$-1` - Desenha dois quadrados brancos
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"` - ERRO: `Missing "`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1"` - Escreve ` 7s35zn17s35 5/%5""&45/%5 s3sq}ye3£3! +r5&d5l/7o5 pss3>m)eup5 5|45/*£t0p  usq5`, um quadrado, `51~£h1`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F` - ERRO: `Mistake`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.` - ERRO: `FOR variable`
    - `F.` inicia um `FOR`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L` - ERRO: `Mistake`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72` - Escreve ` 7s35zn17s35 5/%5""&45/%5 s3sq}ye3£3! +r5&d5l/7o5 pss3>m)eup5 5|45/*£t0p  usq5`, um quadrado, `51~£h1`
    - `:` - Separa comandos
    - `F.L=0TO72` - FOR L variando de 0 a 72
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S` - ERRO: `Syntax error`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.` - ERRO: `No such variable`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12` - Escreve ` 7s35zn17s35 5/%5""&45/%5 s3sq}ye3£3! +r5&d5l/7o5 pss3>m)eup5 5|45/*£t0p  usq5`, um quadrado, `51~£h1`
    - `F.L=0TO72S.12` - FOR L variando de 0 a 72 com STEP 12
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L` - ERRO: `Mistake`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?` - ERRO: `No such variable`
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?H.=151` - Muda propriedades da saída
    - `1` - Primeira linha vermelha
    - `2` - Primeira linha verde
    - `3` - Primeira linha amarela
    - `4` - Primeira linha azul
    - `5` - Primeira linha rosa
    - `6` - Primeira linha ciano
    - `8` - Primeira linha piscante
    - `13` - Primeira linha com o dobro do tamanho vertical
    - `18` - Pedaços de QRcode verde
    - `19` - Pedaços de QRcode amarelo
    - `20` - Pedaços de QRcode azul
    - `21` - Pedaços de QRcode rosa
    - `22` - Pedaços de QRcode ciano
    - `23` - Pedaços de QRcode normal
    - `24` - Primeira linha inteira preta
    - `29` - Primeira linha inteira branca
    ....
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?H.=151:N.` - Faz algo parecido na segunda linha, deve ser o "next" do for
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?H.=151:N.:V.23` - Faz o mesmo que o anterior mas não volta para novo comando
- `0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?H.=151:N.:V.23;1,12;0;0;` - Rearranja pra cada linha ter 12 caracteres

Concluindo, esse é menor que o outro e ainda funciona:

```
0$H.=" 7s35zn17s35 5/%5""&45/%5 s3sq}ye3#3! +r5&d5l/7o5 pss3>m)eup5 5|45/*#t0p  usq5"+CHR$-1+"51~#h1":F.L=0TO72S.12:L?H.=23:N.:V.23;1,12;0;0;
```

Agora preciso descobrir como fazer cada parte de um QRcode, mudando o texto inicialmente escrito na tela. O arquivo `ls.png` mostra um qr code para `ls`. Vou reproduzi-lo. Para começar vou mudar partes do texto e ver o que acontece. Mudando o primeiro caracter, percebo que cada caracter altera duas colunas e 3 linhas do QRcode final, conforme descrito abaixo (0 para preto e 1 para branco):

- bit0 ao bit4 e bit6 do código ascii, nessa ordem
- `@-_` - não funciona