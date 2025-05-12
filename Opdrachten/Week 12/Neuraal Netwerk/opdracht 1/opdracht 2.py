import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Handmatige matrixvermenigvuldiging (zonder np.dot)
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

# Dataset: 4x4 plaatjes → 16 inputfeatures
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
weights_input_hidden = 2 * np.random.rand(16, 6) - 1
weights_hidden_output = 2 * np.random.rand(6, 6) - 1
bias_hidden = np.zeros((1, 6))
bias_output = np.zeros((1, 6))
lr = 0.5
epochs = 5000

for epoch in range(epochs):
    for i in range(len(images)):
        inputs = images[i].reshape(1, -1)  # Maak het een rij
        target = outputs[i].reshape(1, -1)

        # Forward
        hidden_input = matmul(inputs, weights_input_hidden) + bias_hidden
        hidden_output = sigmoid(hidden_input)

        final_input = matmul(hidden_output, weights_hidden_output) + bias_output
        final_output = sigmoid(final_input)

        # Backprop
        error = target - final_output
        d_output = error * sigmoid_derivative(final_output)

        error_hidden = matmul(d_output, weights_hidden_output.T)
        d_hidden = error_hidden * sigmoid_derivative(hidden_output)

        # Gewichten bijwerken
        weights_hidden_output += lr * matmul(hidden_output.T, d_output)
        weights_input_hidden += lr * matmul(inputs.T, d_hidden)

        bias_hidden += lr * d_hidden
        bias_output += lr * d_output

    if epoch % 1000 == 0:
        loss = np.mean(np.square(error))
        print(f"Epoch {epoch} - Loss: {loss:.4f}")

# Testen
print("\nNa training:")
test_input = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1]).reshape(1, -1)
hidden_input = matmul(test_input, weights_input_hidden) + bias_hidden
hidden_output = sigmoid(hidden_input)
final_input = matmul(hidden_output, weights_hidden_output) + bias_output
final_output = sigmoid(final_input)
print("Testoutput:", final_output)








#   Vragen:
#   1.	Hoe groot moet jouw neuraal netwerk zijn om jouw gekozen inputdimensie zodanig te hebben verwerkt dat de error beduidend verlaagd is na het trainen tov andere inputdimensies?

#   ->  Heb een neurale netwerk voor afbeeldingen gemaakt van 4x4. dit grootte verlaagd de errors veel meer dan input van 3x3 grootte.

#   2.	Hoeveel hidden nodes heb je nodig? Experimenteer met verschillende aantallen en evalueer de invloed op prestaties (errors).

#   ->  1 Hidden nodes is goed genoeg.

#   3.	Hoeveel iteraties zijn ongeveer nodig om het netwerk goed te trainen? ‘Goed’ is subjectief, maar het gaat erom dat je experimenteel een netwerk architectuur vindt (in dit geval aantal nodes) die de grootste error verlaging oplevert.

#   ->  het moet een iteratie hebben van ongeveer 5000 om de netwerk zo goed mogelijk getraind te hbben.

#   4.	Hoeveel output nodes gebruik je (afhankelijk van het aantal klassen)?

#   ->  Ik heb 6 output nodes die afhankelijk zijn het aantal klassen, omdat elk output heeft maar 1 input voorbeeld.
#
#
#
#
#
#
#