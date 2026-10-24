# COVID-19 Surveillance Explorer (covid_explorer.py, v1)

Genie Tang · [spatialhealthinformatics.github.io](https://spatialhealthinformatics.github.io)

A Streamlit web app for comparing reported COVID-19 cases and deaths across countries, built on the Johns Hopkins CSSE global time series:
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

## What it shows

- Up to six countries at once, each keeping one colour across every view.
- Cases or deaths, daily new or cumulative, raw counts or rates per 100,000.
- A 7-day average, a choice of how to treat negative "correction" days, one chart or one panel per country, a date range and a log scale.
- Headline tiles (latest value, peak and its date, total for the window), a bubble map, a world choropleth with a ranked table, a summary table.
- **Spatial statistics**: global Moran's I and LISA clusters of country rates (PySAL), with a Moran scatterplot.
- **Alerts**: EARS C2 aberration detection on each country's daily series, the method used in syndromic surveillance.

## Run it

```
pip install -r requirements.txt
streamlit run covid_explorer.py
```

No local data files are needed; the app reads the CSSE files from GitHub and caches them for 12 hours.

## Data preparation

- Province and territory rows are summed to national totals.
- Daily new counts are the day-to-day change in the running total.
- Negative daily values are reporting corrections; hidden by default, with options to set to zero or keep.
- Population, ISO3 codes and map positions come from the CSSE `UID_ISO_FIPS_LookUp_Table.csv`.
- Data end on March 9, 2023, when CSSE stopped collecting.
