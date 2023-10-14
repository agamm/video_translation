import csv
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# Define your input file paths and language
MP4_FILE = "./video.mp4"
CSV_FILE = "./translations.csv"
LANGUAGE = "Russian"
SUB_POS = "bottom"
BOX_TOP = 0.15
BOX_BOT = 0.24
TEXT_SIZE = 20  # 16 = big, 20=small (higher = smaller)


def process_video(mp4_path, csv_path, language):
    subtitles = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            subtitles.append(row)

    video_clip = VideoFileClip(mp4_path)
    # Define the size of the letterbox

    def my_filter(frame):
        """Blacken a rectangular zone of the frame"""
        size_t = int(video_clip.h*BOX_TOP)
        size_b = int(video_clip.h*BOX_BOT)
        frame[:size_t, :] = 0
        frame[-size_b:, :] = 0
        return frame
    letterboxed = CompositeVideoClip([video_clip]).fl_image(my_filter)

    final_clip = add_subtitles_to_video(language, subtitles, letterboxed)

    output_filename = f'./output/{language}_video.mp4'
    final_clip.write_videofile(output_filename)

    video_clip.close()
    letterboxed.close()
    final_clip.close()
    print(f"Video with subtitles has been created: {output_filename}")


def parse_timestamp(timestamp):
    hours, minutes, seconds = map(int, timestamp.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def filter_csv_by_language(subtitles, language):
    result = []

    for row in subtitles:
        if len(result) < 2:
            result.append(row)
        else:
            if row[0].lower() == language.lower():
                result.append(row)

    return result


def add_subtitles_to_video(language, subtitles, video_clip):
    print("Creating", language)

    subtitles = filter_csv_by_language(subtitles, language)
    subtitle_clips = []
    for i in range(2, len(subtitles[1])):

        start_time = parse_timestamp(subtitles[1][i-1])
        end_time = video_clip.duration
        if i < len(subtitles[1]):
            end_time = parse_timestamp(subtitles[1][i])

        text = subtitles[2][i-1]

        text = add_newline_if_long(text)
        print(text)

        subtitle_clip = TextClip(
            text, fontsize=video_clip.h // TEXT_SIZE, color='white', bg_color='black', font="Helvetica")
        subtitle_clip = subtitle_clip.set_start(
            start_time).set_end(end_time)

        pos = 0.04
        if SUB_POS == 'bottom':
            pos = 0.88
        subtitle_clip = subtitle_clip.set_position(
            ("center", pos), relative=True)
        subtitle_clips.append(subtitle_clip)

    final_clip = CompositeVideoClip([video_clip] + subtitle_clips)

    return final_clip


def add_newline_if_long(text):
    if len(text) > 61:
        middle = len(text) // 2  # Find the middle of the text
        left_half = text[:middle]
        right_half = text[middle:]

        # Find the nearest space or comma character in the right half
        for i in range(middle, len(text)):
            if text[i] in (' ', ','):
                index = i
                break
        else:
            # If no space or comma found, use the middle point
            index = middle

        # Split the text at the found index and insert a newline
        left_half = text[:index]
        right_half = text[index:]
        text = left_half + "\n" + right_half.strip()

    return text


if __name__ == '__main__':
    process_video(MP4_FILE, CSV_FILE, LANGUAGE)
