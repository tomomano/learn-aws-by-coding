import torch
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from matplotlib import pyplot as plt

# custom functions and classes
from simple_mnist import Model, train, evaluate

def main():
    transf = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.1307,), (0.3081,))])

    trainvalset = datasets.MNIST(root='./data', train=True, download=True, transform=transf)

    # Split train data into train and validation set
    train_size = int(len(trainvalset) * 0.8)
    val_size = len(trainvalset) - train_size
    trainset, valset = torch.utils.data.random_split(trainvalset, [train_size, val_size])
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
    valloader = torch.utils.data.DataLoader(valset, batch_size=64, shuffle=True)

    testset = datasets.MNIST(root='./data', train=False, download=True, transform=transf)
    testloader = torch.utils.data.DataLoader(testset, batch_size=1000, shuffle=False)

    model = Model()
    model.to("cuda")

    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

    train_losses = []
    for epoch in range(5):
        losses = train(model, trainloader, optimizer, epoch)
        train_losses = train_losses + losses
        test_loss, test_accuracy = evaluate(model, testloader)
        print(f"\nTest set: Average loss: {test_loss:.4f}, Accuracy: {test_accuracy:.1f}%\n")
    
    torch.save(model.state_dict(), "mnist_cnn.pt")
