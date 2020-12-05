# Importing Required Libraries
import imutils
import os
import shutil
import sys
import time
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
        self.fileNames = []
        self.frame_accuracies = []
        # self.isFound = False
        self.accuracy_image = ''


        # to compare image with video
        self.isCharacterFound = False
        self.isImageMatchedVideo = False
        self.characterId = None
        self.characterToFindId = None
        self.characterMatchedId = None

        self.isVideoDetails = False
        self.videoWidth = 0
        self.videoHeight = 0
        self.videoFps = 0

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
        self.accuracy_image = str(round(confidence * 100, 2)) + '%'
        self.numAccuracy = round(confidence * 100, 2)
        # for video frame
        self.isCharacterFound = True

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

        self.isCharacterFound = False

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
            self.characterId = class_ids[i]

            # self.isFound = True
            # print("[Prediction] Class : ", self.classes[class_ids[i]])
            # print("[Prediction] Score : ", round(confidences[i] * 100, 6))

        # Storing Image ================= make sure have folder output
        if self.MODE == "image":
            if self.isVideoDetails == False:
                cv2.imwrite("output_image.png", image)
            else:
                saveFile = "output_image1.png"
                if os.path.exists(saveFile):
                    saveFile = "output_image2.png"
                    cv2.imwrite(saveFile, image)
                else:
                    cv2.imwrite(saveFile, image)


    def detectCharacter(self):
        # self.isFound = False
        start = time.time()
        # Loading input file and processing
        if self.MODE == "image":
            img = cv2.imread(self.FILE, cv2.IMREAD_COLOR)
            self.process_Image(img, 1)

        if self.MODE == "video":
            cap = cv2.VideoCapture(self.FILE)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            self.fpsStats = fps
            frameWidth = 600

            if self.isVideoDetails == True:
                frameWidth = self.videoWidth
                fps = self.videoFps

            ret, frame = cap.read()  # read first frame
            # - change width only
            frame = imutils.resize(frame, width=frameWidth)

            # Change fourcc according to video format supported by your device
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # (*'XVID') (*'MJPG')
            op_vid = cv2.VideoWriter("output_video." + self.ext, fourcc, fps, (frame.shape[1], frame.shape[0]))
            self.videoWidth = frame.shape[1]
            self.videoHeight = frame.shape[0]
            self.videoFps = fps


            index = 0
            self.timestamps.clear()
            self.fileNames.clear()
            self.frame_accuracies.clear()

            while cap.isOpened():
                # Reading video frame by frame
                ret, frame = cap.read()
                numOfFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.numOfFramestats = numOfFrame

                if ret:
                    frame = imutils.resize(frame, width=frameWidth)
                    frameTimestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000  # in milliseconds - times by 1000
                    frameTimestamp = "{:.3f}".format(frameTimestamp)

                    self.process_Image(frame, index)
                    index += 1
                    op_vid.write(frame)

                    if self.isCharacterFound and self.characterId == self.characterToFindId:
                        # if self.isCharacterFound and self.characterId == self.characterToFindId:  # is character =
                        # character / label
                        # print('charId : ' + str(self.characterId))
                        # print('charId to find : ' + str(self.characterToFindId))

                        self.isImageMatchedVideo = True

                        output_file = "output_" + self.characterName + str(index).zfill(5) + "." + "png"

                        output_frame_name = "output/" + output_file
                        fileName = 'output\\' + output_file

                        self.timestamps.append(str(frameTimestamp) + ' sec')
                        self.fileNames.append(fileName)
                        self.frame_accuracies.append(self.numAccuracy)
                        cv2.imwrite(output_frame_name, frame)
                else:
                    break

            cap.release()
            op_vid.release()

        end = time.time()
        total_time = round(end - start, 2)
        print("[INFO] Time : {} sec".format(total_time))
        # print(len(self.frame_accuracies))
        # print(self.timestamps)

        # delete when no match found - NO EFFECT
        # if not self.isImageMatchedVideo and self.MODE == "video":
        #     output_dir = 'output/'
        #     output_vid = 'output_video.mp4'
        #
        #     if os.path.exists(output_dir):
        #         try:
        #             shutil.rmtree(output_dir)
        #         except OSError as e:
        #             print("Error: %s : %s" % (output_dir, e.strerror))
        #
        #     if os.path.exists(output_vid):
        #         try:
        #             shutil.rmtree(output_vid)
        #         except OSError as e:
        #             print("Error: %s : %s" % (output_vid, e.strerror))

    def checkVideo(self):
        return 0

    # ============================    set and get function   ============================================

    def getFirstFrame(self, fileName):
        if not os.path.exists(fileName):
            sys.exit("[ERROR] Invalid config path given")

        firstFrameName = 'video_firstFrame.png'
        cap = cv2.VideoCapture(fileName)
        ret, frame = cap.read()  # read first frame
        cv2.imwrite(firstFrameName, frame)
        cap.release()

        return firstFrameName

    def setFileName(self, fileName):
        # reset all video status
        # to compare image with video
        # self.isCharacterFound = False
        # self.characterMatchedId = None

        self.isImageMatchedVideo = False
        self.characterId = None     # not a big prob - always change at ddraw
        self.characterToFindId = None

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

    def setCharacterToFindId(self, id):
        self.characterToFindId = id

    def setConfidence(self, confidence):
        if isinstance(confidence, float):
            self.CONFIDENCE = confidence

    def setThreshold(self, threshold):
        if isinstance(threshold, float):
            self.NMS_THRESHOLD = threshold

    def setScale(self, scale):
        if isinstance(scale, float):
            self.SCALE = scale

    def setWidth(self, width):
        if isinstance(width, int):
            self.videoWidth = width

    def setHeight(self, height):
        if isinstance(height, int):
            self.videoHeight = height

    def setFps(self, fps):
        if isinstance(fps, int):
            self.videoFps = fps

    def getCharacterName(self):
        charName = self.characterName.upper()
        return charName


if __name__ == '__main__':
    cartoon = Cartoon()
    # dir = 'input_images/shin-chan2.jpg'
    dir = 'input_images/bean 5 secs.mp4'
    # cartoon.setConfidence(0.6)
    cartoon.setFileName(dir)
    cartoon.detectCharacter()
