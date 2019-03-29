# Media transcoder

Transcode all video files within a directory for 'direct play'. This script will search for all video files within a directory and check its codec. If the codec is not h264, then it will be transcoded to h264.

This is especially useful for a raspberry pi media server, where all media from 1080p and up needs to be transcoded in order to be watched properly. This script does not copy any subtitles.

## Setup

This script relies heavily on `ffmpeg` and `ffprobe`. Make sure that you have this installed, if not run

```bash
sudo apt install ffmpeg
```

Both python 2 and python 3 are supported.

```bash
pip install -r requirements.txt
```

## Usage

All available options are specified below. Of all these options, only `path` is **required**.

```text
usage: python index.py --path=PATH [--override=False] [--threads=1]

Arguments
    --path (required)
        Location which will be searched for video's and transcoded if they are found.

    --overwrite
        Overwrite the original file with the newly transcoded file. Default is False.

    --threads
        How many CPU cores you'd like to use for transcoding. Default is 1.
```
