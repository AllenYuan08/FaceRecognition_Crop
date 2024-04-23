import cv2
import os
import dlib
import numpy as np
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import shutil

def get_all_files(directory, extensions):
    """Retrieve all files with specified extensions in the given directory including subdirectories."""
    files = []
    for root, dirs, file_list in os.walk(directory):
        for file in file_list:
            if file.endswith(extensions):
                files.append((os.path.join(root, file), root))
    return files

def process_video(video_path, output_path, pbar=None):
    """Extract frames from video and save as images, aiming for 10 frames per video."""
    vc = cv2.VideoCapture(video_path)
    total_frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames
    timeF = max(1, total_frames // 10)  # Frame interval to capture 10 frames, ensuring at least 1

    frame_number = 0
    extracted_frames = 0  # Counter for extracted frames

    while vc.isOpened():
        rval, frame = vc.read()
        if not rval:
            break
        if frame_number % timeF == 0 and extracted_frames < 10:
            file_name = f'{extracted_frames:02d}.png'
            cv2.imwrite(os.path.join(output_path, file_name), frame)
            extracted_frames += 1
            if pbar:
                pbar.update(1)
        frame_number += 1
        
        if extracted_frames >= 10:
            break  # Exit loop after extracting 10 frames

    vc.release()

    if pbar:
        # Adjust the progress bar in case the video is shorter than expected
        pbar.update(10 - extracted_frames)

def process_image(args):
    """Detect face in an image, crop, resize and save to the specified directory."""
    img_path, crop_dir = args
    os.makedirs(crop_dir, exist_ok=True)  # Ensure the directory exists before saving the image
    detector = dlib.get_frontal_face_detector()
    img = cv2.imread(img_path)
    if img is None:
        return f"Error loading image: {img_path}"

    faces = detector(img, 1)
    if len(faces) > 0:
        face = faces[0]
        cropped_img = img[face.top():face.bottom(), face.left():face.right()]
        if cropped_img.size == 0:
            return f"Error: Cropped image is empty for {img_path}"
        resized_img = cv2.resize(cropped_img, (244, 244), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(crop_dir, os.path.basename(img_path)), resized_img)
        # No message returned for normal face detected cases
    else:
        # Get the center coordinates
        center_x, center_y = img.shape[1] // 2, img.shape[0] // 2
        # Calculate the 1/4 to 3/4 crop dimensions based on the image dimensions
        crop_width = img.shape[1] // 4
        crop_height = img.shape[0] // 4
        cropped_img = img[center_y - crop_height:center_y + crop_height, center_x - crop_width:center_x + crop_width]
        resized_img = cv2.resize(cropped_img, (244, 244), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(crop_dir, os.path.basename(img_path)), resized_img)
        return f"No face detected, center crop and resized to 244x244 for {os.path.basename(img_path)}"

    return ""  # Return an empty string for cases where face is detected and processed




def main():
    """Main function to handle video to image and image cropping processes."""
    mode = input("Please input the mode (V: only video2img, I: only image crop, B: Both): ")
    if mode not in ['V', 'I', 'B']:
        print("Invalid input, please enter V, I, or B.")
        return

    print("Please input the paths:")
    base_video_dir = input("Please input the video path: ")
    base_output_dir = input("Please input the image path: ")
    base_crop_dir = input("Please input the crop path: ")
    
    # base_video_dir = "/mnt/sdh/YHC_Work/test"
    # base_output_dir = "/mnt/sdh/YHC_Work/test_output"
    # base_crop_dir = "/mnt/sdh/YHC_Work/test_output_crop"

    if mode in ['V', 'B']:
        video_files = get_all_files(base_video_dir, ('.mp4', '.avi', '.mov', '.MOV'))
        total_frames_to_extract = 10 * len(video_files)  # Assuming each video contributes 10 frames
        with tqdm(total=total_frames_to_extract, desc='Video to Image Progress', unit='frame') as pbar:
            for video_path, root in video_files:
                output_subdir = os.path.relpath(root, base_video_dir)
                video_output_dir = os.path.join(base_output_dir, output_subdir, os.path.splitext(os.path.basename(video_path))[0])
                os.makedirs(video_output_dir, exist_ok=True)
                process_video(video_path, video_output_dir, pbar)

    if mode in ['I', 'B']:
        image_files = get_all_files(base_output_dir, ('.png',))
        with ProcessPoolExecutor() as executor:
            futures = []
            for img_path, root in image_files:
                crop_dir = os.path.join(base_crop_dir, os.path.relpath(root, base_output_dir))
                os.makedirs(crop_dir, exist_ok=True)
                future = executor.submit(process_image, (img_path, crop_dir))
                futures.append(future)
            for future in tqdm(as_completed(futures), total=len(futures), desc='Processing images', unit='img'):
                print(future.result())

if __name__ == '__main__':
    main()
