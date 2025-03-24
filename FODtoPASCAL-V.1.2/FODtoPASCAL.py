import os
import xml.etree.ElementTree as ET
import random
from os import path, sep
from PIL import Image
from datetime import datetime, time
from path import NEWLINE

def move_and_update_file_pair(annotation_file, image_file, new_dataset_directory, folder_names, iterator_string):
    transfer_data = update_files(annotation_file, image_file, iterator_string)
    if (transfer_data == 0):
        print("An error occurred when parsing data for transfer.")
        quit()
    elif transfer_data is None:
        print("Did not add annotation file at " + annotation_file + " due to no annotated objects.")
        return False

    # Save file as .jpg. and write updated xml file.
    # TODO fix some whitespace issues not allowing a "pretty print" of the xml file
    with Image.open(image_file) as img:
        img.save(new_dataset_directory + os.sep + folder_names[1] + os.sep + iterator_string + ".jpg")
    transfer_data.write(new_dataset_directory + os.sep + folder_names[0] + os.sep + iterator_string + ".xml")

def update_files(annotation_file, image_file, iterator_string):
    file_ext = os.path.splitext(image_file)[1].lower()
    if (file_ext == ".png" or file_ext == ".jpg"):
        tree = ET.parse(annotation_file)
        root = tree.getroot()
        file_name = root.find('filename')
        file_name.text = iterator_string + ".jpg"

        # Eliminate empty annotations.
        if root.find("object") is None:
            return None
        
        # Fully update xml file to Pascal VOC format.
        for annotated_object in root.iterfind("object"):

            truncated = "truncated"
            difficult = "difficult"
            pose = "pose"

            if root.find(truncated) is None:
                truncated_element = ET.Element(truncated)
                truncated_element.text = "0"
                annotated_object.insert(2, truncated_element)

            if root.find(difficult) is None:
                difficult_element = ET.Element(difficult)
                difficult_element.text = "0"
                annotated_object.insert(3, difficult_element)

            if root.find(pose) is None:
                pose_element = ET.Element(pose)
                pose_element.text = "Unspecified"
                annotated_object.insert(4, pose_element)

            indent(annotated_object)
        return tree
    else:
        return 0

# The following indent code recieved from https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python.
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def create_directory(output_file_location, folder_names):
    try: 
        time = datetime.now()
        time_string = time.strftime("%d-%m-%Y_%H.%M.%S")
        new_path = output_file_location + os.sep + "ConvertedDataset_" + time_string + os.sep + folder_names[2]
        os.makedirs(new_path)
        os.makedirs(new_path + os.sep + folder_names[0])
        os.makedirs(new_path + os.sep + folder_names[4] + os.sep + folder_names[3])
        os.makedirs(new_path + os.sep + folder_names[1])
        return new_path
    except: 
        print ("An error occurred when creating a directory for the converted dataset at " + output_file_location + ".")
        quit()

def traverse_dataset(directory, output_directory, folder_names, file_types, file_data, pascal_voc_file_names, train_percentage):
    print("Converting Dataset to Pascal VOC, this may take a while...")
    start_time = datetime.now()
    new_path = create_directory(output_directory, pascal_voc_file_names)
    xml_count = 0
    image_count = 0
    xml_files = []
    new_xml_files = []
    for root, directories, filenames in os.walk(directory):
        if path.basename(root).lower() == folder_names[0].lower() or path.basename(root).lower() == folder_names[1].lower():
            for filename in filenames:
                if filename.lower().endswith(".xml"):
                    xml_count += 1
                    xml_files.append(root + os.sep + filename)
                if filename.lower().endswith(".png") or filename.lower().endswith(".jpg"):
                    image_count += 1

    if image_count == xml_count and xml_count == len(xml_files):
        print("Image and annotation counts are equal in directory (" + str(xml_count) + " count), procceding to convert dataset.")
        file_name_iterator = 0
        empty_check = True
        for xml_file in xml_files:
            split_path = path.split(xml_file)
            file_extension = path.splitext(split_path[1])
            remove_annotation_path = path.split(split_path[0])
            image_path_png = remove_annotation_path[0] + os.sep + folder_names[1] + os.sep + file_extension[0] + file_types[1]
            image_path_jpg = remove_annotation_path[0] + os.sep + folder_names[1] + os.sep + file_extension[0] + file_types[2]
            string_iterator = str(file_name_iterator).zfill(file_data[1])
            new_xml_files.append(string_iterator)
            if path.isfile(image_path_png) and path.isfile(xml_file):
                empty_check = move_and_update_file_pair(xml_file, image_path_png, new_path, pascal_voc_file_names, string_iterator)
            elif path.isfile(image_path_jpg) and path.isfile(xml_file):
                empty_check = move_and_update_file_pair(xml_file, image_path_jpg, new_path, pascal_voc_file_names, string_iterator)
            else:
                print("Matching image file for the following annotation does not exist: " + xml_file)
                print("Matching image should be located at this location as either a .png or .jpg file: " + image_path_png)
                print("Ending conversion process.")
                quit()
            if not empty_check is False:
                file_name_iterator += 1
    else:
        print("Annotation files and image files are not equal in selected directory, will not convert for this reason.")
        quit()

    dataset_sizes = create_imageset_files(new_xml_files, file_name_iterator, train_percentage, new_path, pascal_voc_file_names)
    end_time = datetime.now()
    
    print("Done! " + str(file_name_iterator) + " xml files converted and " + str(file_name_iterator) + " images converted.")
    print("Total conversion time: " + str(end_time - start_time))
    print("Train dataset size: " + str(dataset_sizes[0]))
    print("Test dataset size: " + str(dataset_sizes[1]))

def create_imageset_files(xml_list, xml_count, train_percentage, dataset_path, pascal_voc_file_names):
    testset_iterator = 0
    test_percentage = 1.00 - train_percentage
    test_set_size = round(xml_count * test_percentage)
    train_set_size = xml_count - test_set_size
    main_file_path = dataset_path + os.sep + pascal_voc_file_names[4] + os.sep + pascal_voc_file_names[3]
    test_txt_file = open(main_file_path + os.sep + "test.txt", "w")
    random.seed(datetime.now())
    used_string = "used"

    while(testset_iterator < test_set_size):
        selected_int = random.randint(0, xml_count - 1)
        filename = xml_list[selected_int]

        # Prevents the use of duplicate files in the test dataset.
        if filename.lower() == used_string:
            continue

        test_txt_file.write(filename + '\n')
        xml_list[selected_int] = used_string
        testset_iterator += 1

    test_txt_file.close()
    train_txt_file = open(main_file_path + os.sep + "trainval.txt", "w")
    trainset_iterator = 0

    while (trainset_iterator < xml_count):
        train_filename = xml_list[trainset_iterator]

        if (train_filename.lower() == used_string):
            trainset_iterator += 1
            continue
        
        train_txt_file.write(train_filename + '\n')
        trainset_iterator += 1

    train_txt_file.close()
    return (train_set_size, test_set_size)

# Annotations folder name must be first item, followed by the frame folder name.
folder_names = ('annotations', 'frame')
# Annotations file type must be first, followed by the image file type.
file_types = ('.xml', '.png', '.jpg')
# Corresponding annotation and frame files should be the same name other than file types. This data should be the leading name followed by number length in the filename.
file_data = ('frame_', 6)
# First string: Annotations directory, Second string: Images Directory, Third string: Dataset Directory, Fourth String: Main directory, Fifth String: Image sets directory.
pascal_voc_file_names = ("Annotations", "JPEGImages", "VOC2007", "Main", "ImageSets")

# Settings.
directory_to_convert = 'E:\\Files\\School\\MachineLearningProject\\Data\\FullDataset - SSD DATA'
output_directory = os.path.split(directory_to_convert)[0]
# Validate this to be less than 100%
train_set_percentage = .75

if (os.path.isdir(directory_to_convert)):
    traverse_dataset(directory_to_convert, output_directory, folder_names, file_types, file_data, pascal_voc_file_names, train_set_percentage)
else:
    print("Directory does not exist: " + directory_to_convert)