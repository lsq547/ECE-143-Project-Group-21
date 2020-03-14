# ECE-143-Project-Group-21

Analysis of Steam Games

## Group members

Yue Qiao (Henry): yuq021@ucsd.edu

Shiqi Liu: shl352@ucsd.edu

Matheus Gorski: mgorski@ucsd.edu

Yifan Cao: y8cao@ucsd.edu

## Overview

In 2017, Steam, the most popular platform for purchasing and playing computer games, generated over 4.5 Billion USD in revenue. In order to better understand the many factors that drive the changes in this industry, it is necessary to take a closer look at following factors:
* The developers and publishers of Steam games
* Distribution of system requirements for Steam users
* Trend of genres and tags of Steam games

## Dataset

Steam Games Dataset: https://www.kaggle.com/nikdavis/steam-store-games

Datasets contain a variety of information about almost every computer games released before May 2019 on popular gaming platform Steam and a third party Steam database website SteamSpy. Datasets include information such as user reviews, average play time, developers, genres, tags indicating style of games, and number of people who own the title.

## File Structure
The datasets folder contains all data needed for processing. 

The src folder contains all .py files for data processing, analysis and plotting. 

The jupter notebook contains all commands to run python scripts and show visualizations.
```
├── datasets
|   ├── steam.csv
|   ├── steam_requirements_data.csv
|   └── steamspy_data.csv
|   └── steamspy_tag_data.csv
├── src
|   ├── data_processing.py
|   ├── developer_and_publisher.py
|   ├── system_requirements.py
|   ├── tag_analysis.py
├── Final Project.ipynb
├── Steam Analysis Group 21 Presentation Slides.pdf
├── README.md
```

## Required Packages
* regex
* DateTime
* scipy
* pandas
* numpy
* matplotlib
* seaborn

To install these packages, use command:
```
pip install [packagename]
```
