# First import the library
import pyrealsense2 as rs
import cv2
import numpy as np
import os
import time 

def startRsPipeline():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # Start streaming
    pipeline.start(config)
    return pipeline

def detecting(pipeline, width = 640, height = 360):

    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        return

    #Left search
    minDepthLeft = width
    minXLeft = 0
    step = 5

    leftThreshold = int(width/6)

    for x in range(leftThreshold,int(width/2),step):			
        for y in range(0,int(height), step):
            dist = depth_frame.get_distance(x, y)
            if (dist != 0 and dist < minDepthLeft):
                minDepthLeft = dist
                minXLeft = x

    #Right search
    minDepthRight = width
    minXRight = 0

    rightThreshold = int(width*5/6)
    for x in range(int(width/2),rightThreshold, step):			
        for y in range(0,int(height), step):
            dist = depth_frame.get_distance(x, y)
            if (dist != 0 and dist < minDepthRight):
                minDepthRight = dist
                minXRight = x

    depthThreshold = 0.6

    # if minDepthRight < depthThreshold:
    #     if minXRight < (width*3/4):
    #         print("Front: ", minDepthRight)

    #     else:
    #         print("Right: ", minDepthRight)

    # if minDepthLeft < depthThreshold:
    #     if minXLeft > (width/4):
    #         print("Front: ", minDepthLeft)

    #     else:
    #         print("Left: ", minDepthLeft)

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # Stack both images horizontally
    images = np.hstack((color_image, depth_colormap))

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    

def start(pipeline = None):
    if pipeline == None:
        pipeline = startRsPipeline()

    try:
        while True:
            detecting(pipeline)
            c = cv2.waitKey(1)
            if c == 27:
                break

    except Exception as e:
        pipeline.stop()
        print(e)

start()