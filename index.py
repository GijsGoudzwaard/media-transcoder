import os
import subprocess

ffprobe = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "

def getNonH264Paths():
	non_h264 = []

	for dirpath,_,filenames in os.walk("./../Media"):
		for f in filenames:
			path = os.path.abspath(os.path.join(dirpath, f)).replace(' ', '\ ')

			process = subprocess.Popen(ffprobe + path, shell=True, stdout=subprocess.PIPE)
			output, error = process.communicate()

			if not 'h264' in output.decode("utf-8"):
				non_h264.append(path)

	return non_h264

# getNonH264Paths()

for path in getNonH264Paths():
	print(path)
