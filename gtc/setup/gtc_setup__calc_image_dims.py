#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np


def calc_image_dims(
    img_tmp: np.ndarray,
    p: dict
) -> dict:

    """Calculate the image dimension and area."""

    img_res_in_um = p['img_res_in_um_per_px']
    target_res_height = p['plot_props']['output_image_dim']

    ####

    height, width = img_tmp.shape[0:2]  # !!!NOTE opencv changes axis order: [rows, cols] = [height, width]

    rescale_fac = float(height) / float(target_res_height)  # calculate output dimensions for true to scale saving of images
    target_res_width = int(float(width) / rescale_fac)

    img_dict = {'dims': (height, width),
                'rows': height,
                'cols': width,
                'area_px2': width * height,  # image area in square pixel and micrometer
                'area_um2': float(width * height) * img_res_in_um ** 2,
                'dims_out': (target_res_height, target_res_width)}

    print('Image dimensions: rows (= height) = %d [px], cols (= width) = %d [px]' % (height, width))

    print('Resolution of the microscope image = %3.4e [um2/px]' % p['img_res_in_um_per_px'] ** 2)

    print('Relative area = 1.00 [-]')
    print('Absolute area = %3.2e [px2] = %3.2e [um2] = %3.2f [mm2]'
          % (img_dict['area_px2'], img_dict['area_um2'], img_dict['area_um2'] / 10 ** 6))

    print('Output graphics are resized to %dpx x %dpx'
          % (img_dict['dims_out'][0], img_dict['dims_out'][1]))

    return img_dict

#################################
