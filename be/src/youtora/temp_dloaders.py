# temporary module to avoid conflicts with feature 80
import subprocess
import numpy as np


class FrameDownloader:
    # the format code used by youtube dl
    # https://askubuntu.com/questions/486297/how-to-select-video-quality-from-youtube-dl
    # we are using 240p resolution
    # as for just text detection, this will suffice
    SETTINGS_DICT = {
        'format_code': '135',  # 480P
        'frame_res': (480, 854)  # height , width\
    }
    # on mac & linux
    FFMPEG_BIN = "ffmpeg"

    @classmethod
    def dl_frame_binary(cls, vid_url, timestamp) -> np.array:
        """
        :param vid_url: the video from which to download the frames
        :param timestamp: the timestamp at which to capture the frame
        :return: a numpy array of the image
        """
        # credit: http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
        cmd = "ffmpeg -ss '{timestamp}'" \
              " -i $(youtube-dl -f {format_code} --get-url '{vid_url}')" \
              " -f image2pipe" \
              " -pix_fmt rgb24" \
              " -vframes 1" \
              " -q:v 2" \
              " -vcodec rawvideo" \
              " -" \
            .format(timestamp=timestamp, format_code=cls.SETTINGS_DICT['format_code'], vid_url=vid_url)

        # build the subprocess
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=10**8  # should be bigger than the size of the frame
        )
        frame_res: tuple = cls.SETTINGS_DICT['frame_res']
        # get the raw byte image and terminate the process
        raw_image = proc.communicate()[0]
        proc.terminate()
        # decode the bytes to integers
        image = np.frombuffer(raw_image, 'uint8')  # decode the bytes
        # reshape with the given resolution.
        image = image.reshape((frame_res[0], frame_res[1], 3))
        return image
