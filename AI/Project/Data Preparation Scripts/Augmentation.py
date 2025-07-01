import os
import random
from PIL import Image, ImageEnhance
import numpy as np

FOLDER_A = "original_images"
FOLDER_B = "all_copies"
FOLDER_C = "random_copies"

os.makedirs(FOLDER_B, exist_ok=True)
os.makedirs(FOLDER_C, exist_ok=True)

def distort_image(img):
    width, height = img.size
    margin = int(min(width, height) * 0.15)

    def jitter(x, y):
        return (
            x + random.randint(-margin, margin),
            y + random.randint(-margin, margin)
        )

    original_corners = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height)
    ]

    distorted_corners = [jitter(x, y) for x, y in original_corners]
    coeffs = find_perspective_coeffs(distorted_corners, original_corners)
    return img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

def find_perspective_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
    A = np.array(matrix)
    B = np.array(pb).reshape(8)
    res = np.linalg.lstsq(A, B, rcond=None)[0]
    return res

def augment_image(img):
    rotations = [0, 90, 180, 270]
    distortions = ['orig', 'distort_up', 'distort_down']
    contrasts = [0.85, 1.0, 1.15]
    saturations = [0.7, 1.0, 1.3]

    variants = []

    for r in rotations:
        rotated = img.rotate(r, expand=True)
        for d in distortions:
            if d == 'orig':
                distorted = rotated
            else:
                distorted = distort_image(rotated)
            for c in contrasts:
                contrast_enhanced = ImageEnhance.Contrast(distorted).enhance(c)
                for s in saturations:
                    final = ImageEnhance.Color(contrast_enhanced).enhance(s)
                    variants.append(final.copy())

    return variants

for filename in os.listdir(FOLDER_A):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    input_path = os.path.join(FOLDER_A, filename)
    base_name = os.path.splitext(filename)[0]
    img = Image.open(input_path).convert("RGB")

    augmented = augment_image(img)
    all_paths = []

    for i, var in enumerate(augmented):
        out_path = os.path.join(FOLDER_B, f"{base_name}_aug_{i+1:03d}.jpg")
        var.save(out_path)
        all_paths.append(out_path)

    selected = random.sample(all_paths, 30)
    for i, path in enumerate(selected):
        img = Image.open(path)
        c_path = os.path.join(FOLDER_C, f"{base_name}_sel_{i+1:02d}.jpg")
        img.save(c_path)
