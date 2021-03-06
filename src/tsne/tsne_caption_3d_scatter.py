 #####################################################################################
 # MIT License                                                                       #
 #                                                                                   #
 # Copyright (C) 2019 Charly Lamothe, Guillaume Ollier, Balthazar Casalé             #
 #                                                                                   #
 # This file is part of Joint-Text-Image-Representation.                             #
 #                                                                                   #
 #   Permission is hereby granted, free of charge, to any person obtaining a copy    #
 #   of this software and associated documentation files (the "Software"), to deal   #
 #   in the Software without restriction, including without limitation the rights    #
 #   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       #
 #   copies of the Software, and to permit persons to whom the Software is           #
 #   furnished to do so, subject to the following conditions:                        #
 #                                                                                   #
 #   The above copyright notice and this permission notice shall be included in all  #
 #   copies or substantial portions of the Software.                                 #
 #                                                                                   #
 #   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
 #   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        #
 #   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     #
 #   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          #
 #   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
 #   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   #
 #   SOFTWARE.                                                                       #
 #####################################################################################

import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


class TSNECaption3DScatter(object):
    """
    Build the embedded t-SNE space of a caption representation,
    and output the representation in a 3D scatter image.

    References
    ----------
    https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    https://www.kaggle.com/jeffd23/visualizing-word-vectors-with-t-sne
    """
    
    def __init__(self, activations, text_representation,
        output_dimension=10, output_name='tsne_caption_3d_scatter.jpg',
        output_directory='./', perplexity=50, iterations=5000, caption_size=10,
        output_size=(50, 50), quality=100):
        
        """
        Parameters
        ---------
        activations : numpy.ndarray
            Activations of a trained caption model

        text_representation : TextRepresentation
            Caption dataset representation

        output_dimension : int (default: 10)
            Number of small captions in output image

        output_name : str, optional (default: tsne_caption_3d_scatter.jpg)
            Name of output image file

        output_directory : str, optional (default: ./)
            Destination directory for output image

        perplexity : int, optional (default: 50)
            t-SNE perplexity

        iterations : int, optional (default: 5000)
            Number of iterations in tsne algorithm

        caption_size : (int), optional (default: 10)
            The size of a single caption

        output_size : (int, int), optional (default: (50, 50))
            The size (width, height) of the output image

        quality : int, optional (default: 100)
            Quality of the output image
        """
        
        self.activations = activations
        self.text_representation = text_representation
        self.output_dimension = output_dimension
        self.output_name = output_name
        self.output_directory = output_directory
        self.perplexity = perplexity
        self.iterations = iterations
        self.caption_size = caption_size
        self.output_size = output_size
        self.quality = quality
        self.to_plot = np.square(self.output_dimension)

        if self.output_dimension == 1:
            raise ValueError("Output scatter dimension 1x1 not supported.")

        if not os.path.exists(self.output_directory):
            raise ValueError("'{}' not a valid directory.".format(self.output_directory))

    def generate(self):
        X_3d = self._generate_tsne()
        self._plot_tsne_scatter(X_3d, self.text_representation._texts, self.output_dimension)

    def _generate_tsne(self):
        tsne = TSNE(perplexity=self.perplexity, n_components=3, init='pca', n_iter=self.iterations)
        X_3d = tsne.fit_transform(np.array(self.activations)[0:self.to_plot,:])
        X_3d -= X_3d.min(axis=0)
        X_3d /= X_3d.max(axis=0)
        return X_3d

    def _plot_tsne_scatter(self, X_3d, texts, output_dimension):
        x = []
        y = []
        z = []
        for value in X_3d:
            x.append(value[0])
            y.append(value[1])
            z.append(value[2])

        fig = plt.figure(figsize=self.output_size)

        ax = fig.add_subplot(111, projection='3d')

        for i in range(len(x)):
            ax.scatter(x[i], y[i], z[i])
            ax.text(x[i], y[i], z[i], texts[i], size=self.caption_size, zorder=1, color='k')

        plt.savefig(self.output_name, quality=self.quality)
