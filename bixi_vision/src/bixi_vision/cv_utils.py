#! /usr/bin/env python
""" utility function for object detection
author: ren ye
changelog:
(2017-01-29) init
"""

import cv2
import numpy as np

# calibrated by palette
lower_red1 = np.array([0, 90, 90])
upper_red1 = np.array([25, 255, 255])
lower_red2 = np.array([175, 90, 90])
upper_red2 = np.array([255, 255, 255])
lower_blue = np.array([85, 90, 90])
upper_blue = np.array([130, 255, 255])
lower_green = np.array([25, 50, 75])
upper_green = np.array([75, 255, 255])

# void function for edge detector
def nothing(x):
    pass


#### canny edge function ####
def canny_masking(hsv_mask, threshold1=100, threshold2=200, is_dynamic=False):
    """ take a mask and return an edge """
    if is_dynamic:
        canny_hough_trackwindow(threshold1, threshold2)
        while (1):
            threshold1 = cv2.getTrackbarPos('Th_min', 'edge')
            threshold2 = cv2.getTrackbarPos('Th_max', 'edge')
            mask = cv2.Canny(hsv_mask, threshold1, threshold2,
                             L2gradient=True)
            cv2.imshow("edge", mask)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
    else:
        mask = cv2.Canny(hsv_mask, threshold1, threshold2,
                         L2gradient=True)
    return mask, threshold1, threshold2


def hough_line_detection(img, mask, hsv_mask, thresholdHough=40, minLineLength=10,
                    maxLineGap=5, is_dynamic=False, is_probabilistic=True):
    """ hough line detection """
    if is_probabilistic:
        if is_dynamic:
            hsv_masked_img = cv2.bitwise_and(img, img, mask=hsv_mask)
            canny_hough_trackwindow(None, None,
                                    thresholdHough, minLineLength, maxLineGap)
            while (1):
                # prob. hough lines
                thresholdHough = cv2.getTrackbarPos('Th_Hough', 'edge')
                minLineLength = cv2.getTrackbarPos('min_Linelength_Hough', 'edge')
                maxLineGap = cv2.getTrackbarPos('max_Linegap', 'edge')
                lines = cv2.HoughLinesP(mask.copy(), 1, np.pi/180,
                                       thresholdHough, minLineLength,
                                       maxLineGap)
                try:
                    print lines.shape
                    for l in lines:
                        for x1, y1, x2, y2 in l:
                            cv2.line(hsv_masked_img, (x1, y1), (x2, y2), (0,255,0), 2)
                except:
                    pass
                cv2.imshow("edge", hsv_masked_img)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
        else:
            hsv_masked_img = cv2.bitwise_and(img, img, mask=hsv_mask)
            lines = cv2.HoughLinesP(mask.copy(), 1, np.pi/180,
                                    thresholdHough, minLineLength,
                                    maxLineGap)
            try:
                print lines.shape
                for l in lines:
                    for x1, y1, x2, y2 in l:
                        cv2.line(hsv_masked_img, (x1, y1), (x2, y2), (0,255,0), 2)
            except:
                pass
            cv2.imshow("edge", hsv_masked_img)
            cv2.waitKey(0)
    else:
        if is_dynamic:
            canny_hough_trackwindow(None, None,
                                    thresholdHough, minLineLength, maxLineGap)
            while (1):
                hsv_masked_img = cv2.bitwise_and(img, img, mask=hsv_mask)
                lines = cv2.HoughLinesP(mask.copy(), 1, np.pi/180,
                                        thresholdHough, minLineLength,
                                        maxLineGap)
                try:
                    print lines.shape
                    for l in lines:
                        for rho, theta in l:
                            a = np.cos(theta)
                            b = np.sin(theta)
                            x0 = a*rho
                            y0 = b*rho
                            x1 = int(x0 + 1000*(-b))
                            y1 = int(y0 + 1000*(a))
                            x2 = int(x0 - 1000*(-b))
                            y2 = int(y0 - 1000*(a))
                            cv2.line(hsv_masked_img, (x1,y1), (x2,y2), (0,255,0), 2)
                except:
                    pass
                cv2.imshow("edge", hsv_masked_img)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
        else:
            hsv_masked_img = cv2.bitwise_and(img, img, mask=hsv_mask)
            lines = cv2.HoughLinesP(mask.copy(), 1, np.pi/180,
                                    thresholdHough, minLineLength,
                                    maxLineGap)
            try:
                print lines.shape
                for l in lines:
                    for rho, theta in l:
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + 1000*(-b))
                        y1 = int(y0 + 1000*(a))
                        x2 = int(x0 - 1000*(-b))
                        y2 = int(y0 - 1000*(a))
                        cv2.line(hsv_masked_img, (x1,y1), (x2,y2), (0,255,0), 2)
            except:
                pass
            cv2.imshow("edge", hsv_masked_img)
            cv2.waitKey(0)


def canny_hough_trackwindow(threshold1=None, threshold2=None,
                            thresholdHough=None, minLineLength=None,
                            maxLineGap=None):
    """create track window for canny and hough"""
    # debugging use for user to dynamic change the thresholds
    if threshold1 == None:
        threshold1 = 100
    if threshold2 == None:
        threshold2 = 200
    if thresholdHough == None:
        thresholdHough = 40
    if minLineLength == None:
        minLineLength = 10
    if maxLineGap == None:
        maxLineGap = 5

    cv2.namedWindow("edge")
    cv2.createTrackbar('Th_min', 'edge', threshold1, 255, nothing)
    cv2.createTrackbar('Th_max', 'edge', threshold2, 255, nothing)
    cv2.createTrackbar('Th_Hough', 'edge', thresholdHough, 200, nothing)
    cv2.createTrackbar('min_Linelength_Hough', 'edge', minLineLength, 200, nothing)
    cv2.createTrackbar('max_Linegap', 'edge', maxLineGap, 100, nothing)


#### hsv ####
def hsv_trackwindow(colorname="blue"):
    """ tracked window for hsv thresholding """

    # convert to hsv and do color filtering
    cv2.namedWindow("hsv")
    if colorname == 'blue':
        cv2.createTrackbar('Hl', 'hsv', lower_blue[0], 255, nothing)
        cv2.createTrackbar('Hu', 'hsv', upper_blue[0], 255, nothing)
        cv2.createTrackbar('Sl', 'hsv', lower_blue[1], 255, nothing)
        cv2.createTrackbar('Su', 'hsv', upper_blue[1], 255, nothing)
        cv2.createTrackbar('Vl', 'hsv', lower_blue[2], 255, nothing)
        cv2.createTrackbar('Vu', 'hsv', upper_blue[2], 255, nothing)
    elif colorname == 'red':
        cv2.createTrackbar('Hl', 'hsv', lower_red1[0], 255, nothing)
        cv2.createTrackbar('Hu', 'hsv', upper_red1[0], 255, nothing)
        cv2.createTrackbar('Sl', 'hsv', lower_red1[1], 255, nothing)
        cv2.createTrackbar('Su', 'hsv', upper_red1[1], 255, nothing)
        cv2.createTrackbar('Vl', 'hsv', lower_red1[2], 255, nothing)
        cv2.createTrackbar('Vu', 'hsv', upper_red1[2], 255, nothing)
    elif colorname == 'green':
        cv2.createTrackbar('Hl', 'hsv', lower_green[0], 255, nothing)
        cv2.createTrackbar('Hu', 'hsv', upper_green[0], 255, nothing)
        cv2.createTrackbar('Sl', 'hsv', lower_green[1], 255, nothing)
        cv2.createTrackbar('Su', 'hsv', upper_green[1], 255, nothing)
        cv2.createTrackbar('Vl', 'hsv', lower_green[2], 255, nothing)
        cv2.createTrackbar('Vu', 'hsv', upper_green[2], 255, nothing)


def hsv_masking(img, colorname="blue", is_dynamic=False):
    """ masking color image by color """

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if is_dynamic:
        hsv_trackwindow(colorname)
        while (1):
            hsv_mask = cv2.inRange(img_hsv,
                                   np.array([cv2.getTrackbarPos('Hl', 'hsv'),
                                             cv2.getTrackbarPos('Sl', 'hsv'),
                                             cv2.getTrackbarPos('Vl', 'hsv')]),
                                   np.array([cv2.getTrackbarPos('Hu', 'hsv'),
                                             cv2.getTrackbarPos('Su', 'hsv'),
                                             cv2.getTrackbarPos('Vu', 'hsv')]))

            cv2.imshow("hsv", hsv_mask)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
    else:
        if colorname == "blue":
            hsv_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
        elif colorname == "green":
            hsv_mask = cv2.inRange(img_hsv, lower_green, upper_green)
        elif colorname == "red":
            hsv_mask = cv2.inRange(img_hsv, lower_red1, upper_red1) + \
                cv2.inRange(img_hsv, lower_red2, upper_red2)
    return hsv_mask


#### contour detector ####
def find_contour(mask):
    # find all contours
    hierarchy, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

    # save the moments
    for i, cnt in enumerate(contours):
        print 'no: ', i
        # area and perimeter
        area = cv2.contourArea(cnt)
        print 'area: ', area
        arclength = cv2.arcLength(cnt, True)
        print 'arc length: ', arclength
        # centroid
        M = cv2.moments(cnt)
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
        print 'centroid: ', (centroid_x, centroid_y)
        cv2.circle(img, (centroid_x, centroid_y), 1, (0, 0, 255), -1)
        # aspect ratio
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        aspect_ratio = float(w) / h
        print 'aspect ratio: ', aspect_ratio
        # extent
        rect_area = w * h
        extent = float(area) / rect_area
        print "extent: ", extent
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 1)
        # mimimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        print 'circle_center: ', center
        cv2.circle(img, center, 1, (255, 0, 255), -1)
        # cv2.circle(img, center, radius, (0,255,0), 2)
        # solidity
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
        print 'solidity: ', solidity
        # orientation
        ellipse = cv2.fitEllipse(cnt)
        (x, y), (MA, ma), angle = ellipse
        print 'orientation: ', angle
        print 'ellipse center: ', (x, y)
        cv2.ellipse(img, ellipse, (0, 0, 255), 1)

        cv2.imshow("image", img)
        cv2.waitKey(0)
