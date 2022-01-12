from PIL import Image

data_kdl = [
    [0.138583, 0.043478, (159, 28, 98)],  # Фиолетово-розовый
    [0.110236, 0.071349, (113, 34, 96)],  # Фиолетовый
    [0.143307, 0.066890, (140, 30, 96)],  # Фиолетовый
    [0.111811, 0.055741, (236, 102, 29)],  # Оранжевый
    [0.188976, 0.078037, (0, 0, 0)]  # Черный
]

data_ugmk = [
    [0.089623, 0.070078, (202, 80, 25)],  # Оранжевый
    [0.113208, 0.076752, (246, 246, 246)],  # Белый
    [0.058176, 0.072303, (255, 255, 255)],  # Белый
    [0.231132, 0.087875, (237, 134, 35)],  # Оранжевый
    [0.235849, 0.077864, (253, 250, 254)]  # Белый
]

data_gemotest = [
    [0.099456, 0.025638, (1, 125, 58)],  # Зеленый
    [0.112757, 0.022902, (253, 253, 254)],  # Белый
    [0.129760, 0.032250, (2, 127, 61)],  # Зеленый
    [0.139647, 0.036714, (253, 254, 254)],  # Белый
    [0.376817, 0.025421, (6, 122, 62)],  # Зеленый
]

data_invitro = [
    [0.042654, 0.022321, (2, 163, 186)],  # Бирюзовый
    [0.071090, 0.017857, (249, 251, 252)],  # Белый
    [0.090047, 0.020089, (2, 164, 184)],  # Бирюзовый
    [0.097946, 0.017857, (254, 254, 255)],  # Белый
    [0.199052, 0.034598, (3, 164, 180)]  # Бирюзовый
]

data_sitilab = [
    [0.897638, 0.033296, (219, 8, 68)],  # Розовый
    [0.888189, 0.033296, (255, 255, 255)],  # Белый
    [0.869291, 0.035516, (218, 8, 73)],  # Розовый
    [0.818898, 0.038846, (1, 78, 162)],  # Синий
    [0.897638, 0.039956, (4, 78, 150)]  # Синий
]


def get_pixelscan_result(image, pixels_data):
    # Получаем необходимые данные
    image_w, image_h = image.size
    image_rgb = image.convert("RGB")
    # Будет накапливать ошибку
    error = 0.0
    for pixel_data in pixels_data:
        # Получаем значение пикселя
        rgb_value = image_rgb.getpixel((round(image_w * pixel_data[0]), round(image_h * pixel_data[1])))
        # Вычисляем ошибку и прибавляем к общему результату
        error += compare_pixels(pixel_data[2], rgb_value)
    return error


def get_scan_result(image_path):
    print(f'[PIXELSCAN] Processing image "{image_path}"')
    # Загружаем картинку
    image = Image.open(image_path)
    # Рассчитываем расстояние до каждой клиники и выбираем наименьшее
    sitilab_error = get_pixelscan_result(image, data_sitilab)
    invitro_error = get_pixelscan_result(image, data_invitro)
    gemotest_error = get_pixelscan_result(image, data_gemotest)
    kdl_error = get_pixelscan_result(image, data_kdl)
    ugmk_error = get_pixelscan_result(image, data_ugmk)
    dic = {sitilab_error: 'SITILAB',
           invitro_error: 'INVITRO',
           gemotest_error: 'GEMOTEST',
           kdl_error: 'KDL',
           ugmk_error: 'UGMK'}
    print(f'[PIXELSCAN] Errors list:')
    print(f' - SITILAB: {sitilab_error}')
    print(f' - INVITRO: {invitro_error}')
    print(f' - GEMOTEST: {gemotest_error}')
    print(f' - KDL: {kdl_error}')
    print(f' - UGMK: {ugmk_error}')
    pred = dic[min([sitilab_error, invitro_error, gemotest_error, kdl_error, ugmk_error])]
    print(f'[PIXELSCAN] Prediction: its "{pred}"')
    return pred


def compare_pixels(p1, p2):
    # Получаем разницу в цвете пикселей
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])
