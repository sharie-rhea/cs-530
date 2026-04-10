import math
import random

def single_neuron(inputs, weights, bias, activation='sigmoid'):
    """
    Simulates a single neuron with the given inputs, weights, bias, and activation function.

    Parameters:
    inputs (list of float): The input values to the neuron.
    weights (list of float): The weights corresponding to each input.
    bias (float): The bias term.
    activation (str): The activation function to use. Options: 'sigmoid', 'relu', 'tanh'. Default is 'sigmoid'.

    Returns:
    float: The output of the neuron after applying the activation function.
    """
    if len(inputs) != len(weights):
        raise ValueError("Inputs and weights must have the same length.")

    # Compute the weighted sum
    z = sum(i * w for i, w in zip(inputs, weights)) + bias

    # Apply the activation function
    if activation == 'sigmoid':
        return 1 / (1 + math.exp(-z))
    elif activation == 'relu':
        return max(0, z)
    elif activation == 'tanh':
        return (math.tanh(z) + 1) / 2  # Transform to (0,1) range
    else:
        raise ValueError("Unsupported activation function. Choose 'sigmoid', 'relu', or 'tanh'.")


def binary_classifier(dataset, weights, activation='sigmoid', bias=0.0):
    """
    Implements a binary classifier using the single_neuron function.

    Parameters:
    dataset (list of lists): A list of input vectors, where each vector is a list of floats.
    weights (list of float): The weights for the neuron.
    activation (str): The activation function to use. Options: 'sigmoid', 'relu', 'tanh'. Default is 'sigmoid'.
    bias (float): The bias term. Default is 0.0.

    Returns:
    list of int: A list of binary predictions (0 or 1) for each input vector in the dataset.
                 For 'sigmoid', predictions are based on threshold 0.5.
                 For 'relu', predictions are based on threshold 0.0 (since ReLU outputs >= 0).
                 For 'tanh', predictions are based on threshold 0.5 (transformed to (0,1) range).
    """
    predictions = []
    for inputs in dataset:
        output = single_neuron(inputs, weights, bias, activation)
        if activation == 'sigmoid':
            prediction = 1 if output >= 0.5 else 0
        elif activation == 'relu':
            prediction = 1 if output > 0.0 else 0  # ReLU is >= 0, so > 0 for positive class
        elif activation == 'tanh':
            prediction = 1 if output >= 0.5 else 0  # Tanh transformed to (0,1), threshold 0.5
        else:
            raise ValueError("Unsupported activation function.")
        predictions.append(prediction)
    return predictions


def generate_synthetic_data(n_samples=100, n_features=2, centers=None, noise=0.5):
    """
    Generates synthetic data for binary classification.

    Parameters:
    n_samples (int): Total number of samples to generate. Default is 100.
    n_features (int): Number of features per sample. Default is 2.
    centers (list of lists): Centers for the two classes. If None, defaults to [[0]*n_features, [1]*n_features].
    noise (float): Standard deviation of the Gaussian noise added to the centers. Default is 0.5.

    Returns:
    tuple: (X, y) where X is a list of input vectors (each a list of floats), and y is a list of labels (0 or 1).
    """
    if centers is None:
        centers = [[0.0] * n_features, [1.0] * n_features]
    
    X = []
    y = []
    samples_per_class = n_samples // 2
    
    for _ in range(samples_per_class):
        # Generate sample for class 0
        point = [random.gauss(c, noise) for c in centers[0]]
        X.append(point)
        y.append(0)
        
        # Generate sample for class 1
        point = [random.gauss(c, noise) for c in centers[1]]
        X.append(point)
        y.append(1)
    
    return X, y


def train_single_neuron(X, y, activation='sigmoid', learning_rate=0.01, epochs=1000):
    """
    Trains a single neuron using gradient descent for binary classification.

    Parameters:
    X (list of lists): The input features, where each inner list is a sample's features.
    y (list of int): The target labels (0 or 1) for each sample.
    activation (str): The activation function. Supports 'sigmoid', 'relu', and 'tanh' (all use binary cross-entropy). Default is 'sigmoid'.
    learning_rate (float): The learning rate for gradient descent. Default is 0.01.
    epochs (int): The number of training epochs. Default is 1000.

    Returns:
    tuple: (weights, bias) where weights is a list of floats, and bias is a float.
    """
    if activation not in ['sigmoid', 'relu', 'tanh']:
        raise ValueError("Training supports 'sigmoid', 'relu', and 'tanh' activations.")
    
    if len(X) != len(y):
        raise ValueError("X and y must have the same length.")
    
    n_features = len(X[0])
    # Initialize weights randomly
    weights = [random.uniform(-1, 1) for _ in range(n_features)]
    bias = 0.0
    
    for epoch in range(epochs):
        total_loss = 0.0
        for inputs, target in zip(X, y):
            # Forward pass
            z = sum(i * w for i, w in zip(inputs, weights)) + bias
            if activation == 'sigmoid':
                output = 1 / (1 + math.exp(-z))
                loss = - (target * math.log(output + 1e-15) + (1 - target) * math.log(1 - output + 1e-15))
                dz = output - target
            elif activation == 'relu':
                output = max(1e-7, min(1 - 1e-7, max(0, z)))  # Clip to [1e-7, 1-1e-7]
                # Use binary cross-entropy for ReLU
                loss = - (target * math.log(output) + (1 - target) * math.log(1 - output))
                dz = output - target
            elif activation == 'tanh':
                output = (math.tanh(z) + 1) / 2  # Transform to (0,1)
                # Use binary cross-entropy for tanh
                loss = - (target * math.log(output + 1e-15) + (1 - target) * math.log(1 - output + 1e-15))
                dz = output - target
            
            total_loss += loss
            
            # Backward pass
            for i in range(n_features):
                weights[i] -= learning_rate * dz * inputs[i]
            bias -= learning_rate * dz
        
        # Optional: print loss every 100 epochs
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(X):.4f}")
    
    return weights, bias


def main():
    """
    Main function to test the neural network.
    Generates separate training and testing synthetic data, trains the network with sigmoid, ReLU, and tanh activations,
    and displays the results of binary classification on both training and testing data.
    """
    print("Generating training data...")
    X_train, y_train = generate_synthetic_data(n_samples=200, n_features=2, centers=[[0, 0], [2, 2]], noise=0.5)
    
    print("Generating testing data...")
    X_test, y_test = generate_synthetic_data(n_samples=100, n_features=2, centers=[[0, 0], [2, 2]], noise=0.5)
    
    activations = ['sigmoid', 'relu', 'tanh']
    trained_models = {}
    
    for activation in activations:
        print(f"\nTraining with {activation} activation...")
        weights, bias = train_single_neuron(X_train, y_train, activation=activation, learning_rate=0.1, epochs=500)
        trained_models[activation] = (weights, bias)
        print(f"Trained weights: {weights}")
        print(f"Trained bias: {bias:.4f}")
    
    print("\n" + "="*60)
    print("CLASSIFICATION RESULTS")
    print("="*60)
    
    # Evaluate on training data
    print("\nTRAINING DATA PERFORMANCE:")
    for activation in activations:
        weights, bias = trained_models[activation]
        predictions = binary_classifier(X_train, weights, activation=activation, bias=bias)
        correct = sum(p == t for p, t in zip(predictions, y_train))
        accuracy = correct / len(y_train) * 100
        print(f"{activation.upper()}: {accuracy:.2f}% ({correct}/{len(y_train)})")
    
    # Evaluate on testing data
    print("\nTESTING DATA PERFORMANCE:")
    for activation in activations:
        weights, bias = trained_models[activation]
        predictions = binary_classifier(X_test, weights, activation=activation, bias=bias)
        correct = sum(p == t for p, t in zip(predictions, y_test))
        accuracy = correct / len(y_test) * 100
        print(f"{activation.upper()}: {accuracy:.2f}% ({correct}/{len(y_test)})")
    
    # Show sample test predictions
    print("\nSAMPLE TEST PREDICTIONS (first 10):")
    activation = 'sigmoid'  # Use sigmoid for sample display
    weights, bias = trained_models[activation]
    predictions = binary_classifier(X_test[:10], weights, activation=activation, bias=bias)
    for i in range(10):
        print(f"  Input: {X_test[i]}, True: {y_test[i]}, Predicted: {predictions[i]}")


if __name__ == "__main__":
    main()