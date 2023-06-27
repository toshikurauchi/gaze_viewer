import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    visibility: "FullScreen"
    width: 1024
    height: 768
    title: "Calibration"

    property double space: Math.min(10 * calibPoint.radius, Math.min(width, height) / 4)
    property var calibrationPositions: [
        {x: width / 2, y: height / 2},
        {x: space, y: height / 2},
        {x: width - space, y: height / 2},
        {x: width / 2, y: space},
        {x: width / 2, y: height - space},
        {x: space, y: space},
        {x: width - space, y: height - space},
        {x: width - space, y: space},
        {x: space, y: height - space},
    ]
    property int currentCalibrationIdx: 0

    Rectangle {
        anchors.fill: parent
        focus: true
        color: "black"
    
        Keys.onPressed: (event) => {
            if (event.key == Qt.Key_Space) {
                if (calibPoint.done) {
                    if (currentCalibrationIdx < calibrationPositions.length - 1) {
                        currentCalibrationIdx++;
                    }
                    else {
                        Qt.quit();
                    }
                }
                calibPoint.nextState();
            }
        }
    }

    CalibrationPoint {
        id: calibPoint
        cx: calibrationPositions[currentCalibrationIdx].x
        cy: calibrationPositions[currentCalibrationIdx].y
        radius: 10
    }
}