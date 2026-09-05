
from PySide6.QtWidgets import (
    QMainWindow
)
from PySide6.QtCore import QUrl 
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput

class VideoPlayer(QMainWindow):
    """ Handles the Video Logic """
    def __init__(self,ui_instance,video_url):
        print("Path",video_url,ui_instance)
        self.ui = ui_instance

        # Initialize Media Player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)


        # Connect UI Buttons
        self.ui.play_button.clicked.connect(self.player.play)
        self.ui.pause_button.clicked.connect(self.player.pause)

        # Output
        self.player.setVideoOutput(self.ui.video_area)
        
        self.player.setSource(QUrl.fromLocalFile(video_url))

        