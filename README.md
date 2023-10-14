### Install

`pip install moviepy`
`pip install moviepy[optional]`

- Make sure to have imagemagic installed

### Usage

1. Create a Google sheet with translations and timestamps like so:

```
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Timestamps,0:00:00,0:00:04,0:00:09
Hebrew,שלום, עולם
English,Hello, World
```

2. Edit the code:

```
MP4_FILE = "./video.mp4"
CSV_FILE = "./translations.csv"
LANGUAGE = "Russian" # What language you want to add to the subtitles
SUB_POS = "bottom" # Subtitle position bottom/top
BOX_TOP = 0.15 # letterboxing top
BOX_BOT = 0.24 # letterboxing bottom
TEXT_SIZE = 20  # 16 = big, 20=small (higher = smaller)
```

3. Run: `python main.py`
