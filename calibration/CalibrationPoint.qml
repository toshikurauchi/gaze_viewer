import QtQuick 2.15

Item {
    id: container
    property int cx: 0
    property int cy: 0
    property int radius: 40
    property bool done: false

    property color color: "white"

    x: cx - width / 2
    y: cy - height / 2
    width: 10 * radius
    height: width

    property int nFragments: 0

    function nextState() {
        for (let i = 0; i < calibPoint.states.length; i++) {
            if (calibPoint.states[i].name == calibPoint.state) {
                calibPoint.state = calibPoint.states[(i + 1) % calibPoint.states.length].name
                return
            }
        }
    }

    Rectangle {
        id: calibPoint

        property double rotationAcceleration: 1
        property double rotationSpeed: 0
        property double rotation: 0
        property double aspect: 1
        property double scale: 1

        property int cx: container.width / 2
        property int cy: container.height / 2
        x: cx - width / 2
        y: cy - height / 2

        color: container.color
        radius: container.radius
        width: radius * 2 * scale
        height: width * aspect
        state: "hidden"

        transform: Rotation {
            origin.x: calibPoint.width / 2
            origin.y: calibPoint.height / 2
            angle: calibPoint.rotation
        }

        Timer {
            interval: 15
            running: calibPoint.state == "focused"
            repeat: true
            onTriggered: {
                calibPoint.rotationSpeed = Math.min(calibPoint.rotationSpeed + calibPoint.rotationAcceleration, 15)
                calibPoint.rotation = (calibPoint.rotation + calibPoint.rotationSpeed) % 360
                calibPoint.aspect = Math.max(calibPoint.aspect - 0.02, 0.6)
                calibPoint.scale = Math.max(calibPoint.scale - 0.005, 0.6)
            }
        }

        states: [
            State {
                name: "hidden"
                PropertyChanges {
                    target: calibPoint
                    opacity: 0
                    rotationSpeed: 0
                    rotation: 0
                    aspect: 1
                    scale: 1
                }
                PropertyChanges {
                    target: container
                    nFragments: 0
                    done: false
                }
            },
            State {
                name: "shown"
                PropertyChanges {
                    target: calibPoint
                    opacity: 1
                    rotationSpeed: 0
                    rotation: 0
                    aspect: 1
                    scale: 1
                }
                PropertyChanges {
                    target: container
                    nFragments: 0
                    done: false
                }
            },
            State {
                name: "focused"
                PropertyChanges {
                    target: calibPoint
                    opacity: 1
                    rotationSpeed: 0
                    rotation: 0
                    aspect: 1
                    scale: 1
                }
                PropertyChanges {
                    target: container
                    nFragments: 0
                    done: false
                }
            },
            State {
                name: "done"
                PropertyChanges {
                    target: calibPoint
                    opacity: 0
                    rotationSpeed: 0
                    rotation: 0
                    aspect: 1
                    scale: 1
                }
                PropertyChanges {
                    target: container
                    nFragments: 6
                    done: true
                }
            }
        ]
    }

    Repeater {
        model: container.nFragments
        CalibrationPointFragment {
            size: calibPoint.width / 4
            cx: calibPoint.cx
            cy: calibPoint.cy
            angle: 360 / container.nFragments * index
            color: container.color
            speed: Math.random() * 3 + 2
        }
    }
}