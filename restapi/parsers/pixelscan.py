import numpy as np
import cv2

get_logo_path = {
    'Гемотест':'parsers/logo/GEMOTEST_LOGO.png',
    'INVITRO':'parsers/logo/INVITRO_LOGO.png',
    'KDL': 'parsers/logo/KDL_LOGO.png',
    'Ситилаб': 'parsers/logo/SITILAB_LOGO.png',
    'УГМК': 'parsers/logo/UGMK_LOGO.png',
}

def is_image_from_company(img_rgb, company):
    template = cv2.imread(get_logo_path[company])
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75
    loc = np.where(res >= threshold)
    # Если что-то нашли, то лист не будет пуст
    return len(loc[::-1][0]) > 0


def get_scan_result(image_path):
    print(f'[PIXELSCAN] Processing image "{image_path}"')
    img_rgb = cv2.imread(image_path)
    # Так как из коробки CV не умеет в мультискейлинг, приходится вручную
    # приводить картинку к размеру, с которого был снят логотип
    img_rgb = cv2.resize(img_rgb, (634, 896))
    for company in get_logo_path.keys():
        if is_image_from_company(img_rgb, company):
            print(f'[PIXELSCAN] Prediction: "{company}"')
            return company
    print(f'[PIXELSCAN] Cant find company logo')
    return 'UNKNOWN'

