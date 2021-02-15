# from trackpy questions https://github.com/soft-matter/trackpy/issues/167
# VIDEO EXPORTING
import numpy as np
import pandas as pd
import trackpy as tp
import imageio
import glob
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cv2
import matplotlib.pyplot as plt
import os


def cvtFig2Numpy(fig):
    canvas = FigureCanvas(fig)
    canvas.draw()

    width, height = fig.get_size_inches() * fig.get_dpi()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(height.astype(np.uint32),
                                                                        width.astype(np.uint32), 3)
    return image


def makevideoFromArray(movieName, array, fps=30):
    imageio.mimwrite(movieName, array, fps=fps);


def make_video(vid_path, features_df, export_path, clip_frames=None, fps=30):
    plt.ion()
    imgs = glob.glob(vid_path)
    # frames = pims.open(vid_path)

    if clip_frames is None:
        first = features_df['frame'].unique().min()
        last = features_df['frame'].unique().max()
        clip_frames = [first, last]

    # imgs indexing always starts at 0, its not aware of the dataframe or the clipping.
    f_img_start = 0
    f_img_end = last - first
 
    arr = []
    f_start, f_end = clip_frames
    for fnum, img in zip(range(f_start, f_end), imgs[f_img_start:f_img_end]):
        print(f'Frame -> {fnum}')
        frame = cv2.imread(img)
        fig = plt.figure(figsize=(16, 10))
        plt.imshow(frame)
        axes = tp.plot_traj(features_df.query(f'frame<={fnum}'), label=True)
        axes.set_yticklabels([])
        axes.set_xticklabels([])
        axes.get_xaxis().set_ticks([])
        axes.get_yaxis().set_ticks([])
        arr.append(cvtFig2Numpy(fig))
        plt.close();

    makevideoFromArray(export_path, arr, fps)  # number of FPS at the end


if __name__ == '__main__':
    print(os.getcwd())
    feat_df = pd.read_csv('linked_results/201109_1023AM.csv')
    wheel_vid_names = ['D'] 
    for i in wheel_vid_names:
        feat_df = feat_df[feat_df['filename'] == i]
        vid_path = f'original_video/{i}/*.tif'
        make_video(vid_path=vid_path, features_df=feat_df, export_path=f'linked_video/{i}.mp4')