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
        'frame_format': 'jpeg'
    }

    @classmethod
    def dl_frame_jpeg(cls,
                      vid_url,
                      timestamp,
                      out_path) -> None:
        """
        :param out_path:
        :param vid_url: the video from which to download the frames
        :param timestamp: the timestamp at which to capture the frame
        """
        # credit: http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
        cmd = "ffmpeg -ss '{timestamp}'" \
              " -i $(youtube-dl -f {format_code} --get-url '{vid_url}')" \
              " -vframes 1" \
              " -q:v 2" \
              " {out_path}" \
            .format(timestamp=timestamp,
                    format_code=cls.SETTINGS_DICT['format_code'],
                    vid_url=vid_url,
                    out_path=out_path)

        # build the subprocess
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=10**8  # should be bigger than the size of the frame
        )
        proc.communicate()

