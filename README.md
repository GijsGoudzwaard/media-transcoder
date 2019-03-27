## Setup

Both python 2 and python 3 are supported.

```
pip install -r requirements.txt
```

## Transcoding

```
python index.py --path=./../Media
```

## Options

All available options are specified below. Of all these options, only `path` is **required**.

```
python index.py
    --path (required)
        Location which will be searched for video's and transcoded if they are found.

    --threads
        How many CPU cores you'd like to use for transcoding. Default is 1.
```
