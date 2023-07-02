"""
Train Val split for YOLOv5 dataset


DESCRIPTION
This script is used to split the dataset into train and val sets.

USAGE
1. Change the dir variable to the directory of the dataset. 
   Make sure the dataset has the following structure:
    - <dir>
        - images
            - <image1>.jpg
            - <image2>.jpg
            - ...
        - labels
            - <image1>.txt
            - <image2>.txt
            - ...
2. Change the save_dir variable to the directory where the new dataset will be saved.
3. Change the train_val_split variable to the percentage of the train set.
4. Run the script.





"""



import os
import random
import shutil

dir = "<dir here>"
save_dir = "<save dir here>"

labels_dir = os.path.join(dir, "labels")
images_dir = os.path.join(dir, "images")

folder = ["train", "val"]
train_val_split = 0.7

counter = 0

def check_labels(labels, line):
    if line[0] in labels:
        return True
    
def map_labels(line, cls_mapper):
    line = line.split(' ')
    line[0] = cls_mapper[line[0]]
    return " ".join(line)

def create_missing_dir():
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        print(f"Creating missing directory - {save_dir}")
    for m in folder:
        m_folder = os.path.join(save_dir, m)
        if not os.path.exists(m_folder):
            os.mkdir(m_folder)
            m_images = os.path.join(m_folder, "images")
            m_labels = os.path.join(m_folder, "labels")
            os.mkdir(m_images)
            os.mkdir(m_labels)
            print(f"Creating missing directory - {m_folder}")
            print(f"Creating missing directory - {m_images}")
            print(f"Creating missing directory - {m_labels}")
    print("")

if __name__ == "__main__":
    create_missing_dir()
    all_labels = os.listdir(labels_dir)
    random.shuffle(all_labels)
    total_labels = len(all_labels)
    train_count = int(train_val_split * total_labels)
    data_split = {
        "train": all_labels[:train_count],
        "val": all_labels[train_count:]
    }
    for d in folder:
        labels = data_split[d]
        
        for label in labels:
            filename = os.path.splitext(label)[0]
            path_to_label = os.path.join(labels_dir, label)
            
            if os.path.exists(os.path.join(images_dir, filename+".jpg")):
                path_to_image = os.path.join(images_dir, filename+".jpg")
                shutil.copy(path_to_image, os.path.join(save_dir, d, "images", filename+".jpg"))
                shutil.copy(path_to_label, os.path.join(save_dir, d, "labels", label))
            elif os.path.exists(os.path.join(images_dir, filename+".jpeg")):
                path_to_image = os.path.join(images_dir, filename+".jpeg")
                shutil.copy(path_to_image, os.path.join(save_dir, d, "images", filename+".jpeg"))
                shutil.copy(path_to_label, os.path.join(save_dir, d, "labels", label))
            elif os.path.exists(os.path.join(images_dir, filename+".JPEG")):
                path_to_image = os.path.join(images_dir, filename+".JPEG")
                shutil.copy(path_to_image, os.path.join(save_dir, d, "images", filename+".JPEG"))
                shutil.copy(path_to_label, os.path.join(save_dir, d, "labels", label))
            else:
                print(f"image for {label} cannot be found")

    print("Splitting done!")
    print("--------------------------------")
    print(f"total images : {total_labels}")
    print(f"train images : {len(data_split['train'])}")
    print(f"val images : {len(data_split['val'])}")




