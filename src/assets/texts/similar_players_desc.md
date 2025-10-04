- Similar Players page is comprised of a player's per 90 stats and percentile ranks breakdown, inspired by Fotmob and FBRef's scout report styles, and similarity percentage rating.
- Percentile ranks are calculated and compared against positional peers with a minimum 90s played (5 90s for goalkeepers and 8 90s for outfield players).
- Minimum 90s is used to eliminate potential outliers due to players with insufficient playing time or too small sample size that can potentially skew the data heavily.
- Similarity percentages do not use all data on display on the left section, but only key metrics for each position being used (key metrics can be found on the Role Ratings page).

**How to read**:

- `p90` column indicates Player A's action volume per 90 minutes. (Why per 90s? Read [this](https://www.hudl.com/blog/an-introduction-to-the-per-90-metric) article from then-Statsbomb (now Hudl Statsbomb) to understand why it is easier to measure and compare per 90 stats than raw values.)
- `Percentile ranks` column indicates the percentage of players in the same position that Player A performs better in that metric. This ranking can be viewed by hover above the bar for each metric.
  - For example, Player A's goals percentile rank is **72**. This means Player A performs better in goals (or score more goals, in simpler language) than **72%** of players in her/their position.

**Notes**:

- Player positions are not guaranteed to be 100% correct, the positions are gathered and assumed using Soccerdonna's classification and FBRef's match logs. This is a known problem with women's football data and something that I have written about [here](https://www.talking-tactics.com/i/164710406/the-data) if you are interested in reading about the problems that I faced while doing the pre-processing step for the dataset.
- A few stats have been inverted (the less, the better), including all discipline stats and a couple of possession stats (miscontrols and dispossessed), since it makes more sense than ranking it by pure volume. Please take this into account when comparing against Fotmob's percentile ranks.

**Dev notes**:

- Only comparing similarity of main position...for now.
- Percentiles not include average pass/shot lengths since it's subjective and hard to rank.
- Highlight key metrics.
