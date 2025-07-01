import os
from PIL import Image

BASE_DIR = 'Data'
TARGET_SIZE = (224, 224)

def resize_images(base_path):
    for split in ['Train Data', 'Test Data']:
        split_path = os.path.join(base_path, split)
        for class_name in os.listdir(split_path):
            class_path = os.path.join(split_path, class_name)
            if not os.path.isdir(class_path):
                continue
            for filename in os.listdir(class_path):
                file_path = os.path.join(class_path, filename)
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                try:
                    img = Image.open(file_path)
                    img = img.convert('RGB')
                    img = img.resize(TARGET_SIZE, Image.LANCZOS)
                    img.save(file_path)
                    print(f"Zmieniono rozmiar: {file_path}")
                except Exception as e:
                    print(f"Błąd przetwarzania {file_path}: {e}")

resize_images(BASE_DIR)
