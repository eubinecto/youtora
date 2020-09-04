# temporary module to avoid conflicts with feature 80
import subprocess
from typing import List

import numpy as np
# for encoding the image into data uri
import base64


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

    DATA_URL_FORM = 'data:image/png;base64,{}'

    @classmethod
    def dl_frame_bytes(cls, vid_url, timestamp) -> bytes:
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
        # get the raw byte image and terminate the process
        img_bytes = proc.communicate()[0]
        proc.terminate()
        return img_bytes

    @classmethod
    def _img_bytes_to_np(cls,
                         img_bytes: List[bytes],
                         height: int,
                         width: int) -> np.array:
        # decode the bytes to integers
        image = np.frombuffer(img_bytes, 'uint8')  # decode the bytes
        # reshape with the given resolution.
        image = image.reshape((height, width, 3))
        return image

    @classmethod
    def _img_bytes_to_data_url(cls,
                               img_bytes: List[bytes]):
        encoded = base64.b64encode(img_bytes).decode()
        return cls.DATA_URL_FORM.format(encoded)


