import csv
import math
import statistics
from datetime import datetime

import matplotlib.pyplot as plt

# =====================================================
# PROJETO: lotacao da plataforma ao longo da manha
# Usa calculo (limite, derivada, integral, otimizacao)
# com dados reais do pacote metrosp (Metro de Sao Paulo)
# =====================================================

# ---------- 0) Configuracao (mude aqui) ----------
ARQUIVO = r"C:\Users\User\Downloads\metrosp-station-entries-daily.csv" # CSV exportado do R
ESTACAO = "Luz"                 # nome (ou parte do nome) da estacao
LINHA = 4                   # numero da linha (evita confundir estacoes)
ANO = 2025                     # ano usado para calcular a media
EM_MILHARES = False           # True se a coluna "value" esta em milhares

# Hipoteses do modelo (nao vem dos dados, podem ser ajustadas)
FRACAO_PICO = 0.12   # 12% das entradas do dia acontecem na hora de pico
PERMANENCIA = 0.10   # cada pessoa fica ~0,10 h (6 min) na plataforma


# ---------- 1) Ler os dados reais ----------
# Colunas do CSV: date, line_number, station_name, value
entradas = []  # entradas diarias (so dias uteis) da estacao escolhida

try:
    arquivo = open(ARQUIVO, encoding="utf-8-sig")
    leitor = csv.DictReader(arquivo, delimiter=";")

    for linha in leitor:
        # pula outras estacoes e outras linhas
        if ESTACAO.lower() not in linha["station_name"].lower():
            continue
        if int(float(linha["line_number"])) != LINHA:
            continue

        data = datetime.strptime(linha["date"][:10], "%Y-%m-%d")

        # fica so com dias uteis (segunda=0 ... sexta=4) do ano escolhido
        if data.year == ANO and data.weekday() < 5 and linha["value"] != "NA":
            entradas.append(float(linha["value"]))

    arquivo.close()
except FileNotFoundError:
    print("Arquivo", ARQUIVO, "nao encontrado.")

# ---------- 2) Calibrar o modelo ----------
if len(entradas) > 0:
    # mediana: nao se deixa enganar por dias muito fora do normal
    entradas_dia = statistics.median(entradas)
    if EM_MILHARES:
        entradas_dia = entradas_dia * 1000

    # pessoas na plataforma = pessoas que chegam por hora x tempo que ficam
    pico = entradas_dia * FRACAO_PICO * PERMANENCIA
    print("Estacao:", ESTACAO, "| ano:", ANO)
    print("Entradas por dia util (mediana):", round(entradas_dia))
else:
    # sem dados: usa o modelo original do projeto
    pico = 200
    print("Sem dados. Usando o modelo original (pico = 200).")

# ---------- 3) Modelo matematico ----------
# L(t) = base + altura * e^(-(t - t_pico)^2 / c)
# E uma curva em forma de sino: baixa de madrugada, maxima no pico.
base = 0.10 * pico      # lotacao "de fundo" (10% do pico)
altura = 0.90 * pico    # quanto a lotacao sobe acima da base
t_pico = 7.67           # horario do pico (7,67 h = 7h40)
c = 0.18                # largura do pico (quanto maior, mais largo)

# limites do LED: abaixo de lim_vazio = vazio, acima de lim_lotado = lotado
lim_vazio = 0.30 * pico
lim_lotado = 0.70 * pico


def L(t):
    # lotacao (pessoas) no horario t
    return base + altura * math.exp(-((t - t_pico) ** 2) / c)


def dL(t):
    # derivada L'(t): mostra se a plataforma esta enchendo (+) ou esvaziando (-)
    return -2 * altura / c * (t - t_pico) * math.exp(-((t - t_pico) ** 2) / c)


def d2L(t):
    # segunda derivada L''(t): diz se um ponto critico e maximo ou minimo
    u = (t - t_pico) ** 2 / c
    return 2 * altura / c * (2 * u - 1) * math.exp(-u)


def horario(t):
    # transforma 7.67 em "7h40"
    h = int(t)
    m = round((t - h) * 60)
    if m == 60:
        h = h + 1
        m = 0
    return str(h) + "h" + str(m).zfill(2)


# ---------- 4) Limites ----------
# Muito longe do pico (t enorme), a exponencial vai a 0 e L(t) tende a "base".
print("\n--- Limites ---")
print("t -> +infinito:", round(L(1000), 1), "(= base)")
print("t -> -infinito:", round(L(-1000), 1), "(= base)")

# ---------- 5) Derivadas ----------
print("\n--- Derivadas ---")
print("Pico as", horario(t_pico), "com", round(L(t_pico)), "pessoas")
# L'(t_pico) = 0 (topo da curva) e L'' < 0 confirma que e um MAXIMO
print("L''(pico) =", round(d2L(t_pico)), "(negativo, entao e maximo)")

# Pontos de inflexao: onde L''(t) = 0, ou seja, t_pico -+ raiz(c/2).
# Neles a lotacao muda mais rapido (enche/esvazia mais rapido).
dist = math.sqrt(c / 2)
infl1 = t_pico - dist
infl2 = t_pico + dist
print("Enche mais rapido as", horario(infl1), "->", round(dL(infl1)), "pessoas/h")
print("Esvazia mais rapido as", horario(infl2), "->", round(dL(infl2)), "pessoas/h")

# Horarios em que L(t) = lim_lotado (resolvendo a equacao para t)
raio = math.sqrt(-c * math.log((lim_lotado - base) / altura))
print("Lotado de", horario(t_pico - raio), "ate", horario(t_pico + raio))


# ---------- 6) Integral ----------
# Regra do trapezio: divide a area sob a curva em faixas e soma.
def integral(f, a, b, n=1000):
    h = (b - a) / n                  # largura de cada faixa
    soma = (f(a) + f(b)) / 2         # as pontas contam pela metade
    for i in range(1, n):
        soma = soma + f(a + i * h)
    return soma * h


total = integral(L, 6, 10)   # area sob L(t) entre 6h e 10h
media = total / (10 - 6)     # valor medio = area / tempo
print("\n--- Integral ---")
print("Area de 6h a 10h:", round(total), "pessoas-hora")
print("Lotacao media:", round(media), "pessoas")

# Teorema Fundamental do Calculo: a integral de L' entre 6h e o pico
# deve ser igual a L(pico) - L(6h). Os dois numeros abaixo devem coincidir.
print("Integral de L' (6h ate o pico):", round(integral(dL, 6, t_pico), 2))
print("L(pico) - L(6h):", round(L(t_pico) - L(6), 2))

# ---------- 7) Otimizacao ----------
# Qual o melhor horario para sair? Equilibrio entre:
#  - lotacao menor (L(t))
#  - nao sair cedo demais (custo beta * (t_usual - t)^2)
# J(t) = L(t) + beta * (t_usual - t)^2 ; queremos o t que MINIMIZA J.
t_usual = 7 + 40 / 60       # horario em que a pessoa costuma sair (7h40)
beta = 300 * pico / 200     # peso do custo (escala junto com a lotacao)


def J(t):
    return L(t) + beta * (t_usual - t) ** 2


# Testa horarios de 7h00 ate 7h40 (de 0,001 em 0,001 h) e guarda o melhor
melhor_t = 7.0
t = 7.0
while t <= t_usual:
    if J(t) < J(melhor_t):
        melhor_t = t
    t = t + 0.001

reducao = (1 - L(melhor_t) / L(t_usual)) * 100
print("\n--- Otimizacao ---")
print("Melhor horario para sair:", horario(melhor_t))
print("Lotacao nesse horario:", round(L(melhor_t)), "pessoas")
print("Lotacao as 7h40:", round(L(t_usual)), "pessoas")
print("Reducao:", round(reducao), "%")

# ---------- 8) Graficos ----------
# Lista de horarios de 6h ate 10h, de 0,01 em 0,01
tempos = [6 + i * 0.01 for i in range(401)]
lotacao = [L(x) for x in tempos]
derivada = [dL(x) for x in tempos]

# Grafico 1: lotacao, limites, pico e melhor horario
plt.figure(figsize=(8, 4))
plt.plot(tempos, lotacao, label="L(t)")
plt.axhline(lim_vazio, color="green", linestyle="--", label="limite vazio")
plt.axhline(lim_lotado, color="red", linestyle="--", label="limite lotado")
plt.plot(t_pico, L(t_pico), "ro", label="pico")
plt.plot(melhor_t, L(melhor_t), "g^", label="melhor saida")
plt.xlabel("Horario (h)")
plt.ylabel("Pessoas na plataforma")
plt.title("Lotacao ao longo da manha - " + ESTACAO)
plt.legend()
plt.grid(True)
plt.savefig("grafico_lotacao.png")

# Grafico 2: derivada (acima de 0 = enchendo, abaixo de 0 = esvaziando)
plt.figure(figsize=(8, 4))
plt.plot(tempos, derivada, color="purple", label="L'(t)")
plt.axhline(0, color="black")
plt.xlabel("Horario (h)")
plt.ylabel("Taxa de variacao (pessoas/h)")
plt.title("Taxa de variacao da lotacao")
plt.legend()
plt.grid(True)
plt.savefig("grafico_derivada.png")

# Grafico 3: area sob a curva (a integral)
plt.figure(figsize=(8, 4))
plt.plot(tempos, lotacao)
plt.fill_between(tempos, lotacao, alpha=0.3)
plt.xlabel("Horario (h)")
plt.ylabel("Pessoas na plataforma")
plt.title("Area sob L(t) = " + str(round(total)) + " pessoas-hora")
plt.grid(True)
plt.savefig("grafico_integral.png")

plt.show()

