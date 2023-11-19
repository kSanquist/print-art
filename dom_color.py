from __future__ import print_function
import numpy as np
import scipy
import scipy.misc
import scipy.cluster


# Gets the dominant color of an image and returns the rgb values of said color
def dominant_color(image, n_clusters):
    NUM_CLUSTERS = n_clusters

    ar = np.asarray(image)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes= scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)[0]

    vecs = scipy.cluster.vq.vq(ar, codes)[0]
    counts = scipy.histogram(vecs, len(codes))[0]

    index_max = scipy.argmax(counts)
    peak = codes[index_max]

    rgb = (int(peak[0]), int(peak[1]), int(peak[2]))
    return rgb