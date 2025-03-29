import os
import subprocess

from utils.formats import SUPPORTED_AUDIO_FORMATS
from utils.security.vul_mitigate import SecurePython


def convert_m4a_(obj_file, _out_f: str):
    try:
        out_obj = obj_file.replace(obj_file.split(".")[-1], _out_f)
        if obj_file[-3:].lower() == "m4a":
            command = [
                "ffmpeg",
                "-i",
                f"{obj_file}",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "320k",
                f"{out_obj}",
            ]
        elif _out_f == "m4a":
            command = [
                "ffmpeg",
                "-i",
                f"{obj_file}",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                f"{out_obj}",
            ]
        subprocess.run(command, check=True, text=True)
        return out_obj
    except Exception as e:
        print(f"\033[91m{e}\033[0m")


def m4a(obj, _out_f: str):
    try:
        secure = SecurePython()
        if os.path.isdir(obj):
            print("Detected directory input")
            for root, dirs, files in os.walk(obj):
                for file in files:
                    if file.endswith(list(SUPPORTED_AUDIO_FORMATS)):
                        print(f"\033[1;96m{file}\033[0m")
                        fpath = secure.safe_filepath(root, file)
                        convert_m4a_(fpath, _out_f)
        elif os.path.isfile(obj):
            convert_m4a_(obj, _out_f)
    except Exception as e:
        print(f"\033[91m{e}\033[0m")
    finally:
        print("\033[1;92mDone")


if __name__ == "__main__":
    m4a(obj=input("\033[1;95mEnter directory/folder or file to operate on:\033[93m"))
