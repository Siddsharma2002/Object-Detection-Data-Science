#import os
#import xml.etree.ElementTree as ET
#
# # Define paths
# VOC_ANNOTATIONS_DIR = "C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\VOC2007\Annotations"
# VOC_IMAGES_DIR = "C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\VOC2007\JPEGImages"
#
# YOLO_LABELS_DIR = "C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\yolo label"
# CLASS_NAMES = ["Battery","BoltWasher","ClampPart","Cutter","PlasticPart","Bolt","LuggageTag","Nail","Pliers","Label","Washer","Wrench","FuelCap","Nut","MetalSheet","Hose","AdjustableClamp","AdjustableWrench","BoltNutSet","Hammer","LuggagePart","MetalPart","PaintChip","Pen","Rock","Screw","Screwdriver","SodaCan","Wire","Wood","Tape"]  # Replace with actual class names
#
# # Create output folder if not exists
# os.makedirs(YOLO_LABELS_DIR, exist_ok=True)
#
#
# def convert_voc_to_yolo(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#
#     image_filename = root.find("filename").text
#     image_path = os.path.join(VOC_IMAGES_DIR, image_filename)
#
#     img_width = int(root.find("size/width").text)
#     img_height = int(root.find("size/height").text)
#
#     label_filename = os.path.join(YOLO_LABELS_DIR, image_filename.replace(".jpg", ".txt"))
#
#     with open(label_filename, "w") as f:
#         for obj in root.findall("object"):
#             class_name = obj.find("name").text
#             class_id = CLASS_NAMES.index(class_name) if class_name in CLASS_NAMES else -1
#             if class_id == -1:
#                 continue  # Skip unknown classes
#
#             bbox = obj.find("bndbox")
#             x_min, y_min, x_max, y_max = map(int, [bbox.find("xmin").text, bbox.find("ymin").text,
#                                                    bbox.find("xmax").text, bbox.find("ymax").text])
#
#             # Convert to YOLO format (normalized x_center, y_center, width, height)
#             x_center = (x_min + x_max) / (2 * img_width)
#             y_center = (y_min + y_max) / (2 * img_height)
#             bbox_width = (x_max - x_min) / img_width
#             bbox_height = (y_max - y_min) / img_height
#
#             f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")
#
#
# # Convert all XML annotations
# for xml_file in os.listdir(VOC_ANNOTATIONS_DIR):
#     if xml_file.endswith(".xml"):
#         convert_voc_to_yolo(os.path.join(VOC_ANNOTATIONS_DIR, xml_file))
#
# print("Conversion completed! YOLO labels are saved in:", YOLO_LABELS_DIR)
#
#
# import os
# import xml.etree.ElementTree as ET
#
# # Define paths (use raw strings r"..." to avoid escape character issues)
# VOC_ANNOTATIONS_DIR = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\VOC2007\Annotations"
# VOC_IMAGES_DIR = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\VOC2007\JPEGImages"
# YOLO_LABELS_DIR = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\yolo_label"
#
# # Class names
# CLASS_NAMES = [
#     "Battery", "BoltWasher", "ClampPart", "Cutter", "PlasticPart", "Bolt",
#     "LuggageTag", "Nail", "Pliers", "Label", "Washer", "Wrench", "FuelCap",
#     "Nut", "MetalSheet", "Hose", "AdjustableClamp", "AdjustableWrench",
#     "BoltNutSet", "Hammer", "LuggagePart", "MetalPart", "PaintChip", "Pen",
#     "Rock", "Screw", "Screwdriver", "SodaCan", "Wire", "Wood", "Tape"
# ]
#
# # Create output folder if it doesn't exist
# os.makedirs(YOLO_LABELS_DIR, exist_ok=True)
#
#
# def convert_voc_to_yolo(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#
#     image_filename = root.find("filename").text
#     image_path = os.path.join(VOC_IMAGES_DIR, image_filename)
#
#     img_width = int(root.find("size/width").text)
#     img_height = int(root.find("size/height").text)
#
#     label_filename = os.path.join(YOLO_LABELS_DIR, image_filename.replace(".jpg", ".txt"))
#
#     with open(label_filename, "w") as f:
#         for obj in root.findall("object"):
#             class_name = obj.find("name").text
#             if class_name not in CLASS_NAMES:
#                 continue  # Skip unknown classes
#
#             class_id = CLASS_NAMES.index(class_name)
#
#             bbox = obj.find("bndbox")
#             x_min, y_min, x_max, y_max = map(int, [
#                 bbox.find("xmin").text, bbox.find("ymin").text,
#                 bbox.find("xmax").text, bbox.find("ymax").text
#             ])
#
#             # Convert to YOLO format (normalized x_center, y_center, width, height)
#             x_center = (x_min + x_max) / (2 * img_width)
#             y_center = (y_min + y_max) / (2 * img_height)
#             bbox_width = (x_max - x_min) / img_width
#             bbox_height = (y_max - y_min) / img_height
#
#             f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")
#
#
# # Convert all XML annotations
# for xml_file in os.listdir(VOC_ANNOTATIONS_DIR):
#     if xml_file.endswith(".xml"):
#         convert_voc_to_yolo(os.path.join(VOC_ANNOTATIONS_DIR, xml_file))
#
# print("✅ Conversion completed! YOLO labels are saved in:", YOLO_LABELS_DIR)
#
# def convert_voc_to_yolo(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#
#     image_filename = root.find("filename").text
#     image_path = os.path.join(VOC_IMAGES_DIR, image_filename)
#
#     img_width = float(root.find("size/width").text)
#     img_height = float(root.find("size/height").text)
#
#     label_filename = os.path.join(YOLO_LABELS_DIR, image_filename.replace(".jpg", ".txt"))
#
#     with open(label_filename, "w") as f:
#         for obj in root.findall("object"):
#             class_name = obj.find("name").text
#             if class_name not in CLASS_NAMES:
#                 continue  # Skip unknown classes
#
#             class_id = CLASS_NAMES.index(class_name)
#
#             bbox = obj.find("bndbox")
#             x_min = float(bbox.find("xmin").text)
#             y_min = float(bbox.find("ymin").text)
#             x_max = float(bbox.find("xmax").text)
#             y_max = float(bbox.find("ymax").text)
#
#             # Convert to YOLO format (normalized x_center, y_center, width, height)
#             x_center = (x_min + x_max) / (2 * img_width)
#             y_center = (y_min + y_max) / (2 * img_height)
#             bbox_width = (x_max - x_min) / img_width
#             bbox_height = (y_max - y_min) / img_height
#
#             f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")
#

import os
import xml.etree.ElementTree as ET

# Define paths (use raw strings r"..." to avoid escape character issues)
VOC_ANNOTATIONS_DIR = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\VOC2007\Annotations"
VOC_IMAGES_DIR = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\VOC2007\JPEGImages"
YOLO_LABELS_DIR = r"C:\Users\my pc\OneDrive\Desktop\New folder (5)\FODPascalVOCFormat-V.2.1\FODPascalVOCFormat-V.2.1\yolo_label"

# Class names
CLASS_NAMES = [
    "Battery", "BoltWasher", "ClampPart", "Cutter", "PlasticPart", "Bolt",
    "LuggageTag", "Nail", "Pliers", "Label", "Washer", "Wrench", "FuelCap",
    "Nut", "MetalSheet", "Hose", "AdjustableClamp", "AdjustableWrench",
    "BoltNutSet", "Hammer", "LuggagePart", "MetalPart", "PaintChip", "Pen",
    "Rock", "Screw", "Screwdriver", "SodaCan", "Wire", "Wood", "Tape"
]

# Create output folder if it doesn't exist
os.makedirs(YOLO_LABELS_DIR, exist_ok=True)


def convert_voc_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    image_filename = root.find("filename").text

    # Ensure the correct image extension
    image_filename = os.path.splitext(image_filename)[0] + ".jpg"
    image_path = os.path.join(VOC_IMAGES_DIR, image_filename)

    # Get image size
    img_width = float(root.find("size/width").text)
    img_height = float(root.find("size/height").text)

    # Define output label file
    label_filename = os.path.join(YOLO_LABELS_DIR, image_filename.replace(".jpg", ".txt"))

    with open(label_filename, "w") as f:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in CLASS_NAMES:
                continue  # Skip unknown classes

            class_id = CLASS_NAMES.index(class_name)

            bbox = obj.find("bndbox")
            x_min = float(bbox.find("xmin").text)
            y_min = float(bbox.find("ymin").text)
            x_max = float(bbox.find("xmax").text)
            y_max = float(bbox.find("ymax").text)

            # Convert to YOLO format (normalized x_center, y_center, width, height)
            x_center = (x_min + x_max) / (2 * img_width)
            y_center = (y_min + y_max) / (2 * img_height)
            bbox_width = (x_max - x_min) / img_width
            bbox_height = (y_max - y_min) / img_height

            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")


# Convert all XML annotations
for xml_file in os.listdir(VOC_ANNOTATIONS_DIR):
    if xml_file.endswith(".xml"):
        convert_voc_to_yolo(os.path.join(VOC_ANNOTATIONS_DIR, xml_file))

print("✅ Conversion completed! YOLO labels are saved in:", YOLO_LABELS_DIR)
