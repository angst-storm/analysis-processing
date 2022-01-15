from PIL import Image

crop_values = {
    'УГМК': [(0.427873, 0.281215, 0.584906, 0.7420)],
    'Ситилаб': [(0.532283, 0.338513, 0.644094, 0.742508), (0.544025, 0.233333, 0.635220, 0.39)],
    'INVITRO': [(0.295419, 0.234375, 0.456556, 0.784598)],
    'KDL': [(0.417323, 0.268673, 0.532283, 0.751394), (0.434169, 0.271413, 0.526646, 0.286986)],
    'Гемотест': [(0.569401, 0.507813, 0.670347, 0.803571), (0.567823, 0.256952, 0.675079, 0.413793)]
}


def crop_images(image_paths, lab):
    return [image.crop(crop_coords(crop_value, image)) for image, crop_value in
            zip([Image.open(image) for image in image_paths], crop_values[lab])]


def crop_coords(crop_value, image):
    image_w, image_h = image.size
    return crop_value[0] * image_w, crop_value[1] * image_h, crop_value[2] * image_w, crop_value[3] * image_h
