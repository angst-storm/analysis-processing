from PIL import Image


crop_data_sitilab = [
    [(0.085039, 0.338513, 0.513386, 0.742508), (0.532283, 0.338513, 0.644094, 0.742508),
     (0.678740, 0.338513, 0.801575, 0.742508)],  # Первая страница
    [(0.084906, 0.233333, 0.504717, 0.39), (0.544025, 0.233333, 0.635220, 0.39),
     (0.682390, 0.233333, 0.795597, 0.39)]  # Вторая страница
]

crop_data_kdl = [
    [(0.092913, 0.268673, 0.417323, 0.751394), (0.417323, 0.268673, 0.532283, 0.751394),
     (0.666142, 0.268673, 0.762205, 0.751394)],  # Первая страница
    [(0.095611, 0.271413, 0.371473, 0.286986), (0.434169, 0.271413, 0.526646, 0.286986),
     (0.666144, 0.271413, 0.761755, 0.286986)]  # Вторая страница
]

crop_data_ugmk = [
    [(0.015723, 0.281215, 0.416667, 0.7420), (0.427873, 0.281215, 0.584906, 0.7420),
     (0.594840, 0.281215, 0.698113, 0.7420)],  # Первая страница
]

crop_data_gemotest = [
    [(0.094637, 0.507813, 0.528391, 0.658482), (0.569401, 0.507813, 0.670347, 0.658482),
     (0.695584, 0.507813, 0.783912, 0.658482),
     (0.094637, 0.695313, 0.528391, 0.741071), (0.569401, 0.695313, 0.670347, 0.741071),
     (0.695584, 0.695313, 0.783912, 0.741071),
     (0.094637, 0.756696, 0.528391, 0.803571), (0.569401, 0.756696, 0.670347, 0.803571),
     (0.695584, 0.756696, 0.783912, 0.803571)],  # Первая страница

    [(0.094637, 0.256952, 0.553628, 0.413793), (0.567823, 0.256952, 0.675079, 0.413793),
     (0.697161, 0.256952, 0.780757, 0.413793)]  # Вторая страница
]

crop_data_invitro = [
    [(0.031596, 0.234375, 0.295419, 0.784598), (0.295419, 0.234375, 0.456556, 0.784598),
     (0.511848, 0.234375, 0.665087, 0.784598)],  # Первая страница
    [] # Вторая страница
]

target_to_crop_data = {
    'Ситилаб': crop_data_sitilab,
    'KDL': crop_data_kdl,
    'УГМК': crop_data_ugmk,
    'Гемотест': crop_data_gemotest,
    'INVITRO': crop_data_invitro
}


def get_cropped_images(image_path, target):
    print(f'[CROPPER] Cropping image as {target}')
    result = []
    # Загружаем картинку
    image = Image.open(image_path)
    # У нас только 2 страницы
    if image_path[-5] == '0' or image_path[-5] == '1':
        # Обычно тут 3, но у гемотеста может быть 9
        for i in range(len(target_to_crop_data[target][int(image_path[-5])])):
            # Получаем из одной картинки изображения трех колонок таблицы (имя, значение, ед. изм.) путем разрезания
            # изображения по константным значениям углов таблицы
            image.crop(get_cropped_coords(target_to_crop_data[target][int(image_path[-5])][i], image)).save(
                image_path[:len(image_path) - 4] + f'-{image_path[-5]}-{i}.png')
            result.append(image_path[:len(image_path) - 4] + f'-{image_path[-5]}-{i}.png')
    return result


def get_cropped_coords(k, image):
    image_w, image_h = image.size
    return k[0] * image_w, k[1] * image_h, k[2] * image_w, k[3] * image_h
