import ffmpeg
import customtkinter
import tkinter as tk
import os
from GUI import App
from ffmpeg import FFmpeg, Progress
import VideoFileUtils
from VideoFileUtils import VideoFile

def GetStringFromTextTemplate(text_template: str, VideoObject: VideoFile) -> str:
    """Returns a complete String from a Text Template and the VideoObject
    
    Args:
        - text_template (str): The Text template provided
        - VideoObject (VideoFile): The Video Object
    
    Returns:
        - Complete String (str): The final, complete string"""

    complete_string = (
        text_template
        .replace("<TITLE>", VideoObject.title)
        .replace("<DATE>", str(VideoObject.file_creation_date))
        .replace("<FPS>", str(VideoObject.fps))
        .replace("<BITRATE>", str(VideoObject.bitrate))
        .replace("<CHANNELS>", str(VideoObject.channels))
        .replace("<LENGTH>", str(VideoObject.length))
    )

    return complete_string

def on_convert(new_name, filepaths, output_path, new_format): #converts the provided video to mp4 format
    
    num = 0 # TODO: replace with text template later

    Videos = []

    for filepath in filepaths:
        Videos.append(VideoFileUtils.VideoFile(filepath))

    filecount = len(Videos)
    for VideoObject in Videos:
        num = num + 1
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(VideoObject.filepath)
            .output(
                f"{output_path}\\{GetStringFromTextTemplate(new_name, VideoObject)}{new_format}",
                codec="copy"
            )
        )

        @ffmpeg.on("completed")
        def on_completion():
            app.home_frame_button_4.configure(text=f"Converted! {num}/{filecount}")
            if num == filecount:
                os.system(f'start {os.path.realpath(output_path)}')

        ffmpeg.execute()


if __name__ == "__main__":
    app = App(on_convert)
    app.mainloop()