import cv2
import os
import xml.etree.ElementTree as ET
    
def get_resize_percentage(img_location, target_height, target_width):
    image = cv2.imread(img_location)
    height, width, _ = image.shape
    height_ratio = target_height/height
    width_ratio = target_width/width
    return (image, height_ratio, width_ratio)

def scale_data(img_location, annotation_location, target_height, target_width, xml_strings, display_visuals, visual_display_length):
    image, h_ratio, w_ratio = get_resize_percentage(img_location, target_height, target_width)
    resized_img = resize_image(image, target_height, target_width)
    save_image(resized_img, img_location)
    resize_annotation_and_display(annotation_location, h_ratio, w_ratio, xml_strings, resized_img, display_visuals, visual_display_length, target_width, target_height)

def resize_image(image, target_height, target_width):
    return cv2.resize(image, (target_width, target_height), interpolation= cv2.INTER_AREA)

def save_image(image, location):
    cv2.imwrite(location, image)

def resize_annotation_and_display(annotation_location, height_ratio, width_ratio, xml_strings, resized_image, is_display_visuals, visual_display_length, width, height):
    tree = ET.parse(annotation_location)
    annotation_data = tree.getroot()
    min_point = [0, 0]
    max_point = [0, 0]

    annotation_data.find(xml_strings[5]).text = str(width)
    annotation_data.find(xml_strings[6]).text = str(height)
    for annotated_object in annotation_data.iter(xml_strings[0]):
        min_point = [0, 0]
        max_point = [0, 0]
        point_count = 0
        for bndbox_point in annotated_object.iter():
            if (bndbox_point.tag != xml_strings[0]):
                # Resize coordinate based on its relationship to height or width.
                if (bndbox_point.tag == xml_strings[1] or bndbox_point.tag == xml_strings[2]):
                    new_point_value = float(bndbox_point.text) * width_ratio
                    if (bndbox_point.tag == xml_strings[1]):
                        min_point[0] = int(new_point_value)
                    max_point[0] = int(new_point_value)
                elif (bndbox_point.tag == xml_strings[3] or bndbox_point.tag == xml_strings[4]):
                    new_point_value = float(bndbox_point.text) * height_ratio
                    if (bndbox_point.tag == xml_strings[3]):
                        min_point[1] = int(new_point_value)
                    max_point[1] = int(new_point_value)
                else:
                    print("Incorrect element under \"" + str(annotated_object.tag) + "\" tag in " + annotation_location + " file.")
                    quit()
                bndbox_point.text = str(round(new_point_value, 4))
                point_count += 1
        # Only draw a rectangle if we have modified four points this iteration.
        if(is_display_visuals and point_count == 4):
            cv2.rectangle(resized_image, tuple(min_point), tuple(max_point), (0, 0, 255), 1)

    if(is_display_visuals):
        display_visual(resized_image, visual_display_length)
    tree.write(annotation_location)

def display_visual(image, visual_display_length):
    cv2.imshow('image', image)
    cv2.waitKey(visual_display_length)
    cv2.destroyAllWindows()

def traverse_directory(directory, folder_names, file_types, file_data, target_width, target_height, xml_strings, display_visuals, visual_display_length):
    print("Resizing dataset, this may take a while...")
    for dir_name, sub_dir, _ in os.walk(directory):
        if (folder_names[0].lower() in map(str.lower, sub_dir) and folder_names[1].lower() in map(str.lower, sub_dir)):
            annotations_directory = os.path.join(dir_name, folder_names[0])
            frame_directory = os.path.join(dir_name, folder_names[1])
            count = validate_files(annotations_directory, frame_directory, file_types)
            i = 0
            if (count > 0):
                while (i < count):
                    annotation = os.path.join(annotations_directory, file_data[0] + str(i).zfill(file_data[1]) + file_types[0])
                    frame = os.path.join(frame_directory, file_data[0] + str(i).zfill(file_data[1]) + file_types[1])
                    if (os.path.isfile(annotation) and os.path.isfile(frame)):
                        scale_data(frame, annotation, target_height, target_width, xml_strings, display_visuals, visual_display_length)
                    else:
                        print("Rescale failed, since one of the following files does not exist.")
                        print("Annotation file: " + annotation)
                        print("Frame file: " + frame)
                        quit()
                    i += 1
    print("Done!")

def validate_files(annotations_directory, frames_directory, file_types):
    annotation = os.listdir(annotations_directory)
    frame = os.listdir(frames_directory)
    annotation_count = 0
    frame_count = 0

    for file in annotation:
        if (os.path.splitext(file)[-1].lower() == file_types[0].lower()):
            annotation_count += 1

    for file in frame:
        if(os.path.splitext(file)[-1].lower() == file_types[1].lower()):
            frame_count += 1

    if (annotation_count == frame_count and annotation_count != 0):
        return annotation_count
    else:
        print("Annotations folder and frame folder did not have a matching file count.")
        print("Annotations count " + str(annotation_count) + " at location: " + str(annotations_directory))
        print("Frames count " + str(frame_count) + " at location: " + str(frames_directory))
        quit()

# Annotations folder name must be first item, followed by the frame folder name.
folder_names = ('annotations', 'frame')
# Annotations file type must be first, followed by the image file type.
file_types = ('.xml', '.png')
# Corresponding annotation and frame files should be the same name other than file types. This data should be the leading name followed by number length in the filename.
file_data = ('frame_', 6)
# This tuple needs to be in the following order for proper function: bounding box label, x point, second x point, y point, second y point, width path, and height path.
xml_strings = ('bndbox', 'xmin', 'xmax', 'ymin', 'ymax', './size/width', './size/height')

# Settings
dir = 'E:\\Files\\School\\MachineLearningProject\\Data\\VisualData - Copy'
target_width = 400
target_height = 400
display_visuals = True
# The following setting is in milliseconds.
visual_display_length = 150

if (os.path.isdir(dir)):
    traverse_directory(dir, folder_names, file_types, file_data, target_width, target_height, xml_strings, display_visuals, visual_display_length)
else:
    print("Target directory not found at " + dir)