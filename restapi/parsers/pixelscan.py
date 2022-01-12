import sys
from PIL import Image

data_ugmk = [
    [0.089623, 0.070078, (202, 80, 25)],  # Оранжевый
    [0.113208, 0.076752, (246, 246, 246)],  # Белый
    [0.058176, 0.072303, (255, 255, 255)],  # Белый
    [0.231132, 0.087875, (237, 134, 35)],  # Оранжевый
    [0.235849, 0.077864, (253, 250, 254)]  # Белый
]

data_citilab = [
    [0.897638, 0.033296, (219, 8, 68)],  # Розовый
    [0.888189, 0.033296, (255, 255, 255)],  # Белый
    [0.869291, 0.035516, (218, 8, 73)],  # Розовый
    [0.818898, 0.038846, (1, 78, 162)],  # Синий
    [0.897638, 0.039956, (4, 78, 150)]  # Синий
]

data_invitro = [
    [0.042654, 0.022321, (2, 163, 186)],  # Бирюзовый
    [0.071090, 0.017857, (249, 251, 252)],  # Белый
    [0.090047, 0.020089, (2, 164, 184)],  # Бирюзовый
    [0.097946, 0.017857, (254, 254, 255)],  # Белый
    [0.199052, 0.034598, (3, 164, 180)]  # Бирюзовый
]

data_kdl = [
    [0.138583, 0.043478, (159, 28, 98)],  # Фиолетово-розовый
    [0.110236, 0.071349, (113, 34, 96)],  # Фиолетовый
    [0.143307, 0.066890, (140, 30, 96)],  # Фиолетовый
    [0.111811, 0.055741, (236, 102, 29)],  # Оранжевый
    [0.188976, 0.078037, (0, 0, 0)]  # Черный
]

data_gemotest = [
    [0.099456, 0.025638, (1, 125, 58)],  # Зеленый
    [0.112757, 0.022902, (253, 253, 254)],  # Белый
    [0.129760, 0.032250, (2, 127, 61)],  # Зеленый
    [0.139647, 0.036714, (253, 254, 254)],  # Белый
    [0.376817, 0.025421, (6, 122, 62)],  # Зеленый
]


def get_scan_result(image_path):
    print(f'[PIXELSCAN] Processing image "{image_path}"')

    # загружаем картинку
    image = Image.open(image_path)

    # рассчитываем расстояние до каждой клиники
    ugmk_error = get_pixelscan_result(image, data_ugmk)
    citilab_error = get_pixelscan_result(image, data_citilab)
    invitro_error = get_pixelscan_result(image, data_invitro)
    kdl_error = get_pixelscan_result(image, data_kdl)
    gemotest_error = get_pixelscan_result(image, data_gemotest)

    dic = {
        ugmk_error: 'УГМК',
        citilab_error: 'Ситилаб',
        invitro_error: 'INVITRO',
        kdl_error: 'KDL',
        gemotest_error: 'Гемотест'
    }

    print(f'[PIXELSCAN] Errors list:'
          f' - УГМК: {ugmk_error}'
          f' - Ситилаб: {citilab_error}'
          f' - INVITRO: {invitro_error}'
          f' - KDL: {kdl_error}'
          f' - Гемотест: {gemotest_error}')

    # выбираем наименьшее расстояние
    pred = dic[min([ugmk_error, citilab_error, invitro_error, kdl_error, gemotest_error])]

    print(f'[PIXELSCAN] Prediction: its "{pred}"')

    return pred


def get_pixelscan_result(image, pixels_data):
    # получаем необходимые данные
    image_w, image_h = image.size
    image_rgb = image.convert("RGB")

    # будет накапливать ошибку
    error = 0.0
    for pixel_data in pixels_data:
        # получаем значение пикселя
        rgb_value = image_rgb.getpixel((round(image_w * pixel_data[0]), round(image_h * pixel_data[1])))

        # вычисляем ошибку и прибавляем к общему результату
        error += compare_pixels(pixel_data[2], rgb_value)

    return error


def compare_pixels(p1, p2):
    # получаем разницу в цвете пикселей
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


if __name__ == '__main__':
    print(get_scan_result(sys.argv[1]))
