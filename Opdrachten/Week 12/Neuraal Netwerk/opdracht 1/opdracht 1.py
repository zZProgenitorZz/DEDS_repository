import numpy as np

# Sigmoid activatiefunctie en afgeleide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Inputdata (5 samples, elk met 4 inputs)
inputs = np.array([
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 1]
])

# Outputlabels (1 output per sample)
outputs = np.array([[0], [1], [1], [0], [1]])

# Initiele gewichten (random tussen -1 en 1)
np.random.seed(1)
weights_input_hidden = 2 * np.random.rand(4, 3) - 1  # 4 inputs → 3 hidden nodes
weights_hidden_output = 2 * np.random.rand(3, 1) - 1  # 3 hidden nodes → 1 output node

# Biases
bias_hidden = np.random.rand(1, 3)
bias_output = np.random.rand(1, 1)

# Learning rate
lr = 0.5

# Trainen
for epoch in range(30000):
    # === Voorwaartse propagatie ===
    # Input naar hidden
    hidden_input = []
    for i in range(len(inputs)):
        hidden_row = []
        for j in range(3):  # 3 hidden nodes
            weighted_sum = 0
            for k in range(4):  # 4 input nodes
                weighted_sum += inputs[i][k] * weights_input_hidden[k][j]
            weighted_sum += bias_hidden[0][j]
            hidden_row.append(sigmoid(weighted_sum))
        hidden_input.append(hidden_row)
    hidden_output = np.array(hidden_input)

    # Hidden naar output
    final_output = []
    for i in range(len(hidden_output)):
        weighted_sum = 0
        for j in range(3):
            weighted_sum += hidden_output[i][j] * weights_hidden_output[j][0]
        weighted_sum += bias_output[0][0]
        final_output.append([sigmoid(weighted_sum)])
    final_output = np.array(final_output)

    # === Achterwaartse propagatie ===
    error = outputs - final_output
    d_output = error * sigmoid_derivative(final_output)

    # Hidden-layer fout
    error_hidden = d_output.dot(weights_hidden_output.T)
    d_hidden = error_hidden * sigmoid_derivative(hidden_output)

    # === Gewichten bijwerken ===
    # Input → Hidden
    for i in range(4):  # input nodes
        for j in range(3):  # hidden nodes
            delta = 0
            for k in range(len(inputs)):
                delta += inputs[k][i] * d_hidden[k][j]
            weights_input_hidden[i][j] += lr * delta / len(inputs)

    # Hidden → Output
    for i in range(3):  # hidden nodes
        delta = 0
        for k in range(len(hidden_output)):
            delta += hidden_output[k][i] * d_output[k][0]
        weights_hidden_output[i][0] += lr * delta / len(hidden_output)

    # Biases bijwerken
    for j in range(3):
        delta = 0
        for k in range(len(d_hidden)):
            delta += d_hidden[k][j]
        bias_hidden[0][j] += lr * delta / len(d_hidden)

    delta = 0
    for k in range(len(d_output)):
        delta += d_output[k][0]
    bias_output[0][0] += lr * delta / len(d_output)

    # Afdrukken elke 2000 epochs
    if epoch % 5000 == 0:
        loss = np.mean(np.square(error))
        print(f"Epoch {epoch} - Loss: {loss:.4f}")

# Resultaat na training
print("\nGetrainde output:")
print(final_output.round(2))
