import numpy as np
import torch
from torch.autograd import Variable
from torch import nn
np.set_printoptions(precision=3)

from datasets import MixtureOfBlocks, mixture_of_blocks


if __name__ == '__main__':
    num_samples = 6000
    batch_size = 64
    seed = 0
    im_shape = (28, 28)
    num_epochs = 10
    learning_rate = 0.01 

    loader = mixture_of_blocks(num_samples, batch_size, seed)
    if False:  # neural net
        classifier = nn.Sequential(
                nn.Linear(int(np.prod(im_shape)), 400),
                nn.LeakyReLU(),
                nn.Linear(400, 200),
                nn.LeakyReLU(),
                nn.Linear(200, 50),
                nn.LeakyReLU(),
                nn.Linear(50, MixtureOfBlocks.num_labels),
                )
    else:  # logistic regression
        classifier = nn.Sequential(
                nn.Linear(int(np.prod(im_shape)), MixtureOfBlocks.num_labels),
                )
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(classifier.parameters(), learning_rate)

    for e in range(num_epochs):
        for i, (x, y) in enumerate(loader):
            x = Variable(x.view(batch_size, -1), requires_grad=False)
            y = Variable(y.long().squeeze(), requires_grad=False)
            yhat = torch.max(classifier(x), 1)[1]
            acc = yhat.eq(y).float().sum() / len(y)
            optimizer.zero_grad()
            loss = loss_fn(classifier(x), y)
            loss.backward()
            optimizer.step()
            print(e, i, *loss.data.numpy(), *acc.data.numpy())
