import cv2
import os
import dlib
import numpy as np

# --------------------- 1. Path ---------------------
# Ask user to input the path of the video
video_path = input("Please input the path of the video: ") + '/' # path a
# Ask user to input the path of the storing folder
store_path = input("Please input the path of the storing folder: ") + '/' # path b


# --------------------- 2. Create Folder ---------------------
# Create the same folder as the original folder
dirs = os.listdir(video_path) #path a
for i in range(0, len(dirs)):
    os.mkdir(store_path + dirs[i] + '/') # path b


# Dlib frontal face detector
detector = dlib.get_frontal_face_detector()

def main():
# --------------------- 3. Video to Images ---------------------
    dirs = os.listdir(video_path) # path a
    times = 1 # count the number of videos
    
    for i in range (0, len(dirs)): 
        print("This is the " + str(i) + "th video")
        
        # list all the videos in the folder and read them one by one
        dirs = os.listdir(video_path) # path a
        videoFile = video_path + str(dirs[i]) + '/video.mp4' # path a
        outputFile = store_path + str(dirs[i]) + '/' # path b
        
        # read the video
        vc = cv2.VideoCapture(videoFile)
        c = 1
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            print('openerror!')
            rval = False

        # Time interval between each frame
        timeF = 5
        while rval:
            print(1)
            rval, frame = vc.read()
            if c % timeF == 0:
                print(2)
                # Check if 'frame' is empty before writing
                if frame is not None and frame.size > 0:
                    # frame is not empty, save it
                    cv2.imwrite(outputFile + str(int(c / timeF)) + '.jpg', frame)
                else:
                    print("Frame is empty. Skipping.")

            c += 1
            cv2.waitKey(1)
        vc.release()


# --------------------- 4. Read images ---------------------
        # the path of the images
        dirs = os.listdir(store_path) # path b
        path_read = store_path + str(dirs[i]) + "/"  # path b
        imgs = os.listdir(path_read)
        
        # in case the number of images is too large:
        # pick the images every 10
        for c in range(0, len(imgs)):
            # copy the image every 10 files and delete other files
            if c > 10:
                if c % 10 != 0:
                    path_read_1 = path_read + str(imgs[c])
                    os.remove(path_read_1)
                    print(path_read_1)
        imgs = os.listdir(path_read) 
        
        for b in range(0, len(imgs)):
            # Read the images
            path_read_2 = path_read + str(imgs[b])
            img = cv2.imread(path_read_2)
            print()
            print(path_read_2 + imgs[b])

# --------------------- 5. Crop and Save ---------------------
            # store the images of the coped faces
            path_save = path_read_2
            # detect the faces
            faces = detector(img, 1)
            print("faces in all:", len(faces))

            # crop the faces
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

                        # check if pixel coordinates are out of bounds
                        if 0 <= src_x < img.shape[1] and 0 <= src_y < img.shape[0]:
                            img_blank[i - 1][j - 1] = img[src_y][src_x]
                        else:
                            # if pixel is out of bounds, fill with nearest neighbor pixel valueq
                            nearest_x = max(0, min(src_x, img.shape[1] - 1))
                            nearest_y = max(0, min(src_y, img.shape[0] - 1))
                            img_blank[i - 1][j - 1] = img[nearest_y][nearest_x]

                # save the image
                print("Save into:", path_save + str(imgs[b]) + ".jpg")
                cv2.imwrite(path_save, img_blank)
                print( )

# --------------------- 6. Count the number of videos ---------------------
        times += 1
        print()
        print("This is the" + str(times) + "th video")
        print()

if __name__ == '__main__':
    main()

