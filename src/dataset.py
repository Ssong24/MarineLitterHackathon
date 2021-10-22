import os
import shutil
import xml.etree.ElementTree as ET
import glob

def alignDataset(marine_dataset):
    for i in range(18,21): # 21
        dir1 = marine_dataset +str(i)+ "/2021-09-29 학습용 데이터"
        dir2 = dir1 + "/Set_" + str(i+9)
        print(dir2)
        for f in os.listdir(dir2):
            shutil.move(dir2 + "/" + f, dir2 + "/../../" + f)
        os.rmdir(dir2)
        os.rmdir(dir1)

def read_content(xml_file: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    list_with_all_boxes = []
    list_with_all_names = []
    filename = root.find('filename').text

    width= int(root.find("size/width").text)
    height = int(root.find("size/height").text)
    depth = int(root.find("size/depth").text)
    imgSize = (width, height, depth)

    altitude = float(root.find("altitude").text)
    latitude = float(root.find("lat").text)
    longitude = float(root.find("lon").text)
    location = (altitude, latitude, longitude)


    for boxes in root.iter('object'):
        ymin, xmin, ymax, xmax = None, None, None, None

        ymin = int(boxes.find("bndbox/ymin").text)
        xmin = int(boxes.find("bndbox/xmin").text)
        ymax = int(boxes.find("bndbox/ymax").text)
        xmax = int(boxes.find("bndbox/xmax").text)
        className = boxes.find("name").text

        list_with_single_boxes = [xmin, ymin, xmax, ymax]
        list_with_all_boxes.append(list_with_single_boxes)

        list_with_all_names.append(className)

    return filename, imgSize, list_with_all_names, list_with_all_boxes, location





def cntObjByClass(classNames, num_of_materials):
    for name in classNames:
        last_idx = name.find(')')
        name = name[last_idx + 1:]
        if name in num_of_materials.keys():
            num_of_materials[name] += 1
        else:
            num_of_materials[name] = 1

def groupSameLoc(location, xml_file):
    latitude, longitude = location[1], location[2]
    if latitude == 35.06048047222222 and longitude == 128.88881955555556:
        print(xml_file)

def cntSmallObj(boxes):
    smallCnt = 0
    for box in  boxes:
        boxW, boxH = box[2] - box[0], box[3] - box[1]
        if boxW == 0: boxW = 1
        if boxH == 0: boxH = 1
        box_size = boxW * boxH
        if box_size < 32 * 32:
            smallCnt += 1
    return smallCnt

# Read class name, bbox, and location of file from xml file
# Analyze the dataset from xml file
def cntObjMarineDataset():
    current_path = os.getcwd()
    marine_dataset = os.getcwd() + "/../../Downloads/MarineLitter/Dataset/dataset_"
    small_cnt = 0
    num_of_materials = {}
    for i in range(1, 2): # 1 ~ 20
        for f in glob.glob(marine_dataset + str(i) + "/*.xml"):
            # Import data
            filename, imgSize, classNames, boxes,location = read_content(f)
            print(filename, imgSize,location)

            # Count small objects
            small_cnt += cntSmallObj(boxes)
            # Count objects by class
            cntObjByClass(classNames, num_of_materials)
            # Print image file which have specific location(alt, lon)
            groupSameLoc(location, f)

