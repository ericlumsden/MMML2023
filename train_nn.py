import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from dataclasses import dataclass

conn = sqlite3.connect('./ncaa.db')
df = pd.read_sql("SELECT * FROM menstraining", conn)
df = df.drop(['index'], axis=1)
df.replace('', np.nan, inplace=True)
df.dropna(inplace=True)
df = df.astype(float)

numpy_df = df.to_numpy()
np.random.shuffle(numpy_df)
Y = numpy_df[:, -1]
X = numpy_df[:, :-1]
X_train = X[:300, :]
X_test = X[300:, :]
Y_train = Y[:300].T
Y_test = Y[300:].T


n_hidden = 108
num_iterations = 5000

@dataclass
class NeuralNetwork:
    bias = 0.5
    errors = []

    data_set: any
    training_num: int
    iterations: int
    learning_rate: float
    l1_num: int

    def split(self):
        X, Y = self.data_set[:, :-1], self.data_set[:, -1].T
        X_train, X_test = X[:self.training_num], X[self.training_num:]
        Y_train, Y_test = Y[:self.training_num], Y[self.training_num:]
        return X_train, X_test, Y_train.reshape((len(Y_train),1)), Y_test.reshape((len(Y_test)),1)

    def weights(self, rows, cols):
        return np.random.rand(rows, cols) - 0.5 # random weights between -0.5 and 0.5; columns have to equal rows in X_train, rows have to equal 

    # Will use a sigmoid function for predicting which team will win
    def sigmoid(self, x):
        return 1 / (1 + np.exp(x))
    
    def deriv_sigmoid(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    
    def forward(self, weights, X_train_matrix, Y_train_matrix):
        l1_input = np.dot(X_train_matrix, weights) + self.bias
        l1_output = self.sigmoid(l1_input)
        error = 2 * (l1_output - Y_train_matrix)
        return l1_output, error
    
    def backprop(self, weights, error):
        weights -= self.deriv_sigmoid(error) * self.learning_rate
        return weights

    def train(self):
        X_train, X_test, Y_train, Y_test = self.split()
        random_weights = self.weights(X_train.shape[1], self.l1_num)
        for iteration in range(self.iterations):
            l1_output, error = self.forward(random_weights, X_train, Y_train)
            self.errors.append(np.sum(error))
            random_weights = self.backprop(random_weights, error)
        return random_weights
    
    def test(self, weights, X_test_matrix=X_test, Y_test_matrix=Y_test):
        X_train, X_test, Y_train, Y_test = self.split()
        test_output, test_error = self.forward(weights, X_test, Y_test)
        return test_output, test_error

nn = NeuralNetwork(numpy_df, 300, 5000, 0.0005, 108)
nn.train()
nn.test()

plt.plot(range(len(nn.errors)), nn.errors)
plt.savefig("./errors.png")


'''
class NeuralNetMLP(object):
    def __init__(self, n_hidden=30, l2=0., epochs=100, eta=0.001, shuffle=True, minibatch_size=1, seed=None):
        self.random = np.random.RandomState(seed)
        self.n_hidden = n_hidden
        self.l2 = l2
        self.epochs = epochs
        self.eta = eta
        self.shuffle = shuffle
        self.minibatch_size = minibatch_size
    
    def _onehot(self, y, n_classes):
        onehot = np.zeros((n_classes, y.shape[0]))
        for idx, val in enumerate(y.astype(int)):
            onehot[val, idx] = 1.
        return onehot.T
    
    def _sigmoid(self, z):
        return 1. / (1. + np.exp(-np.clip(z, -250, 250)))
    
    def _forward(self, X):
        z_h = np.dot(X, self.w_h) + self.b_h
        a_h = self._sigmoid(z_h)
        z_out = np.dot(a_h, self.w_out) + self.b_out
        a_out = self._sigmoid(z_out)
        return z_h, a_h, z_out, a_out
    
    def _compute_cost(self, y_enc, output):
        L2_term = (self.l2 * (np.sum(self.w_h ** 2.) + np.sum(self.w_out ** 2.)))
        term1 = -y_enc * np.log(output)
        term2 = (1. - y_enc) * np.log(1. - output)
        cost = np.sum(term1 - term2) + L2_term
        return cost
    
    def predict(self, X):
        z_h, a_h, z_out, a_out = self._forward(X)
        y_pred = np.argmax(z_out, axis=1)
        return y_pred
    
    def fit(self, X_train, y_train, X_valid, y_valid):
        n_output = np.unique(y_train).shape[0]
        n_features = X_train.shape[1]
        self.b_h = np.zeros(self.n_hidden)
        self.w_h = self.random.normal(loc=0.0, scale=0.1, size=(n_features, self.n_hidden))
        self.b_out = np.zeros(n_output)
        self.w_out = self.random.normal(loc=0.0, scale=0.1, size=(self.n_hidden, n_output))
        epoch_strlen = len(str(self.epochs))
        self.eval_ = {'cost': [], 'train_acc': [], 'valid_acc': []}
        y_train_enc = self._onehot(y_train, n_output)
        for i in range(self.epochs):
            indices = np.arange(X_train.shape[0])
            if self.shuffle:
                self.random.shuffle(indices)
            
            for start_idx in range(0, indices.shape[0] - self.minibatch_size + 1, self.minibatch_size):
                batch_idx = indices[start_idx:start_idx + self.minibatch_size]
                z_h, a_h, z_out, a_out = self._forward(X_train[batch_idx])

                sigma_out = a_out - y_train_enc[batch_idx]
                sigmoid_derivative_h = a_h * (1. - a_h)
                sigma_h = (np.dot(sigma_out, self.w_out.T) * sigmoid_derivative_h)
                grad_w_h = np.dot(X_train[batch_idx].T, sigma_h)
                grad_b_h = np.sum(sigma_h, axis=0)
                grad_w_out = np.dot(a_h.T, sigma_out)
                grad_b_out = np.sum(sigma_out, axis=0)
                delta_w_h = (grad_w_h + self.l2*self.w_h)
                delta_b_h = grad_b_h
                self.w_h -= self.eta * delta_w_h
                self.b_h -= self.eta * delta_b_h

                delta_w_out = (grad_w_out + self.l2*self.w_out)
                delta_b_out = grad_b_out
                self.w_out -= self.eta * delta_w_out
                self.b_out -= self.eta * delta_b_out
        
            z_h, a_h, z_out, a_out = self._forward(X_train)
            cost = self._compute_cost(y_enc=y_train_enc, output=a_out)
            y_train_pred = self.predict(X_train)
            y_valid_pred = self.predict(X_valid)

            train_acc = ((np.sum(y_train == y_train_pred)).astype(np.float64) / X_train.shape[0])
            valid_acc = ((np.sum(y_valid == y_valid_pred)).astype(np.float64) / X_valid.shape[0])
            self.eval_['cost'].append(cost)
            self.eval_['train_acc'].append(train_acc)
            self.eval_['valid_acc'].append(valid_acc)
        
        return self

nn = NeuralNetMLP(n_hidden=100, l2=0.01, epochs=10000, eta=0.0005, minibatch_size=100, shuffle=True, seed=1)
nn.fit(X_train=X[:300], y_train=Y[:300], X_valid=X[300:], y_valid=Y[300:])

#plt.plot(range(nn.epochs), nn.eval_['cost'])
plt.plot(range(nn.epochs), nn.eval_['train_acc'], color='blue', label='train')
plt.plot(range(nn.epochs), nn.eval_['valid_acc'], color='red', label='valid')
plt.legend()
plt.show()
'''