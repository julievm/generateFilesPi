#!/usr/bin/env python3
import base64
import os
import numpy
import random
import string
import cv2
import argparse
import captcha.image

# similar to example code given
def main():


    width = 128
    height = 64
    count = 20
    output_dir = 'tryfiles'
    symbols = 'characters_julie.txt'

    # font_path = '.\EamonU.ttf'
    font_path = 'clouds-smile-too.regular.ttf'

    captcha_generator = captcha.image.ImageCaptcha(fonts=[font_path], width=width, height=height)

    # read in all the symbols
    symbols_file = open(symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    # check if dir exists, otherwise create it
    if not os.path.exists(output_dir):
        print("Creating output directory " + output_dir)
        os.makedirs(output_dir)

    for i in range(count):
        # get captchas of different lengths
        reallenth=random.randint(1,6)
        random_str = ''.join([random.choice(captcha_symbols) for j in range(reallenth)])
        image_path = os.path.join(output_dir, complete_captcha_name(reallenth, random_str, "", True))
        if os.path.exists(image_path):
            version = 1
            while os.path.exists(os.path.join(output_dir, complete_captcha_name(reallenth, random_str,str(version), False))):
                version += 1
            image_path = os.path.join(output_dir, complete_captcha_name(reallenth, random_str,str(version), False))

        image = numpy.array(captcha_generator.generate_image(random_str))
        cv2.imwrite(image_path, image)


# encode names to avoid the use of special characters
def complete_captcha_name(reallenth, random_str, version, path_exist):
    remain_length = 6 - reallenth
    remain_str = ''.join("-" for i in range(remain_length))

    if path_exist:
        str_tmp = random_str + remain_str
        str_encoded = base64.urlsafe_b64encode(str_tmp.encode()).decode()
        return str_encoded + '.png'
    else:
        str_tmp = random_str + remain_str + '_' + str(version)
        str_encoded = base64.urlsafe_b64encode(str_tmp.encode()).decode()
        return str_encoded + '.png'

if __name__ == '__main__':
    main()
