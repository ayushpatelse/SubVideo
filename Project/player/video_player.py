
from PySide6.QtCore import ( QUrl, Slot,QTime, Qt)

from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput

class VideoPlayer:
    """ Handles the Video Logic """
    def __init__(self,ui_instance,video_url):
        self.ui = ui_instance
        self.subtitle_blocks = []

        # Initialize Media Player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.positionChanged.connect(self.update_video_timeline)
        self.player.positionChanged.connect(self.get_subtitle)
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
    def update_video_range(self,duration):
        """ Set's Video Duration"""
        
        self.ui.video_timeline.setRange(0,duration)

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
        
    def set_subtitle(self,data:list):
        """ Assign subtitle block """
        if data:
            self.subtitle_blocks = data
        else:
            raise ValueError("Data list is empty:",data)

    def get_subtitle(self,value):
        """ Get the subtitle accordting to the timeline"""
        
        for sub in self.subtitle_blocks:
            if sub.start_ms <= value <= sub.end_ms:
                html_list = "\n".join(sub.text)
                self.ui.subtitle_text.setText(html_list)
                return 

        self.ui.subtitle_text.clear()
 