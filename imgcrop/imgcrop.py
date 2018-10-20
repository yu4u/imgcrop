import math
import numpy as np
import cv2


def get_cropper(patch_size=128, scale=(1.0, 1.0), rotate=(0, 0), distort=0.0, flip=0, margin=0):
    def random_crop(img, points=None):
        src_points = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float32)

        # flip
        if np.random.uniform(0, 1.0) > flip:
            dst_points = np.array([[1, 1], [1, 0], [0, 0], [0, 1]], dtype=np.float32) * patch_size
        else:
            dst_points = np.array([[0, 1], [0, 0], [1, 0], [1, 1]], dtype=np.float32) * patch_size

        # random scaling
        sampled_scale = np.random.uniform(scale[0], scale[1])
        src_points *= patch_size * sampled_scale / 2

        # random rotation
        theta = np.random.uniform(rotate[0] * math.pi * 2 / 360, rotate[1] * math.pi * 2 / 360)
        c, s = np.cos(theta), np.sin(theta)
        r = np.array([[c, -s], [s, c]], dtype=np.float32)
        src_points = np.dot(r, src_points.T).T

        # random perspective distortion
        distort_in_px = patch_size * sampled_scale * distort / 2
        src_points += np.random.uniform(-distort_in_px, distort_in_px, src_points.shape)

        # random shift
        x_min, y_min = src_points.min(axis=0)
        x_max, ymax = src_points.max(axis=0)
        w, h = x_max - x_min, ymax - y_min

        if isinstance(img, list):
            img_h, img_w = img[0].shape[:2]
        else:
            img_h, img_w = img.shape[:2]

        x = np.random.uniform(-margin, img_w - w + margin)
        y = np.random.uniform(-margin, img_h - h + margin)
        src_points[:, 0] += x - x_min
        src_points[:, 1] += y - y_min

        # get perspective transformation
        m = cv2.getPerspectiveTransform(src_points, dst_points)

        # perform random cropping
        # TODO: enable to select cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_CUBIC
        if isinstance(img, list):
            cropped_img = [cv2.warpPerspective(i, m, (patch_size, patch_size), flags=cv2.INTER_CUBIC,
                                               borderMode=cv2.BORDER_REPLICATE) for i in img]
        else:
            cropped_img = cv2.warpPerspective(img, m, (patch_size, patch_size), flags=cv2.INTER_CUBIC,
                                              borderMode=cv2.BORDER_REPLICATE)

        if points is None:
            return cropped_img, src_points, m
        else:
            output_points = cv2.perspectiveTransform(points.reshape(-1, 1, 2), m).reshape(-1, 2)
            return cropped_img, output_points, src_points, m
    return random_crop
