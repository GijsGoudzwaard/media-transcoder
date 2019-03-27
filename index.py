import os
import sys
import magic
import subprocess
from tqdm import tqdm

def getArg(search, fallback = None):
    args = sys.argv[1:]
    found_arg = False

    for arg in args:
        arg = arg.replace('--', '')

        arg, value = arg.split('=')

        if arg == search:
            found_arg = value
            break

    if not found_arg and fallback is not None:
        return fallback
    elif not found_arg and fallback is None:
        sys.exit('\'%s\' is required' % search)

    return found_arg

ffprobe = "ffprobe -v quiet -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "

DIR = getArg('path')

if (DIR == None):
    sys.exit('Path is required.')

mime = magic.Magic(mime=True)

def isVideo(file):
  file_mime = mime.from_file(file)

  return "video" in file_mime

def getFileCount():
  count = 0
  for dirpath, _, filenames in os.walk(DIR):
    for f in filenames:
      count += 1

  return count

def getNonH264Files():
  file_count = getFileCount()

  non_h264 = []

  with tqdm(total=file_count, unit=' Files', unit_scale=True, unit_divisor=1024) as pbar:
    for dirpath, _, filenames in os.walk(DIR):
      for f in filenames:
        path = os.path.abspath(os.path.join(dirpath, f))

        pbar.update(1)

        if isVideo(path):
          process = subprocess.Popen('%s "%s"' % (ffprobe, path), shell=True, stdout=subprocess.PIPE)
          output, error = process.communicate()

          if not 'h264' in output.decode("utf-8"):
            non_h264.append(path)

  return non_h264

print("Fetching to be transcoded files, this could take a while depending on how large your library is...")
non_h264 = getNonH264Files()

print("Non h264 files: %d" % len(non_h264))

# print(getFileCount())

# transcode = 'ffmpeg -i \'%s\' -map 0:a -map 0:s -map 0:v -c:v libx264 -preset ultrafast -crf 23 -tune film -b:v 8M -maxrate:v 8M -bufsize:v 8M -c:a aac -ac 2 -ab 256K -c:s mov_text -threads 4 %s -y'

# print('Transcoding...')

# for path in non_h264:
#     print('[Transcoding] - %s' % path)

# transcoding = subprocess.Popen(transcode % ('input.mkv', 'output.mp4'), shell=True, stdout=subprocess.PIPE)
