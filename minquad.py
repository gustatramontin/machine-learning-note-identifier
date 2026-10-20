import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. Função conhecida
# ============================================================

def f(x):
    return 2 + 3*x - 0.8*x**2 + 0.15*x**3


# ============================================================
# 2. Conjunto de dados
# ============================================================

np.random.seed(42)

n = 40
# n números de -5 a 5, igualmente dividios
x = np.linspace(-5, 5, n)

# Dados sem ruído
y = f(x)

# Dados com ruído: h(x) = f(x) + ruído
ruido = np.random.uniform(-5, 5, n)
b = y + ruido


# ============================================================
# 3. Bases monomiais
#
# g_0(x) = 1
# g_1(x) = x
# g_2(x) = x²
# g_3(x) = x³
#
# A_ki = g_i(x_k)
# ============================================================

grau = 3

g_i = [x**i for i in range(grau + 1)]
# Agrupar lista em colunas
A = np.column_stack(g_i)


# ============================================================
# 4. Equação normal
#
# Aᵀ A w = Aᵀ b
# ============================================================

w = np.linalg.solve(
    A.T @ A,
    A.T @ b
)


# ============================================================
# 5. Função aproximada
#
# g(x) = Σ w_i g_i(x)
# ============================================================

def g(x):
    return sum(
        w[i] * x**i
        for i in range(grau + 1)
    )


# ============================================================
# 6. Mostrar os coeficientes
# ============================================================

print("Coeficientes encontrados:")

for i, wi in enumerate(w):
    print(f"w_{i} = {wi:.4f}")


print("\nFunção estimada:")

for i, wi in enumerate(w):
    print(f"{wi:.4f} x^{i}")


# ============================================================
# 7. Gráfico
# ============================================================

xx = np.linspace(-5, 5, 300)

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

