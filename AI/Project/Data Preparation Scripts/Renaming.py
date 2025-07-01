import os

folder = 'Lenticular'
folder_path = f'Data/{folder}'

image_extensions = ['.jpg', '.jpeg', '.png']

images = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]

images.sort()

for i, filename in enumerate(images, start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"{folder}({i}){ext}"
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, new_name)
    os.rename(src, dst)
