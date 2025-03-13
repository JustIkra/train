import os
import shutil
from PIL import Image

images_dir = "images"
labels_dir = "labels"
output_dir = "sorted"

train_ration = 0.8
val_ration = 0.1
test_ration = 0.1
assert (train_ration + val_ration + test_ration == 1)

os.makedirs(output_dir, exist_ok=True)

labels = [f for f in os.listdir(labels_dir) if f.endswith(".txt")]
bad_labels = []

def resize_and_save(images, save_dir):

    labels_output_dir = os.path.join(output_dir,save_dir, "labels",)
    images_output_dir = os.path.join(output_dir,save_dir, "images",)

    os.makedirs(labels_output_dir, exist_ok=True)
    os.makedirs(images_output_dir, exist_ok=True)

    for image in images:
        try:
            image_path = os.path.join(images_dir, image)
            save_image_path = os.path.join(images_output_dir, image)
            with Image.open(image_path) as img:
                img = img.resize((640, 640), Image.Resampling.LANCZOS)
                img.save(save_image_path)
            label_path = os.path.join(labels_dir, image.replace(".jpg", ".txt"))
            shutil.copy(label_path, labels_output_dir)
        except:
            print("Read image error")
            bad_labels.append(image.replace(".jpg", ".txt"))

def check_label(label):
    label_path = os.path.join(labels_dir, label)
    try:
        with open(label_path,"r") as f:
            seen = set()
            for line in f:
                parts = line.split()
                if len(parts) == 5:
                    annotation = tuple(parts)
                    cls, x, y, w, h = map(float, parts)
                    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                        return False
                    elif annotation in seen:
                        return False
                    seen.add(annotation)
                else:
                    return False

            return True
    except:
        print("Read text file error")
        return False

for label in labels:
    if check_label(label):
        continue
    else:
        bad_labels.append(label)

print(f"{len(bad_labels)} - количество некачественных файлов разметки")

sorted_labels = list(set(labels) - set(bad_labels))

sorted_images = [f.replace(".txt", ".jpg") for f in sorted_labels]

train_count = int(len(sorted_images) * train_ration)
val_count = int(len(sorted_images) * val_ration)
test_count = int(len(sorted_images) * test_ration)

val_images = sorted_images[:val_count]
test_images = sorted_images[val_count:test_count + val_count]
train_images = sorted_images[val_count + test_count:]

resize_and_save(val_images, "val")
resize_and_save(test_images, "test")
resize_and_save(train_images, "train")

print(f"val: {len(val_images)}, test: {len(test_images)},train: {len(train_images)}, sorted: {len(bad_labels)}")