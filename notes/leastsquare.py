import numpy as np

# A4 is the starting point, as in your original code.
NOTES = []
for o in range(2,6):
    NOTES = [*NOTES,
                 f"A{o}",
                 f"A♯{o}",
                 f"B{o}",
                 f"C{o+1}",
                 f"C#{o+1}",
                 f"D{o+1}",
                 f"D♯{o+1}",
                 f"E{o+1}",
                 f"F{o+1}",
                 f"F#{o+1}",
                 f"G{o+1}",
                 f"G#{o+1}"
             ]


def Amat(t):
    FREQUENCIES = np.array([
        (440/4) * 2**(i / 12) for i in range(12*4)
    ])

    columns = []
    for freq in FREQUENCIES:
        columns.append(np.sin(2 * np.pi * freq * t))
        columns.append(np.cos(2 * np.pi * freq * t))

    A = np.column_stack(columns)

# Precompute the pseudoinverse because A doesn't change.
    A_pinv = np.linalg.pinv(A)
    return A_pinv

def get_notes(A, x):
    w = A @ x

    # One amplitude per note: sqrt(a² + b²)
    amplitudes = np.hypot(w[::2], w[1::2])

    order = np.argsort(amplitudes)[::-1]

    return amplitudes
