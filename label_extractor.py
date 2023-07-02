import os
import shutil
import numpy as np
import pandas as pd

def get_labels(line):
    """
    read line of yolo annotations

    return label
    """
    line = line.split(' ')
    return line[0]

def adjust_labels(labels):
    label = []
    for i in labels:
        label.append(" "+i+" ")
    return label

def create_missing_dir():
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        print(f"Creating missing directory - {save_dir}")
    if not os.path.exists(labels_save_dir):
        os.mkdir(labels_save_dir)
        print(f"Creating missing directory - {labels_save_dir}")
    if not os.path.exists(images_save_dir):
        os.mkdir(images_save_dir)
        print(f"Creating missing directory - {images_save_dir}")


dir = "./megadata"
images_dir = os.path.join(dir, "images")
labels_dir = os.path.join(dir, "labels")

save_dir = "./filtered_ppe"
labels_save_dir = os.path.join(save_dir, "labels")
images_save_dir = os.path.join(save_dir, "images")
data = []

labels_to_extract = ["0", "1", "2", "3", "4"]
labels_to_extract = adjust_labels(labels_to_extract)



if __name__ == "__main__":
    assert len(labels_to_extract) > 0, "labels_to_extract cannot be empty"
    print(labels_to_extract)
    create_missing_dir()
    for fname in os.listdir(labels_dir):
        if fname.endswith(".txt"):
            path_to_label = os.path.join(labels_dir, fname)
            
            with open(path_to_label, "r") as f:
                lines = f.readlines()
                labels = []
                for line in lines:
                    line = line.rstrip()
                    labels.append(get_labels(line))
                row_data = [fname, ' '.join(labels)]
            data.append(row_data)
    df = pd.DataFrame(data, columns=["filename", "labels"])
    filtered_df = df[df['labels'].str.contains("|".join(labels_to_extract))]
    for label in filtered_df['filename']:
        filename = os.path.splitext(label)[0]
        path_to_label = os.path.join(labels_dir, label)
        
        if os.path.exists(os.path.join(images_dir, filename+".jpg")):
            path_to_image = os.path.join(images_dir, filename+".jpg")
            shutil.copy(path_to_image, os.path.join(save_dir, "images", filename+".jpg"))
            shutil.copy(path_to_label, os.path.join(save_dir, "labels", label))
        elif os.path.exists(os.path.join(images_dir, filename+".jpeg")):
            path_to_image = os.path.join(images_dir, filename+".jpeg")
            shutil.copy(path_to_image, os.path.join(save_dir, "images", filename+".jpeg"))
            shutil.copy(path_to_label, os.path.join(save_dir, "labels", label))
        elif os.path.exists(os.path.join(images_dir, filename+".JPEG")):
            path_to_image = os.path.join(images_dir, filename+".JPEG")
            shutil.copy(path_to_image, os.path.join(save_dir, "images", filename+".JPEG"))
            shutil.copy(path_to_label, os.path.join(save_dir, "labels", label))
    print(filtered_df)
    # print(df[df['labels'].str.contains("|".join(labels_to_extract))])

