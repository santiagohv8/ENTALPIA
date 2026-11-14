import numpy as np

X = np.array([1, 2, 3, 4, 5])
Y = np.array([0, 1, 0, 1, 1])

# Coeficientes iniciales
b0 = 0.0
b1 = 0.0

for i in range(10):

    # 1. Calculamos z
    z = b0 + b1 * X

    # 2. Calculamos p
    p = 1 / (1 + np.exp(-z))

    # 3. Calculamos Y - p
    error = Y - p

    # 4. Matriz X
    matriz_X = np.column_stack((np.ones(len(X)), X))

    # 5. Matriz W
    W = np.diag(p * (1 - p))

    # 6. Calculamos X^T W X
    A = matriz_X.T @ W @ matriz_X

    # 7. Calculamos X^T (Y - p)
    B = matriz_X.T @ error

    # 8. Calculamos el cambio de los coeficientes
    cambio = np.linalg.inv(A) @ B

    # 9. Actualizamos b
    b0 = b0 + cambio[0]
    b1 = b1 + cambio[1]

    print("Iteración:", i + 1)
    print("b0 =", b0)
    print("b1 =", b1)
    print()