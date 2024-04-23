# FaceRecognition_Crop
A method can detect Faces in images and crop them which is useful for Face Datasets Processing

The newest version: video2img_crop.py

Instructions:
1. First, choose mode: V for video to image; I for face detection and crop; B for both.
2. Then, input the corresponding paths, if choose V or I, you can leave the other path blank or simple input "XXX".
3. Take B as an example:

   (1) Program will first read videos from the video_path, and extract 10 frames evenly and save them into the img_path.
   
   (2) Then, the program will read the images from the img_path and start face detection using dlib front detector with parallel cpu calculations to improve efficiency.
   
       i. If a face is detected, the program will crop the face and resize it into 244*244;
   
       ii. If faces are not detected, the program will present a central crop (size according to each images) and then resize it into 244*244.
   
   (3) Finally, the program will store the cropped images into the crop_path.

 The whole precedure can be seen from a tqdm progress bar。


Inspired by: https://github.com/coneypo/Dlib_face_cut
灵感来源于：https://github.com/coneypo/Dlib_face_cut
