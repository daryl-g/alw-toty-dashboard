# A-League Women TOTY Dashboard

## Overview

Repo for the Streamlit dashboard for the 2024-25 A-League Women Team of the Season.

Currently the repository is only housing the raw advanced data file retrieved from FBRef.

## Information about the data

- Data is correct up until before the ALW Grand Final (May 18th, 2025). _(I can give the data an update but I'm too lazy to do the pre-processing stuff all over again. Besides, one match is a small sample size and would not change the data that much on the grand scheme of things)_.
- Player's main and other positions are _painstakingly, manually_ gathered from Opta data via Fotmob and FBRef's match logs.
- Advanced data files do not include player positions, but those files can be joined with the `PositionMap.csv` file to retrieve the positions.

## Roadmap

**Initial idea**:

- Streamlit dashboard with around 5 pages:
  - My own TOTY + best player for each position (by percentile + calculated role score).
  - Raw stats + calculated role scores for all players of each position (Goalkeeper, Defender, Midfielder, Forward).
- Roles are loosely based on Football Manager-defined roles.
  - Some roles that require tracking data to identify like B2B Midfielder are removed/ignored.
  - Role score are basically an overall rating, comprised of relevant metrics for each role along with its weighting, chosen manually.
- Allow the user to modify the role score, the TOTY, and filter the data based on their preferences.
- Use Streamlit's session data to move player selections between pages.
- Rely more on Plotly to create interactive vizzes, instead of using mplsoccer for static vizzes.
  - Gotta create these vizzes without the help of a package written specifically for football/soccer vizzes...somehow. Could be potential future work to create an mplsoccer equivalent, but for Plotly _(will need a lot of work tho)_.
