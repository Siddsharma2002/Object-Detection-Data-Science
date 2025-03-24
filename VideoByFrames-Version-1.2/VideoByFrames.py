import sys
import os
import re
import json
import argparse
import cv2
import ffmpeg
from pathlib import Path
from pathvalidate.argparse import validate_filepath_arg

def create_directory(output_file_location, target_video):
    i = 0
    try: 
        # Create a folder based on the file name.
        while(True):
            i += 1
            new_path = create_frame_filepath(output_file_location, target_video, i)

            if not os.path.exists(new_path):
                os.makedirs(new_path)
                break
        return new_path
    except: 
        print ("An error occurred when creating a directory for frame output at " + output_file_location +" for target file " + target_video + ".")
        quit()

def create_frame_filepath(directory, target_name, incrementer):
    try:  
        video_name_stem = Path(target_name).stem + str(incrementer)
        return directory + os.sep + video_name_stem + os.sep + "frame"
    except:
        print("An error occured when creating a new directory name at " + directory +".")
        quit()

def trim_video(video_file_location, target_filename, start_time, end_time, video_format='mp4'):
    trim_process = (
        ffmpeg
        .input(video_file_location)
        .trim(start=start_time, end=end_time)
        .setpts('PTS-STARTPTS')
        .output(filename=target_filename, format=video_format)
        .run_async())
    trim_process.communicate()
    return target_filename

def create_frames(video_file_location, output_directory):
    try:
        validate_video_file(video_file_location)
        validate_output_filepath(output_directory)
        current_frame = 0
        video = create_video_capture(video_file_location)
        
        # Process frames until there are no frames left.
        print("Creating frames...")
        while(True): 
            ret, frame = video.read() 
        
            if ret:  
                # Write the current frame to disk. 
                frame_name = output_directory + os.sep + "frame_" + str(current_frame).zfill(6) + '.PNG' 
                cv2.imwrite(frame_name, frame) 
                current_frame += 1
            else: 
                break
        
        # Release all space and windows once frame creation is complete.
        video.release() 
        cv2.destroyAllWindows()
        print("Done!\nFrames are located at: " + output_directory)
    except:
        print("An error occurred when seperating the video into frames for the video at " + output_directory + ".")
        quit()

def validate_time(time):
    try:
        time = str(time)
        min_sec_pattern = re.compile('(^\d{1,2}):(\d{1,2}):(\d{1,2})$')
        if (time == '0'):
            return 0
        elif (min_sec_pattern.match(time)):
            return convert_to_seconds(time)
        elif (float(time)):
            return round(float(time), 2)
        else:
            raise ValueError
    except ValueError:
        print("Error: Time format not found for input " + str(time) + ", please check -h (help) for appropriate formats.")
        quit()

def create_video_capture(filepath):
    return cv2.VideoCapture(filepath)

def convert_to_seconds(time_string):
    try:
        # Convert string HH:MM:SS to seconds, validation should occur before this function is called.
        time_array = time_string.split(':')
        return round(float(time_array[0])*60*60 + float(time_array[1])*60 + float(time_array[2]), 2)
    except:
        print("An error occured when converting the input time into seconds.")
        quit()

def get_args():
    parser = argparse.ArgumentParser(description="Process a video")
    parser.add_argument('-c', action='store_true', required=False, help="Change settings before outputting video", dest="settings", )
    parser.add_argument('-i', type=validate_filepath_arg, required=True, help="File path for the input video", dest="filepath")
    parser.add_argument('-s', type=validate_time, required=False, default=0, help="Start trim time (optional) -- valid formats: HH:MM:SS or a decimal value in seconds (ex 0.5 = 500 milliseconds)", dest="start_time")
    parser.add_argument('-e', type=validate_time, required=False, default=-1, help="End trim time (optional) -- valid formats: HH:MM:SS or a decimal value in seconds (ex 0.2 = 200 milliseconds)", dest="end_time")
    args = parser.parse_args()

    # Modify settings if -c is passed.
    if (args.settings):
        change_settings()

    if not (os.path.isfile(args.filepath)):
        print("Error: Inputted filepath is not a file.")
        quit()

    # Calculate the length of the video to verify inputs
    if not (validate_video_file(args.filepath)):
        print("Error: Video file at " + args.filepath + " is not a valid mp4 file.")
        quit()

    video = create_video_capture(args.filepath)
    video_length = validate_time(video.get(cv2.CAP_PROP_FRAME_COUNT) / int(video.get(cv2.CAP_PROP_FPS)))

    if (args.end_time == -1):      
        args.end_time = video_length
    if (args.end_time < 0 or args.start_time < 0):
        print("Error: Trim time cannot be less than 0 seconds.")
        quit()
    if (args.end_time <= args.start_time):
        print("Error: End time must be greater than start time.")
        quit()
    if (args.end_time > video_length):
        print("Error: End time is longer than the length of the video.")
        quit()
    return args

def get_settings(settings_filename, output_path_index):
    full_filepath = os.path.join(sys.path[0], settings_filename)
    if not (os.path.isfile(full_filepath)):
        print("Settings file does not exist, we must create one first.")
        create_settings(settings_filename, output_path_index)
    with open(full_filepath) as input_file:
        settings = json.load(input_file)

    # Check to make sure the output filepath exists before returning it
    if not (validate_settings_filepath(settings, output_path_index)):
        print("Output file path is corrupted, please enter a new one.")
        create_settings(settings_filename, output_path_index)
        return get_settings(settings_filename, output_path_index)
    return settings

def change_settings():
    create_settings(SETTINGS_FILENAME, OUTPUT_PATH_INDEX)
    
def create_settings(settings_filename, output_index):
    settings_dict = {}

    while (True):
        output_path = input("Enter a default output folder: ")
        setup_complete = os.path.isdir(output_path)

        if (setup_complete):
            # Clean up the file path by inputting it into pathlib. 
            settings_dict[output_index] = str(Path(output_path).absolute())
            break
        else:
            print("Inputted folder location does not exist, please try again.")

    # Add all settings to the settings json file.
    with open (settings_filename, 'w') as output_file:
        json.dump(settings_dict, output_file, indent=4)

def validate_settings_filepath(settings, output_path_index):
    return os.path.isdir(settings[output_path_index])

def validate_output_filepath(filepath):
    return os.path.isdir(filepath)

def validate_video_file(filepath):
    return Path(filepath).suffix.lower() == ".mp4"

# Entrance into the application.
SETTINGS_FILENAME = 'settings.json'
OUTPUT_PATH_INDEX = 'output_location'
arguments = get_args()
settings = get_settings(SETTINGS_FILENAME, OUTPUT_PATH_INDEX)
output_directory = create_directory(settings[OUTPUT_PATH_INDEX], arguments.filepath)
output_file = str(Path(output_directory).parent) + os.sep + os.path.basename(arguments.filepath)
create_frames(trim_video(arguments.filepath, output_file, arguments.start_time, arguments.end_time), output_directory)