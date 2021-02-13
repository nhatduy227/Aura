import pyrealsense2 as rs
from ObjectAvoidance import ObjectAvoidance 
from findObject import findObject 
import cv2

def startRsPipeline():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # Start streaming
    pipeline.start(config)
    return pipeline

def start(pipeline = None, mode = 1):
    if pipeline == None:
        pipeline = startRsPipeline()

    try:
        while True:
            if mode == 1:
                ObjectAvoidance(pipeline)
                c = cv2.waitKey(1)
                if c == 27:
                    break
            if mode == 2:
                findObject(pipeline)
                c = cv2.waitKey(1)
                if c == 27:
                    break

    except Exception as e:
        pipeline.stop()
        print(e)


if __name__ == '__main__':
    start(None,2)