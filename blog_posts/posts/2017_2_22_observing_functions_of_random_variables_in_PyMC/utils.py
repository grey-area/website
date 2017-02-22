import scipy.stats as stats
from IPython.display import Image
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm

def display_graph(model):
    graph = pm.graph.graph(model)
    return Image(graph.create_png())

def plot_2d_pdf(x1, x2, xmin=None, xmax=None, ymin=None, ymax=None):
    if xmin is None:
        xmin = x1.min()
    if xmax is None:
        xmax = x1.max()
    if ymin is None:
        ymin = x2.min()
    if ymax is None:
        ymax = x2.max()

    xx, yy = np.mgrid[xmin:xmax:70j, ymin:ymax:70j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x1, x2])
    kernel = stats.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)

    plt.contourf(xx, yy, f, cmap='Blues')
    plt.xlabel("alpha")
    plt.ylabel("beta")

def plot_lighthouse_posterior(alphas, betas, data, true_alpha, true_beta):

    # Plot the kde of the posterior
    xmin = np.percentile(data, 20)
    xmax = np.percentile(data, 80)
    ymin = -5.0
    ymax = betas.max()
    plot_2d_pdf(alphas, betas, xmin, xmax, ymin, ymax)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    # Plot the true value
    plt.scatter([true_alpha], [true_beta], c="k", s=50)

    # Plot the coastline
    xs = np.linspace(xmin, xmax, 3)
    plt.plot(xs, np.zeros_like(xs), c="k", linewidth=5)

    # Plot the data points
    plt.scatter(data, np.zeros_like(data), c="yellow", s=10, zorder=10)
