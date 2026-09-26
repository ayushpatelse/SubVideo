from dataclasses import dataclass
import subprocess
from pathlib import Path
import json
import tempfile
from .parser import SubtitleBlock,SubtitleParser

@dataclass
class EmbeddedSubtitleStream:
    index: int
    codec: str
    language: str | None = None
    title: str | None = None

    def display_name(self):
        if self.language and self.title:
            return f"{self.language} — {self.title}"
        elif self.language:
            return self.language
        elif self.title:
            return self.title
        return "Unknown subtitle"

    
class EmbeddedSubtitleDetector:

    def __init__(self,file_path):
        self.file_path = file_path 
    
    def get_media_info(self) ->  list[EmbeddedSubtitleStream]:

    
        command = [
            "ffprobe",
            "-v" ,
            "error", 
            "-select_streams",
            "s", 
            "-show_streams" ,
            "-of" ,
            "json" ,
            self.file_path]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)
        streams_data = data["streams"]
        embedded_list = []
        
        for stream in streams_data :

            embedded_subtitle_info =  EmbeddedSubtitleStream(
                index=stream["index"],
                codec=stream["codec_name"],
                language=stream.get("tags",{}).get("language"),
                title=stream.get("tags",{}).get("title"),
            )
            embedded_list.append(embedded_subtitle_info)

        return embedded_list
            
                
class EmbeddedSubtitleExtracter:
    def __init__(self,video_url):
        self.video_url = video_url

    def extract(self,stream: EmbeddedSubtitleStream) -> list[SubtitleBlock]:

        if stream is None:
            return

        with tempfile.TemporaryDirectory() as temp_dir:

            output_path = Path(temp_dir) / f"subtitle_{stream.index}.srt"

            command = [
                "ffmpeg",
                "-i",
                self.video_url,
                "-map",
                f"0:{stream.index}",
                str(output_path)
            ]

            # Execute FFpeg
            subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,        
            )

            extracted_subtitles =  SubtitleParser(output_path).parse()

            return extracted_subtitles

            