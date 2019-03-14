import os
import magic
import subprocess

ffprobe = "ffprobe -v quiet -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "

mime = magic.Magic(mime=True)

def isVideo(file):
    file_mime = mime.from_file(file)

    return "video" in file_mime

def getNonH264Files():
    non_h264 = []

    for dirpath,_,filenames in os.walk("./../../Thor/Media"):
        for f in filenames:
            path = os.path.abspath(os.path.join(dirpath, f))

            if isVideo(path):
                process = subprocess.Popen('%s "%s"' % (ffprobe, path), shell=True, stdout=subprocess.PIPE)
                output, error = process.communicate()

                if not 'h264' in output.decode("utf-8"):
                    non_h264.append(path)

    return non_h264

non_h264 = getNonH264Files()

for path in non_h264:
    print(path)


print('Non h264 files: %d' % len(non_h264))

