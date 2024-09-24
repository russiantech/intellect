import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PycacheHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory and '__pycache__' in event.src_path:
            print(f"Deleting {event.src_path}")
            shutil.rmtree(event.src_path)

def monitor_pycache(root_dir='.'):
    event_handler = PycacheHandler()
    observer = Observer()
    observer.schedule(event_handler, path=root_dir, recursive=True)
    observer.start()

    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # monitor_pycache(root_dir='.')
    monitor_pycache(root_dir='../..')
