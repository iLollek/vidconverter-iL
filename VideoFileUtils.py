from moviepy.editor import VideoFileClip
import os
import datetime
import subprocess


class VideoFile():

    def __init__(self, path: str):
        self.filename = os.path.basename(path)
        self.filepath = os.path.abspath(path)
        self.format = self._get_video_format()
        self.length = self._get_length()
        self.width = self._get_width()
        self.height = self._get_height()
        self.fps = self._get_fps()
        self.bitrate = self._get_bitrate()
        self.channels = self._get_audio_channels()
        self.datarate = self._get_data_rate()
        self.title = self._get_title()
        # self.recorded_date = self._get_recorded_date() # Not possible at the moment.
        self.file_creation_date = self._get_file_creation_date()
        self.file_last_changed_date = self._get_file_last_changed_date()

    def _get_video_format(self):
        _, file_extension = os.path.splitext(self.filepath)
        video_format = file_extension.strip('.')
        return video_format
    
    def _get_length(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)

    def _get_width(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                                "-of", "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return int(result.stdout)

    def _get_height(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height",
                                "-of", "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return int(result.stdout)

    def _get_fps(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                                "-of", "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        fps_str = result.stdout.decode("utf-8").strip()
        num, denom = map(int, fps_str.split("/"))
        return num / denom

    def _get_bitrate(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate",
                                "-of", "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        output = result.stdout.strip()
        if output == b'N/A':
            return None  # or any default value you prefer
        else:
            return int(output)

    def _get_audio_channels(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels",
                                "-of", "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return int(result.stdout)

    def _get_data_rate(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=bit_rate",
                                "-of", "default=noprint_wrappers=1:nokey=1", self.filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return int(result.stdout)

    def _get_title(self):
        # Split the filename into base name and extension
        base_name, _ = os.path.splitext(self.filename)
        # Return only the base name
        return base_name

    def _get_file_creation_date(self):
        creation_time = os.path.getctime(self.filepath)
        return datetime.datetime.fromtimestamp(creation_time).strftime('%d.%m.%y')

    def _get_file_last_changed_date(self):
        last_changed_time = os.path.getmtime(self.filepath)
        return datetime.datetime.fromtimestamp(last_changed_time).strftime('%d.%m.%y')
    
if __name__ == "__main__":
    # Unit-Testing VideoFileUtils
    VF = VideoFile(r"C:\Users\loris\Desktop\Coding\vidconverter\M2U00965.mpeg")

    print(VF.filepath)
    print(VF.format)
    print(VF.length)
    print(VF.bitrate)
    print(VF.fps)