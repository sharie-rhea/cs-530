
"""
Simple Neural Network for XOR Problem

This script demonstrates a basic feedforward neural network implementation
to solve the XOR (exclusive or) logic gate problem. The network consists of
an input layer, one hidden layer, and an output layer, all using sigmoid
activation functions. Training is performed using numerical optimization
to minimize mean squared error.
"""

import numpy as np
import scipy.optimize as optimize

X = np.array([[0,0,1], [0,1,1], [1,0,1], [1,1,1]])  # XOR inputs with bias term (last column always 1)
y = np.array([[0], [1], [1], [0]])  # Corresponding XOR outputs

# Network architecture: 3 input neurons (2 inputs + 1 bias), 4 hidden neurons, 1 output neuron
L1 = 3
L2 = 4
L3 = 1

# Initialize weights randomly (good practice for breaking symmetry) and biases to zero
w1 = np.random.randn(L1 * L2)
w2 = np.random.randn(L2 * L3)
b1 = np.zeros(L2)
b2 = np.zeros(L3)

# Concatenate all parameters into a single flat array for the optimizer
params = np.concatenate([w1, b1, w2, b2])

def a(x):
    """Sigmoid activation function.

    Applies the sigmoid function to the input, which maps any real-valued number
    to a value between 0 and 1. Used as the activation function in neural networks.

    Args:
        x: Input value or array of values.

    Returns:
        The sigmoid of x: 1 / (1 + exp(-x))
    """
    return 1/(1+np.exp(-x))

def f(params, X):
    """Forward pass through the neural network.

    Computes the output of the neural network given the parameters and input data.
    The network has one hidden layer with sigmoid activations.

    Args:
        params: Flattened array containing all network parameters (weights and biases).
        X: Input data matrix.

    Returns:
        The network's output predictions.
    """
    w1 = params[:L1*L2].reshape(L1, L2)
    b1 = params[L1*L2:L1*L2+L2]
    w2 = params[L1*L2+L2:L1*L2+L2+L2*L3].reshape(L2, L3)
    b2 = params[-L3:]
    
    h = a(X.dot(w1) + b1)
    out = a(h.dot(w2) + b2)
    return out

def loss(params, X, y):
    """Mean squared error loss function.

    Computes the mean squared error between the network's predictions and the true targets.

    Args:
        params: Network parameters.
        X: Input data matrix.
        y: True target outputs.

    Returns:
        The mean squared error as a scalar value.
    """
    pred = f(params, X)
    return np.mean((pred - y)**2)

def grad(params, X, y):
    """Numerical gradient computation using finite differences.

    Approximates the gradient of the loss function with respect to the parameters
    using central finite differences. This is a simple but computationally expensive
    method compared to analytical gradients.

    Args:
        params: Network parameters.
        X: Input data matrix.
        y: True target outputs.

    Returns:
        Gradient vector with the same shape as params.
    """
    eps = 1e-7  # Small perturbation for numerical differentiation
    g = np.zeros_like(params)
    for i in range(len(params)):
        params_plus = params.copy()
        params_minus = params.copy()
        params_plus[i] += eps
        params_minus[i] -= eps
        g[i] = (loss(params_plus, X, y) - loss(params_minus, X, y)) / (2*eps)
    return g

# Train the network using L-BFGS-B optimization (quasi-Newton method, efficient for small problems)
result = optimize.minimize(loss, params, args=(X, y), method='L-BFGS-B', jac=grad, options={'maxiter': 1000, 'disp': True})

opt_params = result.x

# Test the trained network on a single input (0 XOR 0 should be 0)
test = np.array([[0,0,1]])
pred = f(opt_params, test)
print("Test:", pred[0][0])  # Print as scalar with default formatting

print("\nAll predictions:")
all_pred = f(opt_params, X)
for i, p in enumerate(all_pred):
    print(f"Input {X[i][:2]}: {p[0]:.6f}")  # Format to 6 decimal places