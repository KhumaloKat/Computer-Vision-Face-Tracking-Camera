import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.PIDModule import PID
from cvzone.PlotModule import LivePlot
from cvzone.SerialModule import SerialObject
cap = cv2.VideoCapture(0)

detector = FaceDetector(minDetectionCon=0.75)

arduino = SerialObject(digits=3, portNo="COM8")

# angle of the servo  - middle point of the face
xPID = PID([0.04, 0, 0.02], 640//2, axis=0)
yPID = PID([0.02, 0, 0.02], 200, axis=1)

xPlot = LivePlot(yLimit=[0, 640], char='X')
yPlot = LivePlot(yLimit=[0, 400], char='Y')

xAngle, yAngle = 105, 30

while True:
    _, img = cap.read()
    imgOut = img.copy()
    img, bboxs = detector.findFaces(img,draw = False)

    if bboxs:
        x, y, w, h = bboxs[0]['bbox']
        cx, cy = bboxs[0]['center']

        resx = int(xPID.update(cx))
        resy = int(yPID.update(cy))

        xAngle -= resx
        yAngle += resy

        imgPlotX = xPlot.update(cx)
        imgPlotY = yPlot.update(cy)

        imgOut = xPID.draw(imgOut, [cx, cy])
        imgOut = yPID.draw(imgOut, [cx, cy])

        imgstack = cvzone.stackImages([img, imgOut, imgPlotX, imgPlotY], 2, 0.5)
    else:
        imgstack = cvzone.stackImages([img, imgOut], 2, 0.5)

    arduino.sendData([xAngle, yAngle])

    cv2.imshow("Image", imgstack)
    cv2.waitKey(1)
