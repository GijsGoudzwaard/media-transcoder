# Media transcoder

Transcode all video files within a directory to 'direct play'. This script will search for all video files within a directory and check its codec. If the codec is not h264, then it will be transcoded to h264.

This is especially usefull for a raspberry pi media server where all media from 1080p and up needs to be transcoded for direct play. This script does not copy any subtitles.

## Setup

Both python 2 and python 3 are supported.

```bash
pip install -r requirements.txt
```

## Usage

All available options are specified below. Of all these options, only `path` is **required**.

```text
usage: python index.py --path=PATH [--output=OUTPUT] [--override=False] [--threads=1]

Arguments
    --path (required)
        Location which will be searched for video's and transcoded if they are found.

    --output
        The name of the transcoded file. The file will be placed in the same
        directory as the original file. Also the file will be forced to .mp4.
        Default is the name of the original file.

    --overwrite
        Overwrite the original file with the newly transcoded file. Default is False.

    --threads
        How many CPU cores you'd like to use for transcoding. Default is 1.
```
