# MuTracker


This repository contains all of the scripts and macros needed to analyze multiple moving particles in microscopy videos and export their data.

Brief workflow overview:
1. Open raw video in ImageJ, crop and clip frames to analyze. Save as tiff image sequence in folder `/original_video`.
2. Open the macro contained in `/imagej` in Fiji (ImageJ) and run. This has two parameters to tweak, the threshold and minimum particle size. This identifies the "blobs" on each frame. This macro also saves a video of the blob outlines in `/imagej_outline_videos` so you can confirm the macro worked correctly.
3. Run `link.py` to link the blobs found by ImageJ on each frame together into cohesive trajectories. Filter based on minimum velocities, max and min areas, etc. Export data to a csv in `/linked_results`.
4. Analyze and plot data in `example_plots.ipynb`. I've included one plot, but the Python package [seaborn](https://seaborn.pydata.org/) has great documentation to plot different types of plots.
5. _Optional -_ Run `video_wheels.py` to generate a video with overlaid trajectories. Great to confirm your tracking is working as intended. As a bonus - it looks pretty cool.

## Background
For those unfamiliar with using Python, I highly recommend:
1. [Anaconda](https://www.anaconda.com/products/individual) - Great installer for Python that contains lots of scientific packages out of the box.
2. [VSCode](https://code.visualstudio.com/) - My favorite development environment for Python. It runs both scripts and jupyter notebooks, is lightweight, works well with virtual environments, and has great git integration.
3. [A low-level understanding of virtual environments](https://towardsdatascience.com/getting-started-with-python-environments-using-conda-32e9f2779307) - To use this package without manually adding all package dependencies yourself, I'd suggest using a virtual environment. The only command you need is `conda env create -f environment.yml` because I've already set up the list of packages in this repository.
4. [Fiji](https://imagej.net/Fiji) - Not Python, but used in this workflow because Fiji/ImageJ does blob identification really well.

## Changelog
2/15/2021
* Changed name from microtracker -> mutracker to match with other software.
* Added more explanation in the analysis portion of the software.
* Added FFT functionality to extract rotation rate
* Added single frame trajectory preview to avoid having to make an entire video.

## Extra info
Written by Coy Zimmermann in 2021 as part of my PhD thesis work on magnetically propelled microwheels in Dr. David W.M. Marr's group at the Colorado School of Mines.
