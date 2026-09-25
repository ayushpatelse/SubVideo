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
        

        # Subtitle Offset Logic
        # Primary Offset
        self.primary_subtitle_name = QLabel("No Subtitle")
        self.primary_subtitle_name.setStyleSheet("QLabel {font-size : 10px; max-height : 15px}")
        primary_offset_layout = QHBoxLayout()
        self.primary_offset_value_label = QLabel("0s")
        self.primary_offset_value_label.setFixedWidth(50)
        self.primary_offset_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.primary_subtitle_change = QPushButton("Change / Load")
        self.primary_subtitle_change.setStyleSheet("QPushButton {font-size : 10px; max-height : 15px}")
        self.primary_subtitle_change.clicked.connect(
            lambda: self.selection_subtitles(PRIMARY_SUBTITLE))
        self.primary_subtitle_remove = QPushButton("Remove")
        self.primary_subtitle_remove.setStyleSheet("QPushButton {font-size : 10px; max-height : 15px}")
        self.primary_minus_button = QPushButton("-") 
        self.primary_minus_button.setFixedWidth(50) 
        self.primary_plus_button = QPushButton("+")
        self.primary_plus_button.setFixedWidth(50) 
        primary_function = QHBoxLayout()

        primary_function.addWidget(self.primary_subtitle_name,alignment=Qt.AlignmentFlag.AlignLeft)
        primary_function.addWidget(self.primary_subtitle_change,alignment=Qt.AlignmentFlag.AlignRight)
        primary_function.addWidget(self.primary_subtitle_remove,alignment=Qt.AlignmentFlag.AlignRight)
        primary_offset_layout.addWidget(self.primary_minus_button)
        primary_offset_layout.addWidget(self.primary_offset_value_label)
        primary_offset_layout.addWidget(self.primary_plus_button)

        # Primary Offset
        self.secondary_subtitle_name = QLabel("No Subtitle")
        self.secondary_subtitle_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.secondary_subtitle_name.setStyleSheet("QLabel {font-size : 10px; max-height : 15px}")
        secondary_offset_layout = QHBoxLayout()
        self.secondary_offset_value_label = QLabel("0s")
        self.secondary_offset_value_label.setFixedWidth(50)
        self.secondary_offset_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.secondary_subtitle_change = QPushButton("Change / Load")
        self.secondary_subtitle_change.setStyleSheet("QPushButton {font-size : 10px; max-height : 15px}")
        self.secondary_subtitle_change.clicked.connect(
            lambda: self.selection_subtitles(SECONDARY_SUBTITLE))
        self.secondary_subtitle_remove = QPushButton("Remove")
        self.secondary_subtitle_remove.setStyleSheet("QPushButton {font-size : 10px; max-height : 15px}")
        self.secondary_minus_button = QPushButton("-") 
        self.secondary_minus_button.setFixedWidth(50) 
        self.secondary_plus_button = QPushButton("+")
        self.secondary_plus_button.setFixedWidth(50) 
        secondary_function = QHBoxLayout()

        secondary_function.addWidget(self.secondary_subtitle_name,alignment=Qt.AlignmentFlag.AlignLeft)
        secondary_function.addWidget(self.secondary_subtitle_change,alignment=Qt.AlignmentFlag.AlignRight)
        secondary_function.addWidget(self.secondary_subtitle_remove,alignment=Qt.AlignmentFlag.AlignRight)
        secondary_offset_layout.addWidget(self.secondary_minus_button)
        secondary_offset_layout.addWidget(self.secondary_offset_value_label)
        secondary_offset_layout.addWidget(self.secondary_plus_button)

        self.primary_subtitle_text = QLabel("")
        self.primary_subtitle_text.setMaximumHeight(50)
        self.primary_subtitle_text.setStyleSheet("background-color: rbga(0,0,0,0); qproperty-alignment: AlignCenter;")

        self.secondary_subtitle_text = QLabel("")
        self.secondary_subtitle_text.setMaximumHeight(50)
        self.secondary_subtitle_text.setStyleSheet("background-color: rbga(0,0,0,0) ; qproperty-alignment: AlignCenter;")

        primary_subtitle_box.addLayout(primary_function)
        primary_subtitle_box.addWidget(self.primary_subtitle_text)
        primary_subtitle_box.addLayout(primary_offset_layout)

        secondary_subtitle_box.addLayout(secondary_function)
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
    def selection_subtitles(self,s_track):
        subtitleFile, _ = QFileDialog.getOpenFileName(
            None,
            self.tr("Open File"),
            "C:/Users/ayush/Desktop/Python/DualSub/Project/Extra/samples",
            self.tr("Subtitles Files ( *.srt )")
) 

        if subtitleFile :
            subtitle_parser =  SubtitleParser(subtitleFile)
            file_name = os.path.basename(subtitleFile)
            try :
                subtitle_block = subtitle_parser.parse()
            except ValueError as error: 
                print(f"Could not load subtitle: {error}")
                return

            if self.video_player.player and subtitle_block != []:
                self.video_player.set_subtitle(data=subtitle_block,fileName=file_name,track=s_track)
            else:
                raise ValueError("Subtitle list is empty or media is not selected",subtitle_block)

            
        
        