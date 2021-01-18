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
        self.CONFIDENCE = 0.5
        self.NMS_THRESHOLD = 0.3
        self.SCALE = 0.00392

        self.FILE = ''  # can be video, can be image
        self.characterName = ''
        self.timestamps = []
        self.fileNames = []
        self.frame_accuracies = []
        self.inputNameList = []

        self.outputImageFolderList = []
        self.outputVideoFolderList = []
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

        # Retrieving Output Layers
        layers_names = self.net.getLayerNames()
        self.output_layers = [layers_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    # ========================   detect character function   ===============================
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

        # Retrieving dimensions of image
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

        # Storing Image ================= make sure have folder output
        if self.MODE == "image":
            if self.isVideoDetails == False:
                cv2.imwrite("output\\output_imageInput.png", image)
            else:
                cv2.imwrite("output\\output_imageItem.png", image)

    # ============================    detection file functions   ============================================
    def detectCharacter(self):
        start = time.time()
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
            frame = imutils.resize(frame, width=frameWidth)

            # Change fourcc according to video format supported by your device
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # (*'XVID') (*'MJPG')
            op_vid = cv2.VideoWriter("output\\output_video." + "mp4", fourcc, fps, (frame.shape[1], frame.shape[0]))
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

    # ============================    detection folder functions   ============================================
    def process_Image_inFolder(self, image, index, count):
        width = image.shape[1]
        height = image.shape[0]
        blob = cv2.dnn.blobFromImage(image, self.SCALE, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)

        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

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

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.CONFIDENCE, self.NMS_THRESHOLD)

        self.isCharacterFound = False

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

        if self.MODE == "image" and self.isCharacterFound and self.characterId == self.characterToFindId:
            outputFile = "output\\output_" + self.characterName + str(count + 1) + ".png"
            self.outputImageFolderList.append(outputFile)
            self.frame_accuracies.append(self.numAccuracy)
            self.inputNameList.append(self.FILE)
            cv2.imwrite(outputFile, image)

    def detectCharacter_inFolder(self, count):
        start = time.time()
        if self.MODE == "image":
            img = cv2.imread(self.FILE, cv2.IMREAD_COLOR)
            self.process_Image_inFolder(img, 1, count)

        if self.MODE == "video":
            cap = cv2.VideoCapture(self.FILE)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frameWidth = 600

            if self.isVideoDetails == True:
                frameWidth = self.videoWidth
                fps = self.videoFps

            ret, frame = cap.read()
            frame = imutils.resize(frame, width=frameWidth)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoName = "output\\output_video" + str(count+1) + ".mp4"
            op_vid = cv2.VideoWriter(videoName, fourcc, fps, (frame.shape[1], frame.shape[0]))
            self.videoWidth = frame.shape[1]
            self.videoHeight = frame.shape[0]
            self.videoFps = fps

            index = 0
            accuracies = []

            while cap.isOpened():
                ret, frame = cap.read()

                if ret:
                    frame = imutils.resize(frame, width=frameWidth)

                    self.process_Image(frame, index)
                    index += 1
                    op_vid.write(frame)

                    if self.isCharacterFound and self.characterId == self.characterToFindId:
                        self.isImageMatchedVideo = True
                        accuracies.append(self.numAccuracy)

                else:
                    break

            cap.release()
            op_vid.release()

            if self.isImageMatchedVideo:
                sumAcc = sum(accuracies)
                avgAcc = round(sumAcc/len(accuracies), 2)
                self.outputVideoFolderList.append(videoName)
                self.frame_accuracies.append(avgAcc)
                self.inputNameList.append(self.FILE)
            else:
                os.remove(videoName)

        end = time.time()
        total_time = round(end - start, 2)
        print("[INFO] Time : {} sec".format(total_time))

    # ============================    set and get function   ============================================
    def getFirstFrame(self, fileName):
        if not os.path.exists(fileName):
            sys.exit("[ERROR] Invalid config path given")

        firstFrameName = 'UI Images\\video_firstFrame.png'
        cap = cv2.VideoCapture(fileName)
        ret, frame = cap.read()  # read first frame
        cv2.imwrite(firstFrameName, frame)
        cap.release()

        return firstFrameName

    def setFileName(self, fileName):
        self.isImageMatchedVideo = False
        self.characterId = None
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

