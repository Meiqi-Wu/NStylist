import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='./Dataset/videos')
args = parser.parse_args()

# Rename all videos to standard format - run only once!
count = 0
for root, dirs, filenames in os.walk(args.input_dir):
    for filename in filenames:
        print(filename)
        fullpath = os.path.join(root, filename)
        filename_zero, fileext = os.path.splitext(filename)

        newpath = os.path.join(root, "vid_{:02}".format(count) +fileext)
        os.rename(fullpath, newpath)
        count+=1