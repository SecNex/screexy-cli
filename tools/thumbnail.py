import os
import cv2

from rich.console import Console

console = Console()

class Thumbnail:
    def __init__(self, video_path: str, media_path: str, timestamp_seconds: int = 1) -> None:
        self.video_path = video_path
        self.media_path = media_path
        self.timestamp_seconds = timestamp_seconds
        self.videos = self.list()
        self.__check()

    def __check(self) -> None:
        if not os.path.exists(self.media_path):
            os.makedirs(self.media_path)
        
    def list(self) -> list:
        if not os.path.exists(self.video_path):
            return []
        list_files = [f"{self.video_path}/{video}" for video in os.listdir(self.video_path) if video.endswith('.mp4')]
        list_files_full = []
        for file in list_files:
            item = {
                "path": file,
                "name": file.split("/")[-1]
            }
            list_files_full.append(item)
        return list_files_full
    
    def generate(self) -> list:
        for v in self.videos:
            try:
                console.print(f"🛠️ Generating thumbnail for {v['name']} in {self.media_path}...")
                cap = cv2.VideoCapture(v["path"])
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_number = int(fps * self.timestamp_seconds)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                __target = f"{self.media_path}/{v['name'].replace('.mp4', '.jpg')}"
                if ret:
                    cv2.imwrite(__target, frame)
                else:
                    print(f"Could not generate thumbnail for {v}")

                cap.release()
                console.print(f"✅ Thumbnail generated for {v['name']} as {__target}.", style="bold")
                print()
            except Exception as e:
                print(f"Could not generate thumbnail for {v}: {e}")
