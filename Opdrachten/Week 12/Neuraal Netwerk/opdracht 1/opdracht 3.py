import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def matmul(a, b):
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            sum = 0
            for k in range(len(b)):
                sum += a[i][k] * b[k][j]
            row.append(sum)
        result.append(row)
    return np.array(result)

# Dataset
images = [
    np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1]),  # A
    np.array([1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1]),  # B
    np.array([0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1]),  # C
    np.array([0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1]),  # 1
    np.array([1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]),  # 2
    np.array([1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1])   # 3
]

outputs = np.array([
    [1, 0, 0, 0, 0, 0],  # A
    [0, 1, 0, 0, 0, 0],  # B
    [0, 0, 1, 0, 0, 0],  # C
    [0, 0, 0, 1, 0, 0],  # 1
    [0, 0, 0, 0, 1, 0],  # 2
    [0, 0, 0, 0, 0, 1]   # 3
])

# Initialisatie
np.random.seed(1)
weights_input_hidden1 = 2 * np.random.rand(16, 6) - 1
weights_hidden1_hidden2 = 2 * np.random.rand(6, 6) - 1
weights_hidden2_output = 2 * np.random.rand(6, 6) - 1

bias_hidden1 = np.zeros((1, 6))
bias_hidden2 = np.zeros((1, 6))
bias_output = np.zeros((1, 6))

lr = 0.5
epochs = 5000

for epoch in range(epochs):
    for i in range(len(images)):
        inputs = images[i].reshape(1, -1)
        target = outputs[i].reshape(1, -1)

        # Forward pass
        hidden1_input = matmul(inputs, weights_input_hidden1) + bias_hidden1
        hidden1_output = sigmoid(hidden1_input)

        hidden2_input = matmul(hidden1_output, weights_hidden1_hidden2) + bias_hidden2
        hidden2_output = sigmoid(hidden2_input)

        final_input = matmul(hidden2_output, weights_hidden2_output) + bias_output
        final_output = sigmoid(final_input)

        # Backpropagation
        error = target - final_output
        d_output = error * sigmoid_derivative(final_output)

        error_hidden2 = matmul(d_output, weights_hidden2_output.T)
        d_hidden2 = error_hidden2 * sigmoid_derivative(hidden2_output)

        error_hidden1 = matmul(d_hidden2, weights_hidden1_hidden2.T)
        d_hidden1 = error_hidden1 * sigmoid_derivative(hidden1_output)

        # Gewichten en biases bijwerken
        weights_hidden2_output += lr * matmul(hidden2_output.T, d_output)
        weights_hidden1_hidden2 += lr * matmul(hidden1_output.T, d_hidden2)
        weights_input_hidden1 += lr * matmul(inputs.T, d_hidden1)

        bias_output += lr * d_output
        bias_hidden2 += lr * d_hidden2
        bias_hidden1 += lr * d_hidden1

    if epoch % 1000 == 0:
        loss = np.mean(np.square(error))
        print(f"Epoch {epoch} - Loss: {loss:.4f}")

# Testen
print("\nNa training:")
test_input = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1]).reshape(1, -1)
hidden1_input = matmul(test_input, weights_input_hidden1) + bias_hidden1
hidden1_output = sigmoid(hidden1_input)

hidden2_input = matmul(hidden1_output, weights_hidden1_hidden2) + bias_hidden2
hidden2_output = sigmoid(hidden2_input)

final_input = matmul(hidden2_output, weights_hidden2_output) + bias_output
final_output = sigmoid(final_input)
print("Testoutput:", final_output)




# 1.	Wat is het minimale aantal nodes per hidden layer dat nog steeds correcte voorspellingen oplevert? Het aantal hidden layers heeft invloed op het functioneren van een netwerk. Maar de gekozen aantal nodes per hidden layer heeft ook impact op het functioneren van het netwerk.

#   ->  1 hidden layer met 3 nodes

# 2.	Wat valt je op als je het aantal nodes sterk verhoogt of verlaagt?

#   ->  Verlagen: te weinig nodes → netwerk leert niet goed, voorspellingen blijven fout of hangen rond 0.5
#   ->  Verhogen: veel nodes → het netwerk wordt trager, leert mogelijk overbodige details (overfitting). Werkt ook niet goed meer.

# 3.	Welke invloed heeft het aantal lagen en nodes op de leersnelheid en de nauwkeurigheid van je netwerk?

#   ->  Meer lagen/nodes → vaak hogere nauwkeurigheid, maar lagere leersnelheid
#   ->  Minder lagen/nodes → snellere training, maar kans op onderfitting

# 4.	Kan het de extra input ook goed voorspellen? Hebben de aantal nodes hier invloed op?

#   ->   Als de extra input vergelijkbaar is met de trainingsdata, dan werkt goed. En het aantal nodes heeft invloed erbij.
