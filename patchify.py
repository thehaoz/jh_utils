import numpy as np
from scipy.stats import multivariate_normal


def patchify(image: np.ndarray, kernel_size: tuple):

    img_height, img_width = image.shape
    tile_height, tile_width = kernel_size

    tiled_array = image.reshape(img_height // tile_height,
                                tile_height,
                                img_width // tile_width,
                                tile_width,
                                )
    tiled_array = tiled_array.swapaxes(1, 2)
    return tiled_array


def points_to_gaussian_heatmap(centers, height, width, scale):
    gaussians = []
    for y,x in centers:
        s = np.eye(2)*scale
        g = multivariate_normal(mean=(x,y), cov=s)
        gaussians.append(g)

    # create a grid of (x,y) coordinates at which to evaluate the kernels
    x = np.arange(0, width)
    y = np.arange(0, height)
    xx, yy = np.meshgrid(x,y)
    xxyy = np.stack([xx.ravel(), yy.ravel()]).T
    
    # evaluate kernels at grid points
    zz = sum(g.pdf(xxyy) for g in gaussians)

    img = zz.reshape((height,width))
    return img