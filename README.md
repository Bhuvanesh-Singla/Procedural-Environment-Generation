# Procedural Environment Generation

We collected earth heightmap images by scraping various websites. After preprocessing and cleaning the images, we created our dataset which has been hosted on Kaggle. It can be accessed <a href="https://www.kaggle.com/datasets/bhuvaneshsingla/procedural-environment-generation" target="_blank">here</a>.

Then we used `DC GAN model architecture`, and trained it with `Wasserstein loss` on the collected images. This gave us generated heightmap images similar to heightmaps of the earth that was collected.

After that, we applied Neural Style Transfer using a pretrained `VGG-19 CNN` Architecture on the generated heightmap images to achieve realistic as well abstract artistic results for a diverse variety of terrains. (Examples present in `3D Terrains` folder)

Upon completing Neural Style Transfer on our generated heightmaps, we used `Unity` to render our final results. We first plotted our height map in grayscale and then added the style-transferred height map on it as a terrain layer. This led to us creating our own explorable 3-Dimensional Terrains.

The link to our project report is given <a href="https://docs.google.com/document/d/17xS5INiF-unRQuC3KZDy22f_GUC0L1R421J8lmPDmbw/edit#heading=h.ot7vjq9fno6a" target="_blank">here</a>, where you can find a detailed account of our abstract, literature survey, methodology, results, challenges faced, and potential future work.
