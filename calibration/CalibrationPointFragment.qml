import QtQuick 2.15

Rectangle {
    id: fragment
    property int size: 20
    radius: size / 2 * scale
    width: size * scale
    height: width
    color: "white"

    property int cx: 0
    property int cy: 0
    x: cx - radius
    y: cy - radius

    opacity: 1

    property double scale: 1
    property double speed: 5
    property double angle: 0

    property double speedX: Math.cos(angle * Math.PI / 180) * speed
    property double speedY: Math.sin(angle * Math.PI / 180) * speed
    property double gravity: 0.1

    property bool isMoving: true

    Timer {
        interval: 15
        running: fragment.isMoving
        repeat: true
        onTriggered: {
            fragment.opacity -= 0.05;
            fragment.scale = Math.max(0.2, fragment.scale - 0.01);
            fragment.speedY += fragment.gravity;
            fragment.x += fragment.speedX;
            fragment.y += fragment.speedY;

            if (fragment.opacity <= 0) {
                fragment.isMoving = false;
            }
        }
    }
}