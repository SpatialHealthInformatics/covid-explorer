# COVID-19 Surveillance Explorer

**Open the app:** https://covid-explorer.streamlit.app

An interactive app for comparing reported COVID-19 cases and deaths across countries, built on the Johns Hopkins CSSE global time series. The app is available in English and Japanese (日本語). Use the language switch at the top of the sidebar.

## What it shows

- Up to six countries at once, each keeping one color across every view.
- Cases or deaths, daily new or cumulative, raw counts or rates per 100,000.
- A 7-day average, a choice of how to treat negative "correction" days, one chart or one panel per country, a date range and a log scale.
- Headline tiles (latest value, peak and its date, total for the window), a bubble map, a world choropleth with a ranked table, and a summary table.
- **Spatial statistics:** global Moran's I and LISA clusters of country rates (PySAL), with a Moran scatterplot.
- **Alerts:** EARS C2 aberration detection on each country's daily series, the method used in syndromic surveillance.

## Data

- Province and territory rows are summed to national totals.
- Daily new counts are the day-to-day change in the running total.
- Negative daily values are reporting corrections. They are hidden by default, with options to set them to zero or keep them.
- Population, ISO3 codes and map positions come from the CSSE `UID_ISO_FIPS_LookUp_Table.csv`.
- Data end on March 9, 2023, when CSSE stopped collecting.

## Sources

- Johns Hopkins University CSSE COVID-19 Data Repository: https://github.com/CSSEGISandData/COVID-19
- Spatial statistics: PySAL (esda, libpysal).
- EARS C2: Hutwagner et al., 2003.

Genie Tang · [spatialhealthinformatics.github.io](https://spatialhealthinformatics.github.io)
