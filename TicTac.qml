import QtQuick 2.12
import QtGraphicalEffects 1.12

Item {
    signal clicked

    states: [
        State { name: "X"; PropertyChanges { target: image; source: "assets/x.png" } },
        State { name: "0"; PropertyChanges { target: image; source: "assets/o.png" } }
    ]

    Image {
        id: image
        anchors.centerIn: parent
        width: parent.width*0.6
        height: parent.height*0.6
    }

    FastBlur {
        anchors.fill: image
        source: image
        radius: 16
    }

    Glow {
        anchors.fill: image
        radius: 10
        samples: 17
        color: "silver"
        source: image
    }


    MouseArea {
        anchors.fill: parent
        onClicked: parent.clicked()
    }
}
