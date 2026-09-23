# Import Library functions,classes ,etc
from PySide6.QtWidgets import  (
    QMainWindow,
    QWidget,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFileDialog
)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt
import os
# Import Custom class,function, etc
from player.video_player import VideoPlayer
from subtitles.parser import SubtitleParser

INITIAL_VOLUME = 70
PRIMARY_SUBTITLE = 1
SECONDARY_SUBTITLE = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # App Name
        self.setWindowTitle("DualSub")
        self.resize(800,600)    # Window Size

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

    
        # Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Video Placeholder
        self.video_area = QVideoWidget()
        main_layout.addWidget(self.video_area)

        # Video Timeline
        timeline_layout = QHBoxLayout()
        self.video_timeline = QSlider(Qt.Horizontal)
        self.v_timeline_lablel = QLabel("00:00 / 00:00")
        timeline_layout.addWidget(self.v_timeline_lablel)
        timeline_layout.addWidget(self.video_timeline)
        main_layout.addLayout(timeline_layout)

        # Volume Slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0,100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setValue(70)
        
        # --- Subtitle ---
        subtitle_layout = QHBoxLayout()
        primary_subtitle_box = QVBoxLayout()
        secondary_subtitle_box = QVBoxLayout()
        self.subtitle_button = QPushButton("Select Subtitles")
        self.subtitle_button.setFixedWidth(90)
        self.subtitle_button.setStyleSheet("QPushButton { font-size :10px }")
        self.subtitle_button.clicked.connect(self.selection_subtitles)

        # Subtitle Offset Logic
        # Primary Offset
        self.primary_subtitle_name = QLabel("pn")
        self.primary_subtitle_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.primary_subtitle_name.setStyleSheet("QLabel {font-size : 10px; max-height : 15px}")
        primary_offset_layout = QHBoxLayout()
        self.primary_offset_value_label = QLabel("0s")
        self.primary_offset_value_label.setFixedWidth(50)
        self.primary_offset_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.primary_minus_button = QPushButton("-") 
        self.primary_minus_button.setFixedWidth(50) 
        self.primary_plus_button = QPushButton("+")
        self.primary_plus_button.setFixedWidth(50) 

        primary_offset_layout.addWidget(self.primary_minus_button)
        primary_offset_layout.addWidget(self.primary_offset_value_label)
        primary_offset_layout.addWidget(self.primary_plus_button)

        # Primary Offset
        self.secondary_subtitle_name = QLabel("pn")
        self.secondary_subtitle_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.secondary_subtitle_name.setStyleSheet("QLabel {font-size : 10px; max-height : 15px}")
        secondary_offset_layout = QHBoxLayout()
        self.secondary_offset_value_label = QLabel("0s")
        self.secondary_offset_value_label.setFixedWidth(50)
        self.secondary_offset_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.secondary_minus_button = QPushButton("-") 
        self.secondary_minus_button.setFixedWidth(50) 
        self.secondary_plus_button = QPushButton("+")
        self.secondary_plus_button.setFixedWidth(50) 

        secondary_offset_layout.addWidget(self.secondary_minus_button)
        secondary_offset_layout.addWidget(self.secondary_offset_value_label)
        secondary_offset_layout.addWidget(self.secondary_plus_button)

        self.primary_subtitle_text = QLabel("Subtitles show here")
        self.primary_subtitle_text.setMaximumHeight(50)
        self.primary_subtitle_text.setStyleSheet("background-color: rbga(0,0,0,0); qproperty-alignment: AlignCenter;")

        self.secondary_subtitle_text = QLabel("Subtitles show here")
        self.secondary_subtitle_text.setMaximumHeight(50)
        self.secondary_subtitle_text.setStyleSheet("background-color: rbga(0,0,0,0) ; qproperty-alignment: AlignCenter;")

        primary_subtitle_box.addWidget(self.primary_subtitle_name)
        primary_subtitle_box.addWidget(self.primary_subtitle_text)
        primary_subtitle_box.addLayout(primary_offset_layout)

        secondary_subtitle_box.addWidget(self.secondary_subtitle_name)
        secondary_subtitle_box.addWidget(self.secondary_subtitle_text)
        secondary_subtitle_box.addLayout(secondary_offset_layout)

        subtitle_layout.addLayout(primary_subtitle_box)
        subtitle_layout.addLayout(secondary_subtitle_box)

        # Horizontal layout
        control_layout = QHBoxLayout()

        # --- Control Buttons ---
        # Open Button select file
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.video_selection)


        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")

        # Adding Control Wigdets
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.subtitle_button)
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        
        main_layout.addLayout(subtitle_layout)
        main_layout.addLayout(control_layout)


    # Video File Selection 
    def video_selection(self):
        
        fileName, _ = QFileDialog.getOpenFileName(
            None,
            self.tr("Open File"),
            "C:/Users/ayush/Desktop/Python/DualSub/Project/Extra",
            self.tr("Video (*.mp4 *.mkv )")
        )
        
        if fileName:
            self.video_player = VideoPlayer(self,video_url=fileName)
            self.video_player.player.play()

        else:
            raise ValueError("No Path selected or found")

    # Subtitle selection
    def selection_subtitles(self):
        subtitleFile, _ = QFileDialog.getOpenFileName(
            None,
            self.tr("Open File"),
            "C:/Users/ayush/Desktop/Python/DualSub/Project/Extra/samples",
            self.tr("Subtitles Files ( *.srt )")
        ) 

        if subtitleFile :
            subtitle_parser =  SubtitleParser(subtitleFile)
            file_name = os.path.basename(subtitleFile)
            subtitle_block = subtitle_parser.parse()
            print(file_name)
            if self.video_player.player and subtitle_block != []:

                if not self.video_player.primary_subtitle.blocks  : 
                    self.video_player.set_subtitle(data=subtitle_block,fileName=file_name,track=PRIMARY_SUBTITLE)
                    print("! Primary Subtitle Set")
                else: 
                    self.video_player.set_subtitle(data=subtitle_block,fileName=file_name,track=SECONDARY_SUBTITLE)
                    print("! Secondary Subtitle Set")
                
            else:
                raise ValueError("Subtitle list is empty or media is not selected",subtitle_block)

            
        
        