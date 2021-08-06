# Given a folder directory, link and filter all data exported from ImageJ.
import pandas as pd 
import trackpy as tp 
import matplotlib.pyplot as plt 
import numpy as np
from glob import glob
import datetime


def link(path, FPS, MPP, SEARCH_RANGE_MICRONS, MEMORY, STUBS, MIN_VELOCITY, MIN_AREA, MAX_AREA):
    """
    Given the path of a csv file output from ImageJ particle analysis, link, filter, and label the trajectories.

    Outputs a dataframe for the csv file analyzed.
    """
    df = pd.read_csv(path)

    # Pull info from filename
    filename = path.split('\\')[-1].rstrip('.csv')
    print(f'Processing {path}')

    # Get the frame information from the imagejdata
    df = label2frame(df)

    df.drop(labels=['Label', ' '], inplace=True, axis=1)
    df.rename({'X': 'x', 'Y': 'y'}, axis=1, inplace=True)

    # Actual Linking
    search_range = round(SEARCH_RANGE_MICRONS / MPP / FPS)  # number of pixels away to look for the blob in each frame
    print(f'Search range --> {search_range} pixels.')
    tp.quiet()  # supress output, makes linking quicker
    t = tp.link_df(df, search_range=search_range, memory=MEMORY)
    t1 = tp.filter_stubs(t, STUBS)
    print('Before filtering:', t['particle'].nunique())
    print('After filtering:', t1['particle'].nunique())

    # Calculate velocities.
    df_vel = calc_velocity(t1)
    df_vel.index.name = None
    t1.index.name = None
    t2 = t1.merge(df_vel, on=['particle', 'frame', 'x', 'y'], how='left')

    # Calculate useful quantities
    t2['time'] = t2['frame'] / FPS
    t2['dv'] = np.sqrt(t2['dx'] ** 2 + t2['dy'] ** 2)  # total velocity in pix/frame
    t2['dv_m'] = t2['dv'] * FPS * MPP  # total velocity in microns/s
    t2['Area_m'] = t2['Area'] * MPP ** 2  # area in microns^2
    t2['dx_m'] = t2['dx'] * FPS * MPP  # x velocity in microns/s, defined as the left/right movement.

    # Keep wheels larger than MIN_AREA
    bp = t2.groupby('particle').mean()['Area_m'] > MIN_AREA  # bp = big_particles
    bp = bp[bp].index.values
    t2 = t2[t2['particle'].isin(bp)]

    # Eliminate wheels smaller than MAX_AREA
    hp = t2.groupby('particle').max()['Area_m'] > MAX_AREA   # hp = huge particles
    hp = hp[hp].index.values
    t2 = t2[~t2['particle'].isin(hp)]  # The (~) operator negates the conditional, i.e. takes everything except the huge particles

    # Eliminate wheels whose means are slower than MIN_VELOCITY
    # fp = t2.groupby('particle').mean()['dx_m'] > MIN_VELOCITY  # fp = fast_particles
    # fp = fp[fp].index.values
    # t2 = t2[t2['particle'].isin(fp)]

    t2['filename'] = filename

    # Make a unique particle column, to prevent interference between videos.
    t2['particle_u'] = t2['filename'] + '-' + t2['particle'].astype(str)

    return t2


def label2frame(df):
    """
    Take the `Label` column in the data from ImageJ and convert it to a `frame` column. This varies according to the recording method and microscope used.

    This accounts for a few microscopes used in the Marr Lab, but you will most likely need to add an if statement to account for your `Label` column.
    """
    labels = df['Label']  # the column of labels
    label = labels.values[0]  # just the first row of the Label column

    print(f'Your label looks like -> {label}')

    # 1:slice:23 format
    if "slice" in labels.values[0]:
        df['Label'] = labels.astype('str')
        df['Label'] = df['Label'].str.split(':').str[2]
        df['frame'] = df['Label'].astype('int')

    # already in correct int format
    elif type(label) != str:
        df['frame'] = labels

    # ImageJ already has time data, convert back to frames
    elif df['Label'].values[0].split(' ')[-1] == 's':
        df['imagejtime'] = labels.str.split(' ').str[-2].str.split(':').str[-1].astype(float)
        df['approx_frame'] = df['imagejtime'] * FPS
        df['frame'] = df['approx_frame'].round().astype(int)

    else:  # Logan
        df['frame'] = labels.str.split('_').str[2].str.lstrip('0').str.rstrip('.tif')
        df['frame'] = pd.to_numeric(df['frame'])

    return df


def calc_velocity(df):
    """
    Take in linked trackpy dataframe and output velocity for each particle.
    Source = http://soft-matter.github.io/trackpy/dev/tutorial/custom-feature-detection.html
    """
    # Creating an empty dataframe to store results
    col_names = ['dx', 'dy', 'x', 'y', 'frame', 'particle']
    data = pd.DataFrame(np.zeros(shape=(1, 6), dtype=np.int64), columns=col_names)

    for item in set(df.particle):
        sub = df[df.particle == item]

        if sub.shape[0] <= 2:
            # Cases in which particle only has 1 or 2 rows of data
            pass
        else:
            # print('Deriving velocities for particle:', str(item))
            dvx = pd.DataFrame(np.gradient(sub.x), columns=['dx', ])
            dvy = pd.DataFrame(np.gradient(sub.y), columns=['dy', ])

            new_df = pd.concat((dvx, dvy, sub.x.reset_index(drop=True), sub.y.reset_index(drop=True),
                                sub.frame.reset_index(drop=True), sub.particle.reset_index(drop=True)),
                            axis=1, names=col_names, sort=False)
            data = pd.concat((data, new_df), axis=0)

    # This is to get rid of the first 'np.zeros' row and to reset indexes
    data = data.reset_index(drop=True)
    data = data.drop(0)
    data = data.reset_index(drop=True)

    return data


if __name__ == "__main__":
    # Video properties
    FPS = 10.0  # Frames per second 
    MPP = 0.618  # Microns per pixel, scale of objective.
    
    # Linking parameters
    SEARCH_RANGE_MICRONS = 250 # microns/s. Fastest a particle could be traveling. Determines "how far" to look to link.
    MEMORY = 0  # number of frames the blob can dissapear and still be remembered
    stubs_seconds = 1.0  # trajectory needs to exist for at least this many seconds to be tracked
    STUBS = stubs_seconds * FPS  # trajectory needs to exist for at least this many frames to be tracked

    # Filtering parameters
    MIN_VELOCITY = None  # um / s  threshold forward velocity, not used unless code above is uncommented.
    MIN_DIAMETER = 4.5  # um
    MIN_AREA = np.pi * (MIN_DIAMETER / 2) ** 2
    MAX_AREA = 36000 # um^2

    # Link each csv from ImageJ in imagej_data
    data_paths = glob('imagej_data/*.csv')
    linked_data = pd.DataFrame()
    for path in data_paths:
        df_sub = link(path, FPS, MPP, SEARCH_RANGE_MICRONS, MEMORY, STUBS, MIN_VELOCITY, MIN_AREA, MAX_AREA)
        linked_data = pd.concat([linked_data, df_sub])

    
    # Save
    d = datetime.datetime.today()
    timendate = d.strftime('%y%m%d_%I%M%p')
    linked_data.to_csv(f'linked_results/{timendate}.csv')