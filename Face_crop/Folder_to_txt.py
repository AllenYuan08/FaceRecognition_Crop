import os

def main():
# --------------------- 1. Path ---------------------
    dir = input("Please input the dir path: ") + '/'
    dirs = os.listdir(dir)
    
# --------------------- 2. Create txt ---------------------
    file_path = 'TXT_FILE_PATH' + '.txt' # path edit
    file_create = open(file_path, 'w')
    file_create.close()
    
# --------------------- 3. Write the txt ---------------------
    label = input("Please input the label: ")
    time = 0

    with open(file_path, "w") as file:
        for i in range(0, len(dirs)):
            dirs_sub = os.listdir(str(dir) + str(dirs[i]) + "/")
            
            for j in range (0, len(dirs_sub)): 
                # print(dirs[i])
                # print(dirs_sub[j])
                file.write('CONTENT_TO_BE_WRITE') # path edit
                file.write('\n')
                
                time += 1
                print("Complete" +str(time) + "times")

if __name__ == '__main__':
    main()