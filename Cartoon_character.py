# Importing Required Libraries
import os
import sys
import time
import shutil
import cv2
import numpy as np


class Cartoon:

    def __init__(self):
        self.IMG_EXT = ["jpg", "jpeg", "png", "bmp"]
        self.VID_EXT = ["avi", "mp4"]
        self.CLASSES = 'cfg/cartoon.names'
        self.CONFIG = 'cfg/yolov2.cfg'
        self.WEIGHTS = 'cfg/cartoon_yolo.weights'
        # self.FILE = 'images/shin-chan2.jpg'  # can be video, can be image
        self.CONFIDENCE = 0.5
        self.NMS_THRESHOLD = 0.3
        self.SCALE = 0.00392

        # self.FILE = 'images/shin-chan2.jpg'  # can be video, can be image
        self.FILE = ''  # can be video, can be image
        self.characterName = ''
        self.timestamps = []

        # Validation of Paths / Files
        if not os.path.exists(self.CLASSES):
            sys.exit("[ERROR] Invalid classes path given")
        if not os.path.exists(self.CONFIG):
            sys.exit("[ERROR] Invalid config path given")
        if not os.path.exists(self.WEIGHTS):
            sys.exit("[ERROR] Invalid weights path given")
        # if not os.path.exists(self.FILE):
        #     sys.exit("[ERROR] Invalid file path given")

        # # put at match character
        # # clear output first
        output_dir = 'output/'
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
            except OSError as e:
                print("Error: %s : %s" % (output_dir, e.strerror))

        # make output directory
        os.mkdir(output_dir)

        self.MODE = "image"

        # Read Class names from CLASSES
        print("[INFO] Loading Classes from : ", self.CLASSES)
        self.classes = None
        try:
            with open(self.CLASSES, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]
            f.close()
            print("[INFO] Classes loaded successfully")
        except:
            sys.exit("[ERROR] File Exception Occured")

        # Generating different colors for different classes
        print("[INFO] Generating colors for different classes")
        self.COLORS = [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
            [255, 255, 0],
            [0, 255, 255]
        ]

        # Loading DNN from config and weights file
        print("[INFO] Loading Model from : ", self.WEIGHTS, self.CONFIG)
        self.net = cv2.dnn.readNet(self.WEIGHTS, self.CONFIG)
        print("[INFO] Model loaded successfully")

        # Retriving Output Layers
        layers_names = self.net.getLayerNames()
        self.output_layers = [layers_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    # ========================   detect character function   ===============================

    # Function to draw bounding boxes
    def draw_BBox(self, image, class_id, confidence, x, y, x_plus_width, y_plus_height):
        label = str(self.classes[class_id]) + " " + str(round(confidence * 100, 2)) + "%"
        color = self.COLORS[class_id]
        cv2.rectangle(image, (x, y), (x_plus_width, y_plus_height), color, 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Function to Process Image - Forward Propogation, NMS, BBox
    def process_Image(self, image, index):
        # print("[INFO] Processing Frame : ", (index + 1))

        # Retriving dimensions of image
        # print("[INFO] Image Dimension : ", image.shape)
        width = image.shape[1]
        height = image.shape[0]

        # Create Input blob, and set input for network
        blob = cv2.dnn.blobFromImage(image, self.SCALE, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)

        # Forward Propogation - inference
        outs = self.net.forward(self.output_layers)

        # Initialization of variables (lists)
        class_ids = []
        confidences = []
        boxes = []

        # For each detection from each output layer, get the confidence, class id and BBox params
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # Thresholding
                if confidence > self.CONFIDENCE:
                    # Calculating BBox params
                    c_x = int(detection[0] * width)
                    c_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = c_x - w / 2
                    y = c_y - h / 2

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # Applying NMS
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.CONFIDENCE, self.NMS_THRESHOLD)

        self.isFrameMatched = False

        # Draw final BBoxes
        for ind in indices:
            i = ind[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            self.draw_BBox(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            self.characterName = self.classes[class_ids[i]]
            self.isFrameMatched = True
            # print("[Prediction] Class : ", self.classes[class_ids[i]])
            # print("[Prediction] Score : ", round(confidences[i] * 100, 6))

        # Storing Image ================= make sure have folder output
        if self.MODE == "image":
            cv2.imwrite("output/output." + self.ext, image)

    def detectCharacter(self):
        start = time.time()
        # Loading input file and processing
        if self.MODE == "image":
            img = cv2.imread(self.FILE, cv2.IMREAD_COLOR)
            self.process_Image(img, 1)

        if self.MODE == "video":
            cap = cv2.VideoCapture(self.FILE)
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            # Change fourcc according to video format supported by your device
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # (*'XVID')
            op_vid = cv2.VideoWriter("output_video." + self.ext, fourcc, fps,
                                     (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

            index = 0
            self.timestamps.clear()

            while (cap.isOpened()):
                # Reading video frame by frame
                ret, frame = cap.read()
                numOfFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                if ret:
                    frameTimestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))  # in milliseconds - times by 1000
                    self.timestamps.append(frameTimestamp)

                    self.process_Image(frame, index)
                    index += 1
                    op_vid.write(frame)
                    if not self.isFrameMatched:
                        #  name = './'+ capt_folder + '/frame' + str(currentFrame).zfill(4) + '.jpg'
                        output_frame_name = "output/output_" + self.characterName + str(index).zfill(5) + "." + "png"
                        cv2.imwrite(output_frame_name, frame)

                else:
                    break

            cap.release()
            op_vid.release()

        end = time.time()
        total_time = round(end - start, 2)
        print("[INFO] Time : {} sec".format(total_time))

        # [Num of Frame] - 154
        # [number of timestamp] - 153
        # BEAN

        # print("[Timestamp] - ")
        # print(self.timestamps)
        #
        # print('\n\n\n\n[Num of Frame] - ' + str(numOfFrame))
        # print(len(self.timestamps))

    def checkVideo(self):
        return 0

    # ============================    set and get function   ============================================

    def setFileName(self, fileName):
        if not os.path.exists(fileName):
            sys.exit("[ERROR] Invalid file path given")
        else:
            self.FILE = fileName

        self.ext = self.FILE.split('.')[-1]
        if self.ext in self.IMG_EXT:
            self.MODE = "image"
        elif self.ext in self.VID_EXT:
            self.MODE = "video"
        else:
            error_msg = "[ERROR] Invalid file format, supported file formats are : " + str(self.IMG_EXT) \
                        + " " + str(self.VID_EXT)
            sys.exit(error_msg)

        print("[INFO] Processing mode set to : ", self.MODE)

    def setConfidence(self, confidence):
        if isinstance(confidence, float):
            self.CONFIDENCE = confidence

    def setThreshold(self, threshold):
        if isinstance(threshold, float):
            self.NMS_THRESHOLD = threshold

    def setScale(self, scale):
        if isinstance(scale, float):
            self.SCALE = scale

    def getCharacterName(self):
        charName = self.characterName.upper()
        return charName


if __name__ == '__main__':
    # main_win = MainWindow()
    # main_win.show()
    # sys.exit(app.exec_())

    cartoon = Cartoon()
    # dir = 'images/shin-chan2.jpg'
    dir = 'images/bean 5 secs.mp4'
    # dir = 'images/bean-10secs.mp4'
    cartoon.setConfidence(0.6)
    cartoon.setFileName(dir)
    cartoon.detectCharacter()
    print(cartoon.getCharacterName())