import os
import sys
import magic
import subprocess
from tqdm import tqdm


def getArg(search, fallback=None):
    """Retrieve an argument. If the argument doesn't exist, return the
    fallback. If the fallback doesn't exist and the argument doesn't
    exist, exit the program since a required argument isn't passed.

    Args:
        search: a string that is being used to search if an argument exists
        fallback: a value that will be returned if the argument doesn't exist
    Returns:
        The value of the argument or the given fallback.
    """
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


# Command that will return the codec of a video file.
ffprobe = "ffprobe -v quiet -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "

# The directory where video files will be searched and transcoded.
DIR = getArg('path')

# Since we need a directory to search / trancode in,
# exit the program if it doesn't exist.
if (DIR == None):
    sys.exit('Path is required.')

mime = magic.Magic(mime=True)


def isVideo(file):
    """Check if the given file is a video or not.

    Args:
        file: a string of an absolute path where a file is stored
    Returns:
        A boolean
    """
    file_mime = mime.from_file(file)

    return "video" in file_mime


def getFileCount():
    """Count how many files there are within a directory.

    Returns:
        The amount of documents there are in a directory
    """
    count = 0

    for dirpath, _, filenames in os.walk(DIR):
        for f in filenames:
            count += 1

    return count


def getNonH264Files():
    """Get all video files whose codec is not h264.

    Returns:
        List of video files whose codec is not h264.
    """
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

# Command that will transcode the video file to a 'direct play' format.
transcode = 'ffmpeg -i "%s" -loglevel quiet -map 0:a -map 0:v -c:v libx264 -preset ultrafast -crf 23 -tune film -b:v 8M -maxrate:v 8M -bufsize:v 8M -c:a aac -ac 2 -ab 256K -threads %d "%s" -y'

print('Transcoding...')

total_nonh264 = len(non_h264)
i = 0

for path in non_h264:
    print('[Transcoding %d/%d] - %s' % (i, total_nonh264, path))

    i += 1

    splitted_path = path.split('/')
    input_dir = '/'.join(splitted_path[:-1])

    file_name = '.'.join(os.path.basename(path).split('.')[:-1])
    file_name = getArg('output', file_name)

    command = transcode % (path, int(getArg('threads', 1)), ('%s/%s.mp4' % (input_dir, file_name)))
    transcoding = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error = transcoding.communicate()

    if getArg('overwrite', False):
        os.remove(path.replace("'", "\'"))
