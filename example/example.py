import argparse
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
from imgcrop import get_cropper


def get_args():
    parser = argparse.ArgumentParser(description="Demo script for random image cropping",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--patch_size", type=int, default=256,
                        help="output patch image size")
    parser.add_argument("--scale", nargs=2, type=float, default=[0.8, 1.2],
                        help="scale range in sampling")
    parser.add_argument("--rotate", nargs=2, type=int, default=[-60, 60],
                        help="rotation range in sampling")
    parser.add_argument("--distort", type=float, default=0.2,
                        help="distortion strength for perspective transformation")
    parser.add_argument("--flip", type=float, default=0.5,
                        help="horizontal flip probability")
    parser.add_argument("--margin", type=int, default=0,
                        help="margin around original image")
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    base_path = Path(__file__).resolve().parent
    original_img = cv2.imread(str(base_path.joinpath("lenna.png")))
    mask_img = cv2.imread(str(base_path.joinpath("lenna_mask.png")))
    out_img = np.zeros((args.patch_size, args.patch_size * 4, 3), dtype=np.uint8)
    random_crop = get_cropper(patch_size=args.patch_size, scale=args.scale, rotate=args.rotate, distort=args.distort,
                              flip=args.flip, margin=args.margin)
    df = pd.read_csv(base_path.joinpath("lenna.csv"), index_col=0)
    points = df[["x", "y"]].values.astype(np.float32)

    while True:
        cropped_img, output_points, src_points, m = random_crop([original_img, mask_img], points)
        img_with_region = original_img.copy()

        # draw cropped region
        for i in range(len(src_points)):
            x1, y1 = src_points[i].astype(np.int)
            x2, y2 = src_points[(i + 1) % len(src_points)].astype(np.int)
            cv2.line(img_with_region, (x1, y1), (x2, y2), (0, 0, 0), 3, cv2.LINE_AA)
            cv2.line(img_with_region, (x1, y1), (x2, y2), (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img_with_region, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(img_with_region, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # original image with cropped region
        out_img[:, :args.patch_size] = cv2.resize(img_with_region, (args.patch_size, args.patch_size))

        # cropped image
        out_img[:, args.patch_size:args.patch_size * 2] = cropped_img[0]

        # cropped mask image
        out_img[:, args.patch_size * 2:args.patch_size * 3] = cropped_img[1]

        # cropped image with landmarks
        for x, y in output_points.astype(np.int):
            cv2.circle(cropped_img[0], (x, y), 3, (0, 255, 255))

        out_img[:, args.patch_size * 3:args.patch_size * 4] = cropped_img[0]
        cv2.imshow("out", out_img)
        key = cv2.waitKey(-1)

        # "q": quit
        if key == 113:
            return 0


if __name__ == '__main__':
    main()
