# A-League Women Recruitment Dashboard

## Overview

A football recruitment, Streamlit-hosted dashboard using Opta/FBRef's A-League Women data from the 2024-25 season.

- Inspired by a combination of Football Manager's Squad Planner and Data Hub screens.
- The name of this repo (`alw-toty-dashboard`) hints at the precessor idea to the current one, which was a dashboard for the 2024-25 Team of the Season.

## Information about the data

- Data is correct up until before the ALW Grand Final (May 18th, 2025). _(I can give the data an update but I'm too lazy to do the pre-processing stuff all over again. Besides, one match is a small sample size and would not change the data that much on the grand scheme of things)_.
- Player's main and other positions are _painstakingly, manually_ gathered from Opta data via Fotmob and FBRef's match logs.
- Advanced data files do not include player positions, but those files can be joined with the `PositionMap.csv` file to retrieve the positions.

## Repository structure

| Folder name                     | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| [assets](./src/assets/)         | Storing images, font files, and Markdown text files |
| [components](./src/components/) | Reusable Streamlit components and widgets           |
| [data](./data/)                 | Raw data files captured from FBRef                  |
| [pages](./src/pages/)           | Layout and data components for the app's pages      |
| [services](./src/services/)     | Calculation and data manipulation logic             |
| [styles](./src/styles/)         | App styling and team colours                        |
| [utils](./src/utils/)           | Reusable utility functions                          |

| File name                  | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| [index.py](./src/index.py) | Set up the app before the pages are loaded            |
| [main.py](main.py)         | Driver code to run the app from command line/terminal |
