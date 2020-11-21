# Importing Required Libraries
import os
import sys
import time
import shutil
import cv2
import numpy as np

# class Cartoon

SCALE = 0.00392

CLASSES = 'cfg/cartoon.names'
CONFIG = 'cfg/yolov2.cfg'
WEIGHTS = 'cfg/cartoon_yolo.weights'
FILE = 'images/shin-chan2.jpg'  # can be video, can be image
# FILE = 'image_detect/shin_2.jpg'  # can be video, can be image
CONFIDENCE = 0.5
NMS_THRESHOLD = 0.3

# Validation of Paths / Files
if not os.path.exists(CLASSES):
    sys.exit("[ERROR] Invalid classes path given")
if not os.path.exists(CONFIG):
    sys.exit("[ERROR] Invalid config path given")
if not os.path.exists(WEIGHTS):
    sys.exit("[ERROR] Invalid weights path given")
if not os.path.exists(FILE):
    sys.exit("[ERROR] Invalid file path given")

# clear output first
output_dir = 'output/'
if os.path.exists(output_dir):
    try:
        shutil.rmtree(output_dir)
    except OSError as e:
        print("Error: %s : %s" % (output_dir, e.strerror))

# make output directory
os.mkdir(output_dir)



# Retriving Mode : video or image based in input file's extension
# default is set to image
MODE = "image"
IMG_EXT = ["jpg", "jpeg", "png", "bmp"]
VID_EXT = ["avi", "mp4"]
ext = FILE.split('.')[-1]
if ext in IMG_EXT:
    MODE = "image"
elif ext in VID_EXT:
    MODE = "video"
else:
    error_msg = "[ERROR] Invalid file format, supported file formats are : " + str(IMG_EXT) + " " + str(VID_EXT)
    sys.exit(error_msg)

print("[INFO] Processing mode set to : ", MODE)

# Read Class names from CLASSES
print("[INFO] Loading Classes from : ", CLASSES)
classes = None
try:
    with open(CLASSES, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    f.close()
    print("[INFO] Classes loaded successfully")
except:
    sys.exit("[ERROR] File Exception Occured")

# Generating different colors for different classes
print("[INFO] Generating colors for different classes")
COLORS = [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 255, 0],
    [0, 255, 255]
]

# Loading DNN from config and weights file
print("[INFO] Loading Model from : ", WEIGHTS, CONFIG)
net = cv2.dnn.readNet(WEIGHTS, CONFIG)
print("[INFO] Model loaded successfully")

# Retriving Output Layers
layers_names = net.getLayerNames()
output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Function to draw bounding boxes
def draw_BBox(image, class_id, confidence, x, y, x_plus_width, y_plus_height):
    label = str(classes[class_id]) + " " + str(round(confidence * 100, 2)) + "%"
    color = COLORS[class_id]
    cv2.rectangle(image, (x, y), (x_plus_width, y_plus_height), color, 2)
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


# Function to Process Image - Forward Propogation, NMS, BBox
def process_Image(image, index):
    print("[INFO] Processing Frame : ", (index + 1))

    # Retriving dimensions of image
    print("[INFO] Image Dimension : ", image.shape)
    width = image.shape[1]
    height = image.shape[0]

    # Create Input blob, and set input for network
    blob = cv2.dnn.blobFromImage(image, SCALE, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Forward Propogation - inference
    outs = net.forward(output_layers)

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
            if confidence > CONFIDENCE:
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
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, NMS_THRESHOLD)

    # Draw final BBoxes
    for ind in indices:
        i = ind[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_BBox(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
        print("[Prediction] Class : ", classes[class_ids[i]])
        print("[Prediction] Score : ", round(confidences[i] * 100, 6))

    # Storing Image ================= make sure have folder output
    if MODE == "image":
        cv2.imwrite("output/output." + ext, image)


start = time.time()
# Loading input file and preocessing
if MODE == "image":
    img = cv2.imread(FILE, cv2.IMREAD_COLOR)
    process_Image(img, 1)


if MODE == "video":
    cap = cv2.VideoCapture(FILE)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Change fourcc according to video format supported by your device
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') #(*'XVID')
    op_vid = cv2.VideoWriter("output." + ext, fourcc, 30,
                             (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # cv.VideoWriter(	filename, fourcc, fps, frameSize[, isColor]	)

    index = 0

    while (cap.isOpened()):
        # Reading video fraom by frame
        ret, frame = cap.read()

        if ret:
            process_Image(frame, index)
            index += 1
            op_vid.write(frame)

        else:
            break

    cap.release()
    op_vid.release()

end = time.time()
total_time = round(end - start, 2)
print("[INFO] Time : {} sec".format(total_time))
# print(str(fps) + "---" + str(fps1))

# python cartoon.py --classes cfg/cartoon.names --config cfg/yolov2.cfg --weights cartoon_yolo.weights --file image_detect/shin_2.jpg
# python cartoon.py --classes cfg/cartoon.names --config cfg/yolov2.cfg --weights cartoon_yolo.weights --file image_detect/shin_2.jpg --confidence 0.8 --threshold 0.5
