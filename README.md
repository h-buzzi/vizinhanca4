### Produzido por Henrique Eissmann Buzzi ###

# Algoritmo Two-pass para connected-components com vizinhança 4

* main possui versão mais otimizada
* version-1 é a versão original, onde a segunda passagem do algoritmo não é tão otimizada

## Modo de usar:

Forneça uma imagem binária para a função "two-pass", e selecione o método. O algoritmo irá retornar o número de objetos encontrados, uma imagem com cada objeto representado pela sua diferente label e sua matriz de label.

## Executando:
Ao rodar o algoritmo, tem-se os 2 métodos:

* default: Este é o algoritmo two-pass apenas, onde ele retornará a imagem dos labels sem se importar com o intervalo do valor numérico que a label possui.

* reform: Este é o algoritmo two-pass em conjunto com um algoritmo de correção de labels, onde ele define o intervalor numérico da label para ser igual ao intervalo de objetos encontrados, ou seja, o primeiro objeto terá label 1, o segundo label 2, até o N elemento final que recebe a label N.

## Conceitos aplicados

Connected-components, Vizinhança 4, Processamento de Imagem, Rotulamento

## Possíveis implementações futuras

* Comparação do método implementado com outras funções já prontas que servem para o mesmo propósito.
