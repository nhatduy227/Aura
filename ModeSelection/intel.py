import pyrealsense2 as rs
from Mode1 import ObjectAvoidance
# from Mode2 import FindObject
from Mode3 import describe_video_stream
import cv2
import sys

def startRsPipeline():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # Start streaming
    pipeline.start(config)
    return pipeline


def start(pipeline=None, mode=1):
    if pipeline is None and mode != 2:
        pipeline = startRsPipeline()

    while True:
        if mode == 1:
            ObjectAvoidance(pipeline)
            c = cv2.waitKey(1)
            if c == 27:
                break
        elif mode == 2:
            FindObject('cat')
            break
        elif mode == 3:
            describe_video_stream(pipeline)
            break

if __name__ == '__main__':
    # start(None, int(sys.argv[1]))
    start(None,3)