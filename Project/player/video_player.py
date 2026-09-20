
from PySide6.QtCore import ( QUrl, Slot,QTime, Qt)

from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from subtitles.tracker import SubtitleTrack

OFFSET_VALUE = 250

class VideoPlayer:
    """ Handles the Video Logic """
    def __init__(self,ui_instance,video_url):
        self.ui = ui_instance
        self.primary_subtitle = SubtitleTrack("Primary Subtitle",[])
        self.secondary_subtitle = SubtitleTrack("Secondary Subtitle",[])
        
        # Initialize Media Player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.positionChanged.connect(self.update_video_timeline)
        self.player.positionChanged.connect(self.update_subtitle)
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

        # --- Subtitle Offset ---
        self.ui.primary_plus_button.clicked.connect(
            lambda : self.update_offset_subtitle(
                self.primary_subtitle,
                self.ui.primary_offset_value_label,
                OFFSET_VALUE))
        self.ui.primary_minus_button.clicked.connect(
            lambda : self.update_offset_subtitle(
                self.primary_subtitle,
                self.ui.primary_offset_value_label,
                -OFFSET_VALUE))
        self.ui.secondary_plus_button.clicked.connect(
            lambda : self.update_offset_subtitle(
                self.secondary_subtitle,
                self.ui.secondary_offset_value_label,
                OFFSET_VALUE))
        self.ui.secondary_minus_button.clicked.connect(
            lambda : self.update_offset_subtitle(
                self.secondary_subtitle,
                self.ui.secondary_offset_value_label,
                -OFFSET_VALUE))

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
        """ Audio output value from 0.0 to 1.0 """ 
        volume_val = value / 100
        self.audio_output.setVolume(volume_val)
        
    def set_subtitle(self,data:list,track):
        """ Assign subtitle block """
        if data:
            # Primary 
            if track == 1:
                self.primary_subtitle.blocks = data

            # Secondary 
            if track == 2 :
                self.secondary_subtitle.blocks = data
            
        else:
            raise ValueError("Data list is empty:",data)

    def get_subtitle(self,value,subtitles,label,offset):
        """ Get the subtitle accordting to the timeline"""
        
        value += offset

        for sub in subtitles:
            if ( sub.start_ms + offset <= value <= sub.end_ms + offset ):
                html_list = "\n".join(sub.text)
                label.setText(html_list)
                return 

        label.clear()

    def update_subtitle(self,value):
        """ Updates the primary and secondary subtitle UI text based on the given value. """
        if self.primary_subtitle.blocks:
            self.get_subtitle(
                value,
                self.primary_subtitle.blocks,
                self.ui.primary_subtitle_text,
                self.primary_subtitle.offset_ms,
            )

        if self.secondary_subtitle.blocks:
            self.get_subtitle(
                value,
                self.secondary_subtitle,
                self.ui.secondary_subtitle_text,
                self.secondary_subtitle.offset_ms,
            )

    def update_offset_subtitle(self,subtitle,label,value):
        """ Update the offset value of the subtitle """

        subtitle.offset_ms += value
        label.setText(f"{subtitle.offset_ms / 1000:+.2f}s")
        self.update_subtitle(self.player.position())
        