import cv2 as cv
import numpy as np
from dipy.segment.mask import median_otsu
from pydicom import Dataset
from sklearn.cluster import KMeans


class Plugin:

    def initialize(self):
        pass

    def process(self, img, n_clusters=3, **kwargs):
        if isinstance(img, Dataset):
            img = img.pixel_array
        img, mask = median_otsu(img, 5, 10)
        x = img.reshape((-1, 1))
        k_means = KMeans(n_clusters=n_clusters, random_state=0).fit(x)
        c_index = np.argmax(k_means.cluster_centers_.reshape((-1)))
        flat = np.full(img.shape[0] * img.shape[1], 0)
        flat[k_means.labels_ == c_index] = 1
        mask = flat.reshape(img.shape)
        k1 = np.ones((3, 3), np.uint16)
        k2 = np.ones((5, 5), np.uint16)
        mask = cv.erode(mask, k2, iterations=1)
        mask = cv.dilate(mask, k1, iterations=1)
        mask = cv.erode(mask, k2, iterations=2)
        mask = cv.dilate(mask, k1, iterations=5)
        return mask

    def destroy(self):
        pass
