import cv2
import os
import dlib
import numpy as np

# --------------------- 1. Path ---------------------
image_path = input("Please input the path of the image: ") + '/' # path

# Dlib frontal face detector
detector = dlib.get_frontal_face_detector()

# --------------------- 2. Detect the faces ---------------------
def main():
    dirs = os.listdir(image_path) # path
    times = 1

    for i in range(0, len(dirs)):
        # the path of the images
        dirs_a = os.listdir(image_path) # path
        path_read_a = image_path + str(dirs_a[i]) + '/' # path
        
        # go into the sub folder
        for j in range(0, 3):
            sub_dirs = os.listdir(path_read_a)
            path_read_b = path_read_a + str(sub_dirs[j]) + "/"
            for k in range(0, 3):
                sub_dirs2 = os.listdir(path_read_b)
                path_read_c = path_read_b + str(sub_dirs2[k]) + "/"
                imgs = os.listdir(path_read_c)
                
                # in case of the number of the images is too large
                # pick the images every 10
                for c in range(0, len(imgs)):
                    # copy the image every 10 files and delete other files
                    if c > 20:
                        if c % 20 != 0:
                            path_read_1 = path_read_c + str(imgs[c])
                            os.remove(path_read_1)
                            print(path_read_1)
                imgs = os.listdir(path_read_c)
                
                # Read the images
                for b in range(0, len(imgs)):
                    path_read_2 = path_read_c + str(imgs[b])
                    img = cv2.imread(path_read_2)
                    print()
                    print(path_read_2 + imgs[b])

                    # store the images of the copied faces
                    path_save = path_read_2
                    faces = detector(img, 1)
                    print("faces in all:", len(faces))

# --------------------- 3. Crop the faces and save ---------------------
                    for num, face in enumerate(faces):
                        # Calculate the size of the rectangle
                        height = face.bottom() - face.top()
                        width = face.right() - face.left()

                        # produce a blank image
                        img_blank = np.zeros((height, width, 3), np.uint8)

                        for i in range(height - 2):
                            for j in range(width - 2):
                                src_x = face.left() + j - 1
                                src_y = face.top() + i - 1

                                # Check if pixel coordinates are out of bounds
                                if 0 <= src_x < img.shape[1] and 0 <= src_y < img.shape[0]:
                                    img_blank[i - 1][j - 1] = img[src_y][src_x]
                                else:
                                    # When pixel is out of bounds, fill with nearest neighbor pixel value
                                    nearest_x = max(0, min(src_x, img.shape[1] - 1))
                                    nearest_y = max(0, min(src_y, img.shape[0] - 1))
                                    img_blank[i - 1][j - 1] = img[nearest_y][nearest_x]

                        # save the image
                        print("Save into:", path_save + str(imgs[b]) + ".jpg")
                        cv2.imwrite(path_save, img_blank)
                        print( )

# --------------------- 4. Count the number of the images ---------------------
        times += 1
        print()
        print("This is the " + str(times) + "th video")
        print()

if __name__ == '__main__':
    main()
