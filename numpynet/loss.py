import numpy as np
# import minpy.numpy as np

class Loss(object):
    '''
    ----------- |                    F = loss
    op or layer | --------> output ==========  label
    -----------	| <-----------------  d F/d output
    '''
    def __init__(self, lossfunc):
        self.lossfunc = lossfunc

    def __repr__(self):
        return "{}, loss:{}".format(self.lossfunc.name, self.lossfunc.loss)

    def forward(self, output, Y):
        self.X1 = self.output = output
        self.X2 = self.Y = Y
        self.loss = self.lossfunc.forward(output, Y)
        self.F = self.loss

    def backward(self):
        self.dF = self.lossfunc.backward()
        self.D = self.dF

    def predict(self, X):
        return self.lossfunc.predict(X)


class MSE(object):
    def __init__(self):
        self.name = 'MSE'
    def forward(self, output, Y):
        self.output = output
        self.Y = Y
        self.loss = 1.0/2 * np.sum(np.dot((output.value - Y.value), (output.value - Y.value).T))
        return self.loss
    def backward(self):
        return self.Y.value - self.output.value
    def predict(self):
        return output

class Softmax(object):
    def __init__(self):
        self.name = 'Softmax'
    def _softmax(self, X):
        max_X = np.max(X, axis=1, keepdims=True) + 1e-6
        # print(np.exp(X / max_X) / (np.sum(np.exp(X / max_X), axis=1, keepdims=True) + 1e-6)[0])
        return np.exp(X - max_X) / (np.sum(np.exp(X - max_X), axis=1, keepdims=True) + 1e-6)
    def forward(self, output, Y):
        self.output = output
        self.Y = Y
        self.loss = - np.sum(Y.value * np.log(self._softmax(output.value) + 1e-6))
        return self.loss
    def backward(self):
        return self._softmax(self.output.value) - self.Y.value
    def predict(self, X):
        return self._softmax(X.value)



