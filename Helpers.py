import numpy as np

from skimage.transform import warp, SimilarityTransform, ProjectiveTransform

class Helpers:

    def __init__(self):

        pass

    @staticmethod

    def resize(image, width=None, height=None, inter='cubic'):

        if width is None and height is None:

            return image

        elif width is None:

            r = height / float(image.shape[0])

            dim = (int(image.shape[1] * r), height)

        else:

            r = width / float(image.shape[1])

            dim = (width, int(image.shape[0] * r))

        resized = warp(image, SimilarityTransform(scale=r), output_shape=dim, mode='edge', preserve_range=True, order=inter)

        resized = resized.astype(image.dtype)

        return resized

    @staticmethod

    def grab_contours(cnts):

        if len(cnts) == 2:

            cnts = cnts[0]

        elif len(cnts) == 3:

            cnts = cnts[1]

        else:

            raise ValueError('The length of the contour must be 2 or 3.')

        return cnts

    @staticmethod

    def orders(pts):

        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)

        rect[0] = pts[np.argmin(s)]

        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)

        rect[1] = pts[np.argmin(diff)]

        rect[3] = pts[np.argmax(diff)]

        return rect

    @staticmethod

    def transform(image, pts):

        rect = Helpers.orders(pts)

        (tl, tr, br, bl) = rect

        maxWidth = max(int(np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))),

                       int(np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))))

        maxHeight = max(int(np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))),

                        int(np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))))

        dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")

        M = ProjectiveTransform()

        M.estimate(src=rect, dst=dst)

        warped = warp(image, M, output_shape=(maxHeight, maxWidth), mode='edge', preserve_range=True)

        return warped.astype(image.dtype)

