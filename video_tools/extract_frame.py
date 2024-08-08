import os
import subprocess
import shlex
from pathlib import Path
import ffmpeg

def ffmpeg_extract(fpath, outpath):
    try:
        (ffmpeg.input(fpath)
              .filter('fps', fps=1)
              .output(str(outpath) + '/' + str(fpath.stem) + '_%d.png', 
                      video_bitrate='5000k',
#                      s='64x64',
                      sws_flags='bilinear',
                      start_number=0)
              .run(capture_stdout=True, capture_stderr=True))
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))

inpath = Path("0")
outpath = Path("frames_0")

for fpath in inpath.glob("*.mp4"):
    print(fpath)
    ffmpeg_extract(fpath, outpath)
    
