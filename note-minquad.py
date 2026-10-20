import numpy as np
import matplotlib.pyplot as plt
from math import floor


# ============================================================
# 1. Função conhecida
# ============================================================

def f(x):
    f0 = 440
    note = 8 
    freq = f0*2**(note/12)
    return np.sin(2*np.pi*freq*(x))


# ============================================================
# 2. Conjunto de dados
# ============================================================

np.random.seed(42)

n = 100_000
# n números de -5 a 5, igualmente dividios
x = np.linspace(0, 0.1, n)

# Dados sem ruído
y = f(x)

# Dados com ruído: h(x) = f(x) + ruído
ruido = np.random.uniform(-1, 1, n)/10
b = y + ruido


# ============================================================
# 3. Bases monomiais
#
# g_0(x) = 1
# g_1(x) = x
# g_2(x) = x²
# g_3(x) = x³

# A_ki = g_i(x_k)
# ============================================================

def note_sin(x, note_i):
    frequency = 2**(note_i/12)*440
    return np.sin(2*np.pi*frequency*x)

def note_cos(x,note_i):
    frequency = 2**(note_i/12)*440
    return np.cos(2*np.pi*frequency*x)

g_sin = [note_sin(x, i) for i in range(12)]
g_cos = [note_cos(x, i) for i in range(12)]
g_i = []
for g_sin_i,g_cos_i in zip(g_sin, g_cos):
    g_i.append(g_sin_i)
    g_i.append(g_cos_i)
# Agrupar lista em colunas
A = np.column_stack(g_i)


# ============================================================
# 4. Equação normal
#
# Aᵀ A w = Aᵀ b
# ============================================================
"""
w = np.linalg.solve(
    A.T @ A,
    A.T @ b
)
"""
w, *_ = np.linalg.lstsq(A, b, rcond=None)

# ============================================================
# 5. Função aproximada
#
# g(x) = Σ w_i g_i(x)
# ============================================================

def g(x):
    result = 0
    for i in range(12):
        result += w[2*i]*note_sin(x, i) + w[2*i+1]*note_cos(x, i)
    return result


# ============================================================
# 6. Mostrar os coeficientes
# ============================================================

print("Coeficientes encontrados:")

for i, wi in enumerate(w):
    print(f"w_{i} = {wi:.4f}")


print("\nFunção estimada:")

notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
for i, wi in enumerate(w):
    if i % 2 == 0:
        amp = np.hypot(wi, w[i+1])
        print(f"{amp:.2f} {notes[floor(i/2)]}")


# ============================================================
# 7. Gráfico
# ============================================================

xx = np.linspace(-1, 1, 300)


plt.scatter(
    x, b,
    color="red",
    label="Dados com ruído"
)

plt.plot(
    xx, f(xx),
    color="blue",
    label="f(x) original"
)
plt.plot(
    xx, g(xx),
    color="green",
    linestyle="--",
    label="g(x) mínimos quadrados"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Método dos Mínimos Quadrados")

plt.legend()
plt.grid()

#plt.show()

plt.savefig(
    "resultado_minimos_quadrados.png",
    dpi=300,
    bbox_inches="tight"
)

