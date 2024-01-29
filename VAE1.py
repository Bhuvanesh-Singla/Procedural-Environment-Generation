import os
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np

directory = "/kaggle/input/procedural-environment-generation/dataset/dataset"
img_shape = (256,256,1)
img_paths = [directory + '/' + file for file in os.listdir(directory)]
img_paths = img_paths[:-6]
img_paths = np.sort(img_paths)

def load_images(img_paths):
    for image in img_paths:
        img = Image.open(image)
        img_array = np.array(img)
        img_array_normalized = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array))
        
        yield np.transpose(np.expand_dims(np.float32(img_array_normalized), axis = 2),(2,0,1))

def show_images(imgs, grid_size=5):
    fig = plt.figure(figsize = (9,9))
    plt.axis("off")
    plt.title("sample training images")
    images = load_images(imgs)
    columns = rows = grid_size
    for i in range(1, columns*rows +1):
        
        fig.add_subplot(rows, columns, i)
        plt.axis("off")
        plt.imshow(np.transpose(next(images), (1,2,0)), cmap = 'gray')
        
    plt.show()
class Terrain(Dataset):
    def __init__(self, img_paths):
        self.img_paths = img_paths
    
    def __len__(self):
        return len(self.img_paths)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        image = next(load_images([self.img_paths[idx]]))
        return image
    
dataset = Terrain(img_paths)
batchsize = 64
shuffle = True

Batches = DataLoader(dataset = dataset, batch_size = batchsize, shuffle = shuffle)

dev = 'cuda' if torch.cuda.is_available() == True else 'cpu'
device = torch.device(dev)
print(dev)

class VAE(nn.Module):
    def __init__(self, input_channels, latent_dim):
        super(VAE, self).__init__()

        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten()
        )

        self.mean_layer = nn.Linear(256 * (256 // 16) * (256 // 16), latent_dim)
        self.log_var_layer = nn.Linear(256 * (256 // 16) * (256 // 16), latent_dim)

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256 * (256 // 16) * (256 // 16)),
            nn.ReLU(),
            nn.Unflatten(1, (256, 256 // 16, 256 // 16)),
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, input_channels, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        mean = self.mean_layer(x)
        log_var = self.log_var_layer(x)

        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        z = mean + eps * std

        xreconstructed = self.decoder(z)

        return xreconstructed, mean, log_var

input_channels = 1 
latent_dim = 64
learning_rate = 3e-4
num_epochs = 25

vae = VAE(input_channels, latent_dim)
criterion = nn.MSELoss()
optimizer = optim.Adam(vae.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for data in Batches:
        inputs = data
        reconstructions, mean, log_var = vae(inputs)

        reconstruction_loss = criterion(reconstructions, inputs)
        kl_divergence = -0.5 * torch.sum(1 + log_var - mean.pow(2) - log_var.exp())
        loss = reconstruction_loss + kl_divergence

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

with torch.no_grad():
    vae.eval()  
    z_sample = torch.randn(1, latent_dim)
    generated_height_map = vae.decoder(z_sample).squeeze()

generated_height_map_np = (generated_height_map * 255).clamp(0, 255).numpy()
plt.imshow(generated_height_map_np, cmap='gray')
plt.title('Generated Height Map')
plt.colorbar()
plt.show()
