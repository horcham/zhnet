import numpy as np
import numpynet as nn

class LeNet(object):
    def __init__(self, imagesize, faltten_size, num_labels, lr=0.0001):

        self.N, self.C, self.W, self.H = imagesize
        self.num_labels = num_labels
        self.lr = lr

        self.graph = nn.Graph()
        self.X = nn.Placeholder()
        W0 = nn.Variable(nn.UniformInit([5, 5, self.C, 6]), lr=lr)
        self.graph.add_var(W0)
        W1 = nn.Variable(nn.UniformInit([5, 5, 6, 16]), lr=lr)
        self.graph.add_var(W1)
        WFC0 = nn.Variable(nn.UniformInit([faltten_size, 84]), lr=lr)
        self.graph.add_var(WFC0)
        WFC1 = nn.Variable(nn.UniformInit([84, 10]), lr=lr)
        self.graph.add_var(WFC1)

        conv0 = nn.Op(nn.Conv2d(padding='valid'), self.X, W0)
        self.graph.add_op(conv0)
        act0 = nn.Layer(nn.ReluActivator(), conv0)
        self.graph.add_layer(act0)

        pool0 = nn.Op(nn.MaxPooling(filter_h=2, filter_w=2, stride=2), act0)
        self.graph.add_op(pool0)

        conv1 = nn.Op(nn.Conv2d(padding='valid'), pool0, W1)
        self.graph.add_op(conv1)
        act1 = nn.Layer(nn.ReluActivator(), conv1)
        self.graph.add_layer(act1)

        pool1 = nn.Op(nn.MaxPooling(filter_h=2, filter_w=2, stride=2), act1)
        self.graph.add_op(pool1)

        fla = nn.Op(nn.Flatten(), pool1)
        self.graph.add_op(fla)

        FC0 = nn.Op(nn.Dot(), fla, WFC0)
        self.graph.add_op(FC0)
        Fact0 = nn.Layer(nn.ReluActivator(), FC0)
        self.graph.add_layer(Fact0)

        FC1 = nn.Op(nn.Dot(), Fact0, WFC1)
        self.graph.add_op(FC1)
        # Fact1 = nn.Layer(nn.IdentityActivator(), FC1)
        # self.graph.add_layer(Fact1)

        self.graph.add_loss(nn.Loss(nn.Softmax()))
        self.graph.add_optimizer((nn.AdamOptimizer()))

    def train(self, X_train, Y_train, X_test, Y_test, \
              epochs, batchsize=100):
        for epoch in range(epochs):
            batch_tr = nn.miniBatch(X_train, Y_train, batchsize)
            batch_te = nn.miniBatch(X_test, Y_test, batch_size=10)
            for i, (batch_x, batch_y) in enumerate(batch_tr):
                self.graph.forward(batch_x)
                self.graph.calc_loss(batch_y)
                self.graph.backward()
                self.graph.update()
                if i % 50 == 0:
                    print('epoch:{}/{}, batch:{}/{}, train loss:{}'.format(epoch, epochs, i, len(batch_tr), self.graph.loss))
            accuracy = self.graph.accuracy(batch_te)
            print('epoch:{}, accuracy:{}'.format(epoch, accuracy))






