import os
import random
from torch.utils.data import Sampler


class VideoSampler(Sampler):
    """
    Dataset shuffle does not work for Custom Sampler. We need to implement the shuffle logic inside
    the sampler.
    """
    def __init__(self, data, replacement=False):
        """
        :data: VideoDataset
        """

        self.video_frame = []
        self.replacement = replacement

        # This logic can be improvised and made more efficient.
        dirs = [x[1] for x in os.walk(data.img_dir+'frames/')][0]
        dirs = sorted(dirs)
        

        i=0
        for dir in dirs:
            absolute_path = data.img_dir + 'frames/' + dir

            count = len([name for name in os.listdir(absolute_path) if os.path.isfile(os.path.join(absolute_path, name))])
            # print(dir,count)
            self.video_frame.extend([(i, j) for j in range(count-1)])
            i += 1
        
        # print(self.video_frame)
        
        
    def __iter__(self):
        if self.replacement:
            random.shuffle(self.video_frame)
 #      print(self.video_frame)
        return iter(self.video_frame)