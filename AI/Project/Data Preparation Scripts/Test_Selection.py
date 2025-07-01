import os
import random
import shutil

source_dir = "Data/Irregular"
train_dir = "Data/Train Data/Irregular"
test_dir = "Data/Test Data"

test_ratio = 0.2

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

all_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

random.shuffle(all_files)
test_count = int(len(all_files) * test_ratio)
test_files = all_files[:test_count]
train_files = all_files[test_count:]

for file in train_files:
    shutil.copy(os.path.join(source_dir, file), os.path.join(train_dir, file))

for file in test_files:
    shutil.copy(os.path.join(source_dir, file), os.path.join(test_dir, file))

