
import numpy as np
from multiprocessing import Process, Manager
import sys

from src.youtube.dload.dloaders import VideoDownloader

# for serialising the output
import pickle

import json


def collect_videos(global_list,
                   _vid_id_list,
                   _lang_code):
    for vid_id in _vid_id_list:
        # make a vid_url
        vid_url = "https://www.youtube.com/watch?v={}" \
            .format(vid_id)
        # the drivers will run separately here. mind the memory
        global_list.append(VideoDownloader.dl_video(vid_url=vid_url,
                                                    lang_code=_lang_code))


def multiprocess_dl_vids(_vid_id_list: list,
                         _lang_code: str,
                         _num_proc=4):

    # split the video id lists into n batches
    batches = np.array_split(np.asarray(_vid_id_list), _num_proc)
    # assign temp buckets for each batches
    # register processes
    with Manager() as manager:
        global_list = manager.list()
        processes = [Process(target=collect_videos, args=(global_list, batch, _lang_code))
                     for batch in batches]

        # start the processes
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        # get the objects
        results = [vid for vid in global_list]

    # return the final output
    return results


if __name__ == "__main__":
    # how do I pass objects to a python script?
    # just serialise it
    lang_code = sys.argv[1]
    num_proc = int(sys.argv[2])
    with open("src/main/in_json.json") as fh:
        vid_id_list = json.loads(fh.read())

    result = multiprocess_dl_vids(vid_id_list,
                                  lang_code,
                                  num_proc)
    # write the binary output to standard out
    with open("src/main/out.txt", 'wb') as fh:
        fh.write(pickle.dumps(result))
