# MuTracker


This repository contains all of the scripts and macros needed to analyze multiple moving particles in microscopy videos and export their data.

Brief workflow overview:
1. **Prep Video** Open raw video in ImageJ, crop and clip frames to analyze. Save as tiff image sequence in folder `/original_video`.
2. **Identify Blobs** Open the macro contained in `/imagej` in Fiji (ImageJ) using Plugins -> Macros -> Edit. Change the filepaths so they direct to your mutracker folder on your system and tweak the minimum particle size if you'd like to exclude small dust particles. This macro also saves a video of the blob outlines in `/imagej_outline_videos` so you can confirm the blob identification worked correctly.
3. **Link Blobs between frames** Run `link.py` to link the blobs found by ImageJ on each frame together into cohesive trajectories. Make sure to change `FPS`, `MPP`, as they change depending on the microscope used. Filters based on minimum velocities, max and min areas, etc. Exports data to a csv in `/linked_results`.
4. **Analyze and Plot** Use the prepared Python notebook `analysis.ipynb`. I've included some basic plots, but the Python package [seaborn](https://seaborn.pydata.org/) has great documentation to support custom plots to match your needs.
5. _Optional -_ Run `video_wheels.py` to generate a video with overlaid trajectories. Great to confirm your tracking is working as intended. As a bonus - it looks pretty cool.

Some notes:
* MuTracker is built to batch process videos. All of these steps will process *all* videos in their corresponding folder.
* Name your videos in `/original_video` with format `name_#` (ex. `glass_1`). This allows the code in `link.py` to name the data appropriately so you can plot it separately.
* This code is still a work in progress comes with no guarantees, and I encourage you to look through the code yourself so you understand what's going on! 

## Background
For those unfamiliar with using Python, I highly recommend:
1. [Anaconda](https://www.anaconda.com/products/individual) - Great installer for Python that contains lots of scientific packages out of the box.
2. [VSCode](https://code.visualstudio.com/) - My favorite development environment for Python. It runs both scripts and jupyter notebooks, is lightweight, works well with virtual environments, and has great git integration.
3. [A low-level understanding of virtual environments](https://towardsdatascience.com/getting-started-with-python-environments-using-conda-32e9f2779307) - To use this package without manually adding all package dependencies yourself, I'd suggest using a virtual environment. The only command you need is `conda env create -f environment.yml` because I've already set up the list of packages in this repository.
4. [Fiji](https://imagej.net/Fiji) - Not Python, but used in this workflow because Fiji/ImageJ does blob identification really well.

## Changelog
8/6/2021
* v1.0! Quality of life fixes, including:
* Changed the filename detection to just strip `.csv`, allowing for more flexibility with filenames
* Moved the `Label` column translation step its own function `label2frame` to isolate the most common stumbling block
* More explanation in `analysis.ipynb` about how plotting works and a link to a tutorial for pandas string comprehension

6/8/2021
* Added a method to either whitelist or blacklist tracked wheels using excel file `chosenwheels.xls`
* Added `xlrd` requirement in environment.yml
* Added `stubs_seconds` to more easily specify stubs instead of calculating the frames manually depending on your video fps
* Added frame and time annotation on the top of tracked videos generated from `video_wheels.py`

3/17/2021
* Cleaned up README, added more explanation
* By default, Fiji macro does an automatic binary step.
* Typo fixes in `analysis.ipynb`.

2/15/2021
* Changed name from microtracker -> mutracker to match with other software.
* Added more explanation in the analysis portion of the software.
* Added FFT functionality to extract rotation rate
* Added single frame trajectory preview to avoid having to make an entire video.

## Extra info
Written by Coy Zimmermann in 2021 as part of my PhD thesis work on magnetically propelled microwheels in Dr. David W.M. Marr's group at the Colorado School of Mines.
