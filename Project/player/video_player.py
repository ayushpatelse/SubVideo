
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
        self.original_mousePressEvent = self.ui.video_timeline.mousePressEvent
        self.ui.video_timeline.mousePressEvent  = self.update_timeline_clicked  # Overiding the Slider Mouse Press event directly 

        # --- Audio Volume ---
        self.audio_output.setVolume(self.ui.volume_slider.value()/100)
        self.ui.volume_slider.valueChanged.connect(self.change_volume)

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

    @Slot(int)
    def update_time_display(self,position,duration):
        """ Converting milliseconds to Human-readable format """
        pos_time = QTime(0,0,0,0).addMSecs(position).toString("mm:ss")
        dus_time = QTime(0,0,0,0).addMSecs(duration).toString("mm:ss")

        # When duration is longer than an hour  (min * sec * milli)(60 * 60 * 1000) 
        if duration >= (3600000):
            pos_time = QTime(0,0,0,0).addMSecs(position).toString("hh:mm:ss")
            dus_time = QTime(0,0,0,0).addMSecs(duration).toString("hh:mm:ss")        
            
        self.ui.v_timeline_lablel.setText(f"{pos_time} / {dus_time}")

    def update_timeline_clicked(self,event):
        """ Calculating the User Click Position"""
        if event.button() == Qt.MouseButton.LeftButton:

            click_x = event.position().x() # get relative value of the slider
            timeline_width = self.ui.video_timeline.width()
            
            percentage = click_x / timeline_width

            slider_length = self.ui.video_timeline.maximum() - self.ui.video_timeline.minimum() 
            curr_click_val = int(self.ui.video_timeline.minimum() + ( slider_length * percentage))

            # snap to the new value
            self.player.setPosition(curr_click_val)

            # Accept the event so it stops propagating
            event.accept()

        # Using the original Slider method to handle timeline slide 
        self.original_mousePressEvent(event)

    @Slot(int)
    def change_volume(self,value):
        # Audio output value from 0.0 to 1.0 
        volume_val = value / 100
        self.audio_output.setVolume(volume_val)
        
        
        