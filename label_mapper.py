"""
Label mapper for YOLOv5

DESCRIPTION
This script is used to map the labels from the original dataset to the labels that are used in the training process.
This is done because the original dataset has 33 classes, but the training process only uses 5 classes.

USAGE
1. Change the class_mapper variable to map the original class to the new class.
2. Change the dir variable to the directory of the original dataset.
3. Make sure the original dataset has the following structure:
    - <dir>
        - images
            - <image1>.jpg
            - <image2>.jpg
            - ...
        - labels
            - <image1>.txt
            - <image2>.txt
            - ...
4. Change the save_dir variable to the directory where the new dataset will be saved.
5. Run the script.

NOTES
- The script will create the save_dir if it does not exist.
- classes that are not in the class_mapper will be ignored.

"""



import os
import shutil
# class_mapper = {
#     "0": "0",
#     "1": "1",
#     "2": "2",
#     "3": "3",
#     "4": "4",               
#                 }
class_mapper = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
    "9": "10",
    "10": "11",
    "11": "12",
    "12": "13",
    "13": "14",
    "14": "15",
    "15": "16",
    "16": "17",
    "17": "18",
    "18": "19",
    "19": "20",
    "20": "21",
    "21": "22",
    "22": "23",
    "23": "24",
    "24": "25",
    "25": "26",
    "26": "27",
    "27": "28",
    "28": "29",
    "29": "30",
    "30": "31",
    "31": "32",
    "32": "33",
               
                }
dir = "<dir here>"
save_dir = "<save dir here>"

labels_dir = os.path.join(dir, "labels")
images_dir = os.path.join(dir, "images")

labels_save_dir = os.path.join(save_dir, "labels")
images_save_dir = os.path.join(save_dir, "images")

counter = 0

def check_labels(labels, line):
    line = line.split(' ')
    return line[0] in labels
    
def map_labels(line, cls_mapper):
    line = line.split(' ')
    line[0] = cls_mapper[line[0]]
    return " ".join(line)

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


if __name__ == "__main__":
    labels = list(class_mapper.keys())
    print(labels)
    create_missing_dir()
    for labels_file in os.listdir(labels_dir):
        if labels_file.endswith(".txt"):
            write_lines = []
            with open(os.path.join(labels_dir, labels_file), "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.rstrip()
                    if check_labels(labels, line):
                        line = map_labels(line, class_mapper)
                        write_lines.append(line)

            if len(write_lines) == 0:
                continue
            else:
                image_file = os.path.splitext(labels_file)[0]
                with open(os.path.join(labels_save_dir, labels_file), 'w') as f:
                    f.writelines("%s\n" % l for l in write_lines)
                try:
                    if os.path.exists(os.path.join(images_dir, image_file+".jpg")):
                        image_file = image_file+".jpg"
                        shutil.copy(os.path.join(images_dir,image_file), os.path.join(images_save_dir,image_file))
                        counter += 1
                    elif os.path.exists(os.path.join(images_dir, image_file+".JPEG")):
                        image_file = image_file+".JPEG"
                        shutil.copy(os.path.join(images_dir,image_file), os.path.join(images_save_dir,image_file))
                        counter += 1
                except FileNotFoundError:
                    print(f"{image_file} does not exist")

                
