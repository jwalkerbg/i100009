# qui/main.qml

import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Two Rows and Two Columns")

    GridLayout {
        anchors.centerIn: parent
        rows: 2
        columns: 2
        rowSpacing: 10
        columnSpacing: 10

        // First row
        ColumnLayout {
            Layout.alignment: Qt.AlignCenter
            Text {
                id: text1
                text: "Text 1"
            }
            Button {
                text: "Change Text 1"
                onClicked: text1.text = "Updated Text 1"
            }
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignCenter
            Text {
                id: text2
                text: "Text 2"
            }
            Button {
                text: "Change Text 2"
                onClicked: text2.text = "Updated Text 2"
            }
        }

        // Second row
        ColumnLayout {
            Layout.alignment: Qt.AlignCenter
            Text {
                id: text3
                text: "Text 3"
            }
            Button {
                text: "Change Text 3"
                onClicked: text3.text = "Updated Text 3"
            }
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignCenter
            Text {
                id: text4
                text: "Text 4"
            }
            Button {
                text: "Change Text 4"
                onClicked: text4.text = "Updated Text 4"
            }
        }
    }
}
