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
from  PySide6.QtGui import QIcon
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QSize,Qt

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
        
        # Subtitles
        subtitle_layout = QHBoxLayout()
        self.subtitle_button = QPushButton("Select Subtitles")
        self.subtitle_button.setFixedWidth(90)
        self.subtitle_button.setStyleSheet("QPushButton { font-size :10px }")
        self.subtitle_button.clicked.connect(self.selection_subtitles)

        self.primary_subtitle_text = QLabel("Subtitles show here")
        self.primary_subtitle_text.setMaximumHeight(50)
        self.primary_subtitle_text.setStyleSheet("background-color: rbga(0,0,0,0); qproperty-alignment: AlignCenter;")

        self.secondary_subtitle_text = QLabel("Subtitles show here")
        self.secondary_subtitle_text.setMaximumHeight(50)
        self.secondary_subtitle_text.setStyleSheet("background-color: rbga(0,0,0,0) ; qproperty-alignment: AlignCenter;")

        subtitle_layout.addWidget(self.primary_subtitle_text)
        subtitle_layout.addWidget(self.secondary_subtitle_text)

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
            subtitle_block = subtitle_parser.parse()
            if self.video_player.player and subtitle_block != []:

                if not self.video_player.primary_subtitle_blocks  : 
                    self.video_player.set_subtitle(subtitle_block,track=PRIMARY_SUBTITLE)
                    print("! Primary Subtitle Set")
                else: 
                    self.video_player.set_subtitle(subtitle_block,track=SECONDARY_SUBTITLE)
                    print("! Secondary Subtitle Set")
                
            else:
                raise ValueError("Subtitle list is empty or media is not selected",subtitle_block)

            
        
        