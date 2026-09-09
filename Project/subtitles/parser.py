import re
from datetime import datetime 
from dataclasses import dataclass

# Subtitle Block Dataclass
@dataclass
class SubtitleBlock:
    index : int
    start_ms : int
    end_ms : int
    text : list[str]


class SubtitleParser:
    def __init__(self,filePath):
        self.file_path = filePath
        
            
    def parse(self):
        """ Parsing the .SRT file into SubtitleBlock """     

        with open(self.file_path,"r") as file:
            blocks = []
            block_text = []

            for line in file:

                if line.strip() =="" :
                    if block_text  : 
                        blocks.append(self.parse_block(block_text))

                    block_text = []
                    continue

                block_text.append(line.strip())           

            # Edge Case : Handling the last subtitle 
            if block_text:
                blocks.append(self.parse_block(block_text))

            return blocks
        

    def timestamp_start_end_ms(self,timeStamp:str):
        """ Extracting Start & End Timestamp  """

        if "-->" in timeStamp:

            start_timestamp,end_timestamp = timeStamp.split('-->')

            start_timestamp = datetime.strptime(start_timestamp.strip(),"%H:%M:%S,%f").time()
            end_timestamp = datetime.strptime(end_timestamp.strip(),"%H:%M:%S,%f").time()
            
            start_ms =  self.timestamp_in_milliseconds(start_timestamp)
            end_ms =  self.timestamp_in_milliseconds(end_timestamp)

            if start_ms > end_ms:
                raise ValueError( f"start_ms{start_ms} is greater than end_ms{end_ms}")

            return (start_ms,end_ms)
        else:
            raise ValueError("<-- Timestamp invalid format -->")

    def timestamp_in_milliseconds(self,value):
        """ Converting value into milliseconds """
        return (value.hour * 3600000) + (value.minute * 60000) + (value.second * 1000) + (value.microsecond // 1000)

    def parse_block(self,data:list[str]):
        """Convert a raw SRT subtitle block into a SubtitleBlock."""

        if len(data) < 3 :
            raise ValueError("Subtitle block is missing index, timestamp, or text") 
        
        time_stamps =  self.timestamp_start_end_ms(data[1])
        
        # Creating Dataclass 
        return SubtitleBlock(
            index = int(re.search(r'\d+',data[0]).group()),
            text = data[2:],
            start_ms =  time_stamps[0],
            end_ms = time_stamps[1]
        )
        