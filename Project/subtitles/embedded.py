from dataclasses import dataclass
import subprocess
import json

@dataclass
class EmbeddedSubtitleStream:
    index: int
    codec: str
    language: str | None = None
    title: str | None = None


class EmbeddedSubtitleDetector:

    def __init__(self,filePath):
        self.file_path = filePath 
    
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
            check=True
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
            
                
