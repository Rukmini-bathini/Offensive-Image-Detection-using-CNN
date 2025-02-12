#!/usr/bin/env python
import sys
import argparse
import tensorflow as tf
import tensorflow.compat.v1 as tf
import numpy as np



from model import OpenNsfwModel, InputType
from image_utils import create_tensorflow_image_loader
from image_utils import create_yahoo_image_loader
import cv2
import time
import os

import numpy as np



def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="Path to the input image.\
                        Only jpeg images are supported.")

    parser.add_argument("-m", "--model_weights", required=True,
                        help="Path to trained model weights file")


    parser.add_argument("-i", "--input_type",
                        default=InputType.TENSOR.name.lower(),
                        help="input type",
                        choices=[InputType.TENSOR.name.lower(),
                                 InputType.BASE64_JPEG.name.lower()])

    args = parser.parse_args()

    model = OpenNsfwModel()

    with tf.compat.v1.Session() as sess:

        input_type = InputType[args.input_type.upper()]

        model.build(weights_path=args.model_weights, input_type=input_type)
        fn_load_image = None

        if input_type == InputType.TENSOR:
            fn_load_image = create_yahoo_image_loader()
        if input_type == InputType.BASE64_JPEG:
            import base64
            fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.global_variables_initializer())

        image = fn_load_image(args.input_file)
        predictions = sess.run(model.predictions, feed_dict={model.input: image})
        print("Results for '{}'".format(args.input_file))
        print("\tSafe score:\t{}\n\tNot Safe  score:\t{}".format(*predictions[0]))

if __name__ == "__main__":
    main(sys.argv)
