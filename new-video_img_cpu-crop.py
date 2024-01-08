import cv2
import os
import dlib
import numpy as np
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import shutil

# Dlib frontal face detector
detector = dlib.get_frontal_face_detector()

def process_image(img_path, output_path, detector):
    img = cv2.imread(img_path)
    if img is None:
        return "Error loading image: " + img_path

    faces = detector(img, 1)
    if len(faces) > 0:
        # If a face is detected, crop the image to the face
        face = faces[0]  # only focus on the first and only face
        height = face.bottom() - face.top()
        width = face.right() - face.left()
        img_blank = np.zeros((height, width, 3), np.uint8)

        for i in range(height - 2):
            for j in range(width - 2):
                src_x = face.left() + j - 1
                src_y = face.top() + i - 1
                if 0 <= src_x < img.shape[1] and 0 <= src_y < img.shape[0]:
                    img_blank[i - 1][j - 1] = img[src_y][src_x]
                else:
                    nearest_x = max(0, min(src_x, img.shape[1] - 1))
                    nearest_y = max(0, min(src_y, img.shape[0] - 1))
                    img_blank[i - 1][j - 1] = img[nearest_y][nearest_x]

        cv2.imwrite(os.path.join(output_path, os.path.basename(img_path)), img_blank)
        return "Overwrote: " + os.path.join(output_path, os.path.basename(img_path))
    else:
        # If no face is detected, copy the original image
        shutil.copy(img_path, os.path.join(output_path, os.path.basename(img_path)))
        return "Copied original image: " + os.path.join(output_path, os.path.basename(img_path))

def process_video(video_path, output_path):
    vc = cv2.VideoCapture(video_path)
    c = 1
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        print('openerror!')
        rval = False

    timeF = 15  # Time interval between each frame

    while rval:
        rval, frame = vc.read()
        if c % timeF == 0 and frame is not None and frame.size > 0:
            cv2.imwrite(os.path.join(output_path, str(int(c / timeF)) + '.png'), frame)
        c += 1
        cv2.waitKey(1)
    vc.release()
    
    def get_all_video_files(base_dir):
        video_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.avi') or file.endswith('.mp4') or file.endswith('.MOV'):
                video_files.append((os.path.join(root, file), root))
    return video_files

def main():
    base_video_dir = 'VIDEO_PATH' # Remember to add '/' at the end
    base_output_dir = 'OUTPUT_PATH'  # Remember to add '/' at the end

    categories = ['attack', 'real']

    # Clip videos to images
    for category in categories:
        video_files = get_all_video_files(os.path.join(base_video_dir, category))
        with tqdm(total=len(video_files), desc=f'Video to Image Progress ({category})') as pbar:
            for video_path, root in video_files:
                subdir = os.path.basename(root)
                video_output_dir = os.path.join(base_output_dir, category, subdir, os.path.splitext(os.path.basename(video_path))[0])
                os.makedirs(video_output_dir, exist_ok=True)
                process_video(video_path, video_output_dir)
                pbar.update(1)

    # Crop faces
    for category in categories:
        crop_dir = os.path.join(base_output_dir, f'{category}_crop')
        image_paths = []
        for root, dirs, files in os.walk(os.path.join(base_output_dir, category)):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    image_paths.append((os.path.join(root, file), root.replace(category, f'{category}_crop')))

        with tqdm(total=len(image_paths), desc=f'Face Cropping Progress ({category})') as pbar:
            for img_path, crop_root in image_paths:
                os.makedirs(crop_root, exist_ok=True)
                process_image(img_path, crop_root, detector)
                pbar.update(1)

if __name__ == '__main__':
    main()