import torch
import torch.optim as optim
from torchvision import datasets, transforms
from simple_mnist import Model, train, evaluate

import numpy as np
import pandas as pd
import os, glob
import boto3
import argparse

def main(lr: float,
         momentum: float,
         epochs: int = 50,
         upload_to_s3: bool = False,):

    transf = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.1307,), (0.3081,))])
    trainvalset = datasets.MNIST(root='/mnist', train=True, download=True, transform=transf)

    # Split train data into train and validation set
    train_size = int(len(trainvalset) * 0.8) # use 80% as training data 
    val_size = len(trainvalset) - train_size # and 20% as validation data
    trainset, valset = torch.utils.data.random_split(trainvalset, [train_size, val_size], generator=torch.Generator().manual_seed(1008))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
    valloader = torch.utils.data.DataLoader(valset, batch_size=64, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Model()
    model.to(device)

    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum)

    metrics = np.zeros((epochs, 3))
    for epoch in range(epochs):
        losses = train(model, trainloader, optimizer, epoch, device=device)
        val_loss, val_accuracy = evaluate(model, valloader, device=device)
        print(f"\nVal set: Average loss: {val_loss:.4f}, Accuracy: {val_accuracy:.1f}%\n")
        metrics[epoch] = [np.mean(losses), val_loss, val_accuracy]

    df = pd.DataFrame(data=metrics, columns=["train_loss", "val_loss", "val_accuracy"])
    filename = f"metrics_lr{lr:0.4f}_m{momentum:0.4f}.csv"
    df.to_csv(filename, header=True, index=False)

    # save the result in S3
    if upload_to_s3:
        transfer_to_s3(filename, filename)

def transfer_to_s3(src, key):
    """
    Given a file path, upload and save the file in S3 with the given key
    Parameters
    ----------
    src: str
        File name of the original file
    key: str
        Key of the file used in S3
    """
    print("Saving results in S3 bucket...")
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(os.environ["BUCKET_NAME"])
    bucket.upload_file(src, key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lr", type=float,
                        help="Learning rate")
    parser.add_argument("-m", "--momentum", type=float,
                        help="Momentum")
    parser.add_argument("-e", "--epochs", type=int, default=50,
                        help="Total number of training epochs")
    parser.add_argument("-u", "--uploadS3", type=bool, default=False,
                        help="If true, the metric data is saved in S3")
    args = parser.parse_args()

    main(args.lr, args.momentum, args.epochs, args.uploadS3)
