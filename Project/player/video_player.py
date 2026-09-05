
from PySide6.QtWidgets import (
    QMainWindow
)
from PySide6.QtCore import ( QUrl, Slot,QTime, Qt
                            )
 
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput

class VideoPlayer:
    """ Handles the Video Logic """
    def __init__(self,ui_instance,video_url):
        print("Path",video_url,ui_instance)
        self.ui = ui_instance

        # Initialize Media Player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.positionChanged.connect(self.update_video_timeline)
        self.player.durationChanged.connect(self.update_video_range)

        # Connect UI 

        # --- Button --- 
        self.ui.play_button.clicked.connect(self.player.play)
        self.ui.pause_button.clicked.connect(self.player.pause)

        # --- Video Timeline --- 
        self.ui.video_timeline.sliderMoved.connect(self.seek)
        
        # Output
        self.player.setVideoOutput(self.ui.video_area)
        self.player.setSource(QUrl.fromLocalFile(video_url))

    @Slot(int)
    def seek(self,mseconds):
        self.player.setPosition(mseconds)

    @Slot()
    def update_video_range(self):
        """ Set's Video Duration"""
        
        self.ui.video_timeline.setRange(0,self.player.duration())

    @Slot(int)
    def update_video_timeline(self,position):
        """ Update Timeline As Video Progress """
        self.ui.video_timeline.setValue(position)
        self.update_time_display(position,self.player.duration())

    def update_time_display(self,position,duration):
        """ Converting milliseconds to Human-readable format """
        pos_time = QTime(0,0,0,0).addMSecs(position).toString("mm:ss")
        dus_time = QTime(0,0,0,0).addMSecs(duration).toString("mm:ss")

        # When duration is longer than an hour  (min * sec * milli)(60 * 60 * 1000) 
        if duration >= (3600000):
            pos_time = QTime(0,0,0,0).addMSecs(position).toString("hh:mm:ss")
            dus_time = QTime(0,0,0,0).addMSecs(duration).toString("hh:mm:ss")        
            
        self.ui.v_timeline_lablel.setText(f"{pos_time} / {dus_time}")

            
        