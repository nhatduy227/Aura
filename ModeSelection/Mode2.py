import jetson.inference
import jetson.utils

#Constant
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.7)
camera = jetson.utils.videoSource("/dev/video2")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
info = jetson.utils.cudaFont()
distance=0.0
classs_dictionary = {'person': 1, 'cat': 17}
    
def FindObject(objName):    
    while display.IsStreaming():
        img = camera.Capture()
        detections = net.Detect(img)
        for detection in detections:
            info.OverlayText(img, 5, 5,"distance:{:.2f}".format(distance),int(detection.Left)+5, int(detection.Top)+35, info.White, info.Gray40)
            if objName in classs_dictionary:
                detect_value = classs_dictionary.get(objName)
                if detect_value == int(detection.ClassID): 
                    print('{} found'.format(objName))
            else: 
                print('Cannot find {}'.format(objName))
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

