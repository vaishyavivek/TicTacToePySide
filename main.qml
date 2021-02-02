import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12
import QtGraphicalEffects 1.12

ApplicationWindow {
    title: qsTr("Tic Tac Toe")
    width: 600
    height: 600
    visible: true


    Rectangle {
        id: game

        property bool running: true

        width: boardGrid.width
        height: boardGrid.height + 15

        Image {
            id: boardImage
            source: "assets/board.png"

            ColorOverlay{
                anchors.fill: boardImage
                source: boardImage
                color: "#80800000"
                opacity: 0.5
            }
        }

        Glow {
            anchors.fill: boardImage
            radius: 10
            samples: 17
            color: "white"
            source: boardImage
        }


        gradient: Gradient {
            GradientStop { position: 0.0; color: "darkgreen" }
            GradientStop { position: 0.65; color: "darkcyan" }
            GradientStop { position: 1.0; color: "darkgreen" }
        }

        Grid{
            id: boardGrid
            width: boardImage.width
            height: boardImage.height
            columns: 3

            Repeater {
                model: 9

                TicTac {
                    width: boardGrid.width/3
                    height: boardGrid.height/3

                    onClicked: {
                        if (game.running && canPlayAtPos(index)) {
                            if (!makeMove(index, "X"))
                                solver.smartAI()
                        }
                    }
                }
            }
        }

        Text {
            id: messageDisplay
            anchors.centerIn: parent
            color: "blue"
            style: Text.Outline; styleColor: "white"
            font.pixelSize: 50; font.bold: true
            visible: false

            Timer {
                running: messageDisplay.visible
                onTriggered: {
                    messageDisplay.visible = false;
                    restartGame();
                }
            }
        }
    }


    function canPlayAtPos(index) {
        return boardGrid.children[index].state === "";
    }

    function makeMove(index, player) {
        boardGrid.children[index].state = player
        solver.updateGrid(index, player)

        if (solver.isWinner()){
            gameFinished(player)
            return true
        }
        else
            return false
    }

    function gameFinished(player) {
        messageDisplay.text = player + " Won"
        messageDisplay.visible = true
        game.running = false
    }

    function restartGame() {
        game.running = true

        for (var i=0; i<9; ++i)
            boardGrid.children[i].state = ""
    }

    Connections {
        target: solver

        function onMakeMove(index, player) {
            boardGrid.children[index].state = player
        }

        function onZeroWon() {
            gameFinished('0')
        }

        function onMatchDraw() {
            messageDisplay.text = "Match Draw"
            messageDisplay.visible = true
            game.running = false
        }
    }
}
