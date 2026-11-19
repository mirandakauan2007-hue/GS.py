# Lotação do Metrô de São Paulo com Cálculo e Python

Projeto de **Cálculo** feito em **Python**. Ele modela a lotação da plataforma de uma estação do metrô de São Paulo ao longo da manhã e usa conceitos de cálculo para analisar essa curva.

## Ideia do projeto

A lotação da plataforma ao longo da manhã é descrita por uma função em forma de sino:

```
L(t) = base + altura * e^(-(t - t_pico)^2 / c)
```

- `t`: horário em horas (7,67 = 7h40)
- `L(t)`: número de pessoas na plataforma
- `t_pico`: horário do pico (7h40)
- `c`: largura do pico

O nível da curva (`base` e `altura`) é calibrado com **dados reais** de entradas diárias de uma estação.

## Integrantes

- Vitor Bianchini Viaro - 569804
- Kauã Miranda - 569473
- João Vitor Da Silva Araújo - 571420
- Lucas Lima Cruz - 572047


## Conceitos de cálculo usados

- **Limites:** mostra que, muito longe do pico, a lotação tende à `base`.
- **Derivada:** `L'(t)` indica quando a plataforma enche (positivo) ou esvazia (negativo).
- **Máximos e mínimos:** `L'(t) = 0` dá o pico, e `L''(t) < 0` confirma que é um máximo.
- **Pontos de inflexão:** `L''(t) = 0` dá os horários em que a lotação muda mais rápido.
- **Integral:** calcula a área sob a curva (pessoas-hora) e a lotação média, pela regra do trapézio.
- **Teorema Fundamental do Cálculo:** confere que a integral de `L'` entre dois horários é igual a `L(b) - L(a)`.
- **Otimização:** encontra o melhor horário para sair, equilibrando lotação menor e não sair cedo demais.

## Como rodar

1. Instale o [Python](https://www.python.org/downloads/) e o matplotlib:
   ```
   pip install matplotlib
   ```
2. Baixe os dados (veja a seção Dados) e coloque o CSV no computador.
3. No topo do código, ajuste as variáveis:
   ```python
   ARQUIVO = "metrosp-station-entries-daily.csv"  # nome ou caminho do CSV
   ESTACAO = "Luz"       # nome da estação
   LINHA = 4             # número da linha
   ANO = 2025            # ano usado no cálculo
   EM_MILHARES = False   # True se o valor do CSV estiver em milhares
   ```
4. Rode:
   ```
   python test.py
   ```

Sem o CSV, o programa avisa e usa um modelo padrão (pico de 200 pessoas), então ele roda de qualquer forma.

## Saída

O programa imprime no terminal os limites, as derivadas, a integral e o resultado da otimização, e salva 3 gráficos:

- `grafico_lotacao.png`: a curva L(t), os limites de vazio e lotado, o pico e o melhor horário de saída
- `grafico_derivada.png`: a taxa de variação L'(t)
- `grafico_integral.png`: a área sob a curva

## Dados

Os dados vêm do pacote **metrosp**, que reúne dados do Metrô de São Paulo (fonte original: METRO SP / Insper Dataverse):

- Repositório: https://github.com/viniciusoike/metrosp
- Dataset usado: entradas diárias por estação (`station_entries_daily`)
- Colunas usadas: `date`, `line_number`, `station_name`, `value`
- O CSV é separado por `;` e usa `NA` para valores ausentes

O CSV não está neste repositório porque é grande (cerca de 27 MB).

## Hipóteses do modelo

Estes valores são estimativas e **não vêm dos dados**. Podem ser ajustados no código:

- `FRACAO_PICO = 0.12`: 12% das entradas do dia acontecem na hora de pico
- `PERMANENCIA = 0.10`: cada pessoa fica cerca de 6 minutos na plataforma
- `t_pico = 7.67` e `c = 0.18`: o horário e a largura do pico são fixos, porque os dados são diários e não mostram o horário

Os dados reais calibram o **nível** da lotação. O **formato** do pico vem do modelo.

## Tecnologias

- Python 3
- matplotlib
- Bibliotecas padrão: `csv`, `math`, `statistics`, `datetime`
