
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
from player.video_player import VideoPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QSize,Qt


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

        # Timeline
        timeline_layout = QHBoxLayout()
        self.video_timeline = QSlider(Qt.Horizontal)
        self.v_timeline_lablel = QLabel("00:00 / 00:00")
        timeline_layout.addWidget(self.v_timeline_lablel)
        timeline_layout.addWidget(self.video_timeline)
        main_layout.addLayout(timeline_layout)

        # Horizontal layout
        control_layout = QHBoxLayout()

        # --- Control Buttons ---
        # Open Button select file
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.video_selection)


        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")

        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)

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
            print("File Path: %s" %fileName)
            self.video_player = VideoPlayer(self,video_url=fileName)
            self.video_player.player.play()

        else:
            print("No Path selected")
        

        

        

        