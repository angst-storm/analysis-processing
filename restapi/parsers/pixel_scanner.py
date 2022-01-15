import numpy as np
import cv2

logos_paths = {
    'Гемотест': 'parsers/logos/gemotest.png',
    'INVITRO': 'parsers/logos/invitro.png',
    'KDL': 'parsers/logos/kdl.png',
    'Ситилаб': 'parsers/logos/citilab.png',
    'УГМК': 'parsers/logos/ugmk.png',
}


def is_image_from_company(img_rgb, company):
    template = cv2.imread(logos_paths[company])
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75
    loc = np.where(res >= threshold)
    return len(loc[::-1][0]) > 0


def get_scan_result(image_path):
    img_rgb = cv2.imread(image_path)
    img_rgb = cv2.resize(img_rgb, (634, 896))
    for company in logos_paths.keys():
        if is_image_from_company(img_rgb, company):
            return company
    return 'unknown'
