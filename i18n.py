# =============================================================================
# i18n.py: English / Japanese (日本語) switch for the COVID-19 Surveillance Explorer
# Author:   Genie Tang
# Version:  v1
#
# How it works: covid_explorer.py keeps its English text. When the sidebar language
# is 日本語, this module translates text on its way to the page (labels, markdown,
# tables, chart titles and hover text). English is the default and is never changed.
# Open the Japanese version directly with ?lang=ja at the end of the app address.
# To add or fix a Japanese phrase, edit DATA below (english text -> japanese text).
# =============================================================================
import functools
import re

import streamlit as st
from streamlit.delta_generator import DeltaGenerator as _DG

DATA = {
 "exact": {
  "COVID-19 by Country": "国別 COVID-19",
  "Countries": "国",
  "Add a country": "国を追加",
  "Type or pick a country": "国名を入力または選択",
  "Add": "追加",
  "Selected countries (click x to remove)": "選択した国（xで削除）",
  "Up to 6 countries can be compared at once. Remove one first.": "同時に比較できるのは最大6か国です。先にどれかを削除してください。",
  "Display options": "表示オプション",
  "Measure": "指標",
  "Cases": "感染者数",
  "Deaths": "死亡者数",
  "Count type": "件数の種類",
  "Daily new": "日別の新規",
  "Cumulative": "累計",
  "Per 100,000 people": "人口10万人あたり",
  "Divides by the CSSE population estimate so countries of different sizes can be compared.": "CSSEの人口推計で割るので、人口規模の異なる国を比べられます。",
  "7-day average": "7日間平均",
  "Trailing 7-day mean. Many countries reported only on weekdays or once a week, so raw daily counts jump between zero and large spikes.": "直近7日間の平均です。平日だけ、または週1回だけ報告した国が多く、日別の件数は0と大きな山の間を行き来します。",
  "Negative daily values (data corrections)": "日別のマイナス値（データの訂正）",
  "Hide (show as a gap)": "表示しない（空白にする）",
  "Set to zero": "0にする",
  "Keep as reported": "報告どおりにする",
  "A negative daily value means the country revised its total downward. It is not a real count of new cases.": "日別のマイナス値は、その国が累計を下方修正したことを表します。実際の新規感染者数ではありません。",
  "Chart layout": "グラフの配置",
  "One chart": "1つのグラフ",
  "One panel per country": "国ごとにパネルを分ける",
  "Separate panels help when one country's counts dwarf the others.": "1か国の件数がほかの国より極端に大きいときは、パネルを分けると見やすくなります。",
  "Log scale (y-axis)": "対数目盛（縦軸）",
  "Date range": "期間",
  "Daily COVID-19 Cases and Deaths by Country": "国別の新型コロナ（COVID-19）日別感染者数と死亡者数",
  "Spatial Statistics": "空間統計",
  "Chart": "グラフ",
  "Map": "地図",
  "World Map": "世界地図",
  "Alerts": "アラート",
  "Summary Table": "集計表",
  "User Guide": "使い方",
  "About the Data": "データについて",
  "Add at least one country in the sidebar to see the chart.": "グラフを表示するには、サイドバーで国を1つ以上追加してください。",
  "Add at least one country in the sidebar to see the map.": "地図を表示するには、サイドバーで国を1つ以上追加してください。",
  "Add at least one country in the sidebar to see the world map.": "世界地図を表示するには、サイドバーで国を1つ以上追加してください。",
  "Add at least one country in the sidebar to see the spatial statistics.": "空間統計を表示するには、サイドバーで国を1つ以上追加してください。",
  "Add at least one country in the sidebar to see the alerts.": "アラートを表示するには、サイドバーで国を1つ以上追加してください。",
  "Add at least one country in the sidebar to see the table.": "表を表示するには、サイドバーで国を1つ以上追加してください。",
  "Hover for every country's value on a date. Drag on the chart to zoom; double-click to reset.": "グラフにカーソルを合わせると、その日の全ての国の値を表示します。グラフ上をドラッグすると拡大し、ダブルクリックで元に戻ります。",
  "Download the plotted data (CSV)": "表示データをダウンロード（CSV）",
  "Map outlines are being fetched from the Plotly CDN. If the map is blank, static/world_110m.json is missing from the folder next to this script.": "地図の輪郭はPlotlyのCDNから読み込んでいます。地図が空白の場合は、このスクリプトと同じフォルダーに static/world_110m.json がありません。",
  "None of the selected entries has a map position.": "選択した項目には、地図上の位置がありません。",
  "Bubble area is proportional to the rate per 100,000 in the selected date window. Colors match the chart.": "バブルの面積は、選んだ期間の人口10万人あたりの率に比例します。色はグラフと同じです。",
  "⟲  Reset map view": "⟲  地図の表示をリセット",
  "Zoom back out to the whole world": "世界全体の表示に戻します",
  "Scroll or drag to zoom and pan. Press Reset map view above to return to the whole world.": "スクロールやドラッグで拡大と移動ができます。上の「地図の表示をリセット」を押すと、世界全体の表示に戻ります。",
  "Shade countries by": "色分けの基準",
  "Rate per 100,000": "人口10万人あたりの率",
  "Count": "実数",
  "Shading uses one blue scale from light to dark; the darkest step starts at the 98th percentile so a few extreme values do not flatten the rest. Selected countries are outlined in orange. Hover any country for its numbers.": "色分けは、薄い青から濃い青までの1つの色調です。一部の極端な値でほかの国の差が見えなくならないよう、最も濃い色は98パーセンタイルから始まります。選択した国はオレンジの枠で囲んでいます。国にカーソルを合わせると数値を表示します。",
  "Country": "国",
  "Population": "人口",
  "Cases in window": "期間内の感染者数",
  "Deaths in window": "期間内の死亡者数",
  "Cases per 100k": "感染者数（10万人あたり）",
  "Deaths per 100k": "死亡者数（10万人あたり）",
  "Deaths per 100 cases": "100感染者あたりの死亡者数",
  "Neighbours per country (k nearest, great-circle distance)": "1か国あたりの近隣国の数（大圏距離によるk近傍）",
  "Global Moran's I": "全体のモランI",
  "Permutation p-value": "順列検定のp値",
  "High-High countries": "高-高の国",
  "Countries in analysis": "解析対象の国",
  "**Moran scatterplot**": "**モラン散布図**",
  "Standardised log rate (z)": "標準化した対数率（z）",
  "Spatial lag of z (neighbours' mean)": "空間ラグ（近隣国の平均のz）",
  "**Do countries with high case rates sit next to each other?** Global Moran's I measures that for the whole map; local Moran (LISA) finds the clusters.": "**感染率の高い国どうしは隣り合っているか？** 全体のモランIは地図全体でそれを調べ、局所モラン（LISA）はクラスターを特定します。",
  "**Do countries with high death rates sit next to each other?** Global Moran's I measures that for the whole map; local Moran (LISA) finds the clusters.": "**死亡率の高い国どうしは隣り合っているか？** 全体のモランIは地図全体でそれを調べ、局所モラン（LISA）はクラスターを特定します。",
  "**When would a surveillance system have raised an alert?** EARS C2 compares each day's cases with the mean and standard deviation of the previous 7 days (after a 2-day gap). A day more than 3 standard deviations above that baseline is an alert.": "**サーベイランスはいつアラートを出せたか？** EARS C2は、各日の感染者数を、直前の7日間（2日の間隔を置く）の平均と標準偏差と比べます。基準より標準偏差の3倍を超えて高い日がアラートです。",
  "**When would a surveillance system have raised an alert?** EARS C2 compares each day's deaths with the mean and standard deviation of the previous 7 days (after a 2-day gap). A day more than 3 standard deviations above that baseline is an alert.": "**サーベイランスはいつアラートを出せたか？** EARS C2は、各日の死亡者数を、直前の7日間（2日の間隔を置く）の平均と標準偏差と比べます。基準より標準偏差の3倍を超えて高い日がアラートです。",
  "Alert threshold (standard deviations above baseline)": "アラートのしきい値（基準より何標準偏差上か）",
  "Alert days in window": "期間内のアラート日数",
  "Days in window": "期間内の日数",
  "First alert": "最初のアラート",
  "Largest C2": "最大のC2",
  "Day of largest C2": "C2が最大の日",
  "Deaths per 100 cases is a case fatality ratio over the window. It depends on how much testing each country did, so it is not a measure of how deadly the virus was.": "100感染者あたりの死亡者数は、期間内の致命率です。各国の検査の量に左右されるため、ウイルスの致死性を示す指標ではありません。",
  "Loading CSSE data from GitHub...": "GitHubからCSSEデータを読み込んでいます...",
  "Running Moran's I and LISA...": "モランIとLISAを計算しています..."
 },
 "frag": {
  "999 random re-assignments<br>of the rates to countries": "999回のランダムな入れ替え<br>（率を国に再割り当て）",
  "High rates whose neighbours<br>also have high rates": "率が高く、近隣国も<br>率が高い国",
  "High-High": "高-高",
  "Low-Low": "低-低",
  "High-Low": "高-低",
  "Low-High": "低-高",
  "Not significant": "有意でない",
  "Similar rates sit together": "似た率の国が隣り合っている",
  "No clear spatial pattern": "はっきりした空間パターンなし",
  "Cases in window": "期間内の感染者数",
  "Deaths in window": "期間内の死亡者数",
  "Cases per 100k": "感染者数（10万人あたり）",
  "Deaths per 100k": "死亡者数（10万人あたり）",
  " (7-day average)": "（7日間平均）",
  "No values in this window.": "この期間に値はありません。",
  "No population is available for: ": "人口データがありません：",
  ". Per-capita values are blank.": "。人口あたりの値は空欄です。",
  ". Selected countries are outlined in orange.": "。選択した国はオレンジの枠で囲んでいます。",
  " · bubble area": " · バブルの面積",
  "Could not load the CSSE data from GitHub: ": "GitHubからCSSEデータを読み込めませんでした：",
  "'>GitHub</a>). App ": "'>GitHub</a>）。アプリ",
  ".</p>": "。</p>",
  "; font-size:1.05rem; margin-top:-0.4rem'>Pick countries in the sidebar and compare how reported cases and deaths moved from January 2020 to March 2023. Source: Johns Hopkins CSSE COVID-19 time series (<a href='": "; font-size:1.05rem; margin-top:-0.4rem'>サイドバーで国を選び、2020年1月から2023年3月までに報告された感染者数と死亡者数の推移を比べられます。出典：ジョンズ・ホプキンス大学CSSE COVID-19時系列データ（<a href='",
  ": %{customdata[0]:,.0f}<br>Per 100,000: %{customdata[1]:,.1f}<br>Population: %{customdata[2]:,.0f}<extra></extra>": "：%{customdata[0]:,.0f}<br>10万人あたり：%{customdata[1]:,.1f}<br>人口：%{customdata[2]:,.0f}<extra></extra>",
  "<b>%{text}</b><br>z = %{x:.2f}<br>spatial lag = %{y:.2f}<extra></extra>": "<b>%{text}</b><br>z = %{x:.2f}<br>空間ラグ = %{y:.2f}<extra></extra>",
  "<br>Rate per 100,000: %{customdata[0]:,.0f}<br>p = %{customdata[1]:.3f}<extra></extra>": "<br>10万人あたりの率：%{customdata[0]:,.0f}<br>p = %{customdata[1]:.3f}<extra></extra>",
  "Alert: %{y:,.0f} (C2 = %{customdata:.1f})<extra></extra>": "アラート：%{y:,.0f}（C2 = %{customdata:.1f}）<extra></extra>",
  "Method: rates per 100,000 for the selected date window, log10-transformed because they are right-skewed. Spatial weights: each country's k nearest neighbours by great-circle distance between the CSSE country positions, row-standardised. Global Moran's I and local Moran statistics from PySAL esda with 999 permutations. High-High: a high-rate country surrounded by high-rate neighbours; Low-Low: the reverse; High-Low and Low-High are spatial outliers. Expected I under no spatial pattern: ": "方法：選んだ期間の人口10万人あたりの率を使い、分布が右に偏っているためlog10変換しています。空間重み：CSSEの国の位置の間の大圏距離で各国のk個の近隣国を選び、行で標準化しています。全体のモランIと局所モランは、PySAL esdaで999回の並べ替えにより計算しています。高-高：率の高い国が、率の高い近隣国に囲まれている。低-低：その逆。高-低と低-高は空間的な外れ値です。空間パターンがない場合のIの期待値：",
  ". Reported rates reflect testing and reporting practices, which themselves cluster regionally, so the clusters describe the reported data, not necessarily infection.": "。報告された率は検査と報告の方法を反映しており、それ自体が地域ごとにまとまる傾向があります。このため、クラスターは報告データを表すもので、必ずしも感染そのものを表すわけではありません。",
  "Method: EARS C2 (CDC Early Aberration Reporting System). Baseline = the 7 days ending 2 days before the day being tested; C2 = (count - baseline mean) / baseline SD, with the SD floored at 0.2. Negative daily values (corrections) are set to zero before testing. Weekly reporting, where a country posts a whole week on one day, produces alerts on reporting days; the first alerts of each wave are the ones worth reading. The same method runs in the author's automated influenza alert report for Japan's IDWR data.": "方法：EARS C2（CDCの早期異常検知システム）。基準期間は、検査する日の2日前で終わる7日間です。C2 =（件数 − 基準期間の平均）÷ 基準期間のSD で、SDの下限は0.2です。日別のマイナス値（訂正）は、検査の前に0にしています。国が1週間分を1日にまとめて報告する場合は、その報告日にアラートが出ます。読む価値があるのは、各流行の波の最初のアラートです。同じ方法を、作成者による日本のIDWRデータのインフルエンザ自動アラートレポートでも使っています。",
  "\n**Getting started**\n1. In the sidebar, pick a country in **Add a country** and press **Add**. You can also type\n   straight into **Selected countries**. Remove a country with the **x** on its tag.\n   Up to six countries can be compared at once; each keeps its color while selected.\n2. Choose **Cases** or **Deaths**, then **Daily new** or **Cumulative**.\n3. Turn on **Per 100,000 people** to compare countries of different sizes.\n4. For daily counts, the **7-day average** smooths out weekday and weekly reporting patterns.\n   Choose how to show **negative daily values** (downward corrections to a country's total).\n5. **One panel per country** gives each country its own y-axis, which helps when one\n   country's numbers dwarf the others. **Log scale** is another way to handle that.\n6. Drag the **Date range** slider to zoom in on a period. The tiles, map and table all\n   follow the selected range.\n\n**Reading the results**\n- The tiles above the chart show each country's most recent value in the window, its\n  peak and the peak date (daily view), and the total for the window.\n- Hover over the chart to see every selected country's value on that date.\n- The **Map** tab places the selected countries with bubble area proportional to the\n  rate per 100,000 in the window.\n- The **World map** tab shades every country by its rate (or count) for the window,\n  outlines the selected countries, and ranks all countries in a table below.\n- The **Spatial statistics** tab tests whether high rates cluster geographically\n  (global Moran's I) and maps the clusters (LISA). Change the number of neighbours\n  to see how stable the result is.\n- The **Alerts** tab runs EARS C2 aberration detection on each selected country's\n  daily counts and marks the days a surveillance system would have raised an alert.\n- The **Summary table** tab gives totals, per-capita rates and deaths per 100 cases.\n- **Download the plotted data** saves exactly what is on the chart as a CSV file.\n": "\n**はじめに**\n1. サイドバーの**国を追加**で国を選び、**追加**を押します。**選択した国**に直接入力することもできます。国を外すには、タグの**x**を押します。同時に比較できるのは最大6か国で、選択している間は各国の色が変わりません。\n2. **感染者数**または**死亡者数**を選び、次に**日別の新規**または**累計**を選びます。\n3. 人口規模の異なる国を比べるには、**人口10万人あたり**をオンにします。\n4. 日別の件数では、**7日間平均**が平日だけの報告や週1回の報告によるばらつきをならします。**日別のマイナス値**（国の累計の下方修正）の表示方法も選べます。\n5. **国ごとにパネルを分ける**と、国ごとに縦軸が分かれます。1か国の数値がほかの国より極端に大きいときに役立ちます。**対数目盛**でも対応できます。\n6. **期間**のスライダーを動かすと、期間を絞り込めます。カード、地図、表は全て選んだ期間に合わせて変わります。\n\n**結果の見方**\n- グラフの上のカードには、各国の期間内の最新値、ピークとその日付（日別の表示のとき）、期間内の合計を表示します。\n- グラフにカーソルを合わせると、その日の選択した全ての国の値を表示します。\n- **地図**タブでは、選択した国をバブルで表示します。バブルの面積は、期間内の人口10万人あたりの率に比例します。\n- **世界地図**タブでは、全ての国を期間内の率（または実数）で色分けし、選択した国を枠で囲み、下の表で全ての国を順位づけします。\n- **空間統計**タブでは、率の高い国が地理的に集まっているか（全体のモランI）を検定し、クラスターを地図に示します（LISA）。近隣国の数を変えると、結果がどれだけ安定しているかを確認できます。\n- **アラート**タブでは、選択した各国の日別件数にEARS C2による異常検知を行い、サーベイランスシステムがアラートを出したはずの日に印をつけます。\n- **集計表**タブでは、合計、人口あたりの率、100感染者あたりの死亡者数を表示します。\n- **表示データをダウンロード**を押すと、グラフに表示しているデータをそのままCSVファイルで保存します。\n",
  "\n**Source.** Johns Hopkins University Center for Systems Science and Engineering (CSSE),\nCOVID-19 Data Repository, global time series of confirmed cases and deaths\n([link](": "\n**出典：** ジョンズ・ホプキンス大学システム科学工学センター（CSSE）、COVID-19データリポジトリ、確定感染者数と死亡者数の世界の時系列データ（[リンク](",
  ")). Population, ISO3 codes and map positions come from the CSSE\n`UID_ISO_FIPS_LookUp_Table.csv`. CSSE stopped collecting data on March 10, 2023, so\nevery series ends on **": ")）。人口、ISO3コード、地図上の位置は、CSSEの `UID_ISO_FIPS_LookUp_Table.csv` によります。CSSEは2023年3月10日にデータの収集を終えたため、全ての系列は**",
  "**.\n\n**How the data were prepared**\n- Countries reported by province or territory (for example China, Canada, Australia,\n  the United Kingdom, and France, including overseas territories) were summed to\n  one national total.\n- The files report running totals. Daily new counts are the change from one day to\n  the next.\n- Some daily changes are negative because a country revised its total downward\n  (France removed about 349,000 cases on May 20, 2021). These are corrections, not\n  real counts, so by default they are hidden. Cumulative totals, the window totals in\n  the tiles, the map and the summary table are left as reported, so corrections still\n  count there.\n- Five entries are not countries: Diamond Princess, MS Zaandam, Summer Olympics 2020,\n  Winter Olympics 2022, and Antarctica. They can be viewed as counts but have no\n  population, so their per-capita values are blank.\n- Recovered counts are not shown because CSSE stopped tracking them in August 2021.\n\n**Limits of the data.** Confirmed cases depend on how much testing each country did,\nwhich changed over time and differs across countries. After home testing became\ncommon in 2022, many cases were never reported. Many countries also moved to weekly\nreporting, so a daily chart shows long flat stretches followed by spikes; the\n7-day average spreads these out. Comparisons across countries should be read with\nthese limits in mind.\n\n**Spatial statistics.** Global Moran's I and local Moran (LISA) from PySAL `esda`,\nwith k-nearest-neighbour weights (`libpysal`) on great-circle distance between the CSSE\ncountry positions, 999 permutations. **Alerts.** EARS C2 (7-day baseline, 2-day lag,\n3 SD threshold), the aberration-detection method used in syndromic surveillance.\n\n**Built with** Python, Streamlit, pandas, Plotly, PySAL (esda, libpysal). Code: `covid_explorer.py` ": "**で終わります。\n\n**データの準備方法**\n- 州や地域ごとに報告している国（中国、カナダ、オーストラリア、イギリス、フランスなど。海外領土を含む）は、合計して国全体の値にしました。\n- ファイルは累計を報告しています。日別の新規件数は、前日からの変化です。\n- 国が累計を下方修正したため、日別の変化がマイナスになる日があります（フランスは2021年5月20日に約349,000件の感染者を削除しました）。これは訂正で、実際の件数ではないため、初期設定では表示しません。累計、カードの期間内合計、地図、集計表は報告どおりのままなので、訂正もそこに含まれます。\n- 次の5つは国ではありません：ダイヤモンド・プリンセス号、MSザーンダム号、2020年夏季オリンピック、2022年冬季オリンピック、南極。件数は表示できますが、人口がないため、人口あたりの値は空欄です。\n- CSSEが2021年8月に回復者数の集計を終えたため、回復者数は表示していません。\n\n**データの限界** 確定感染者数は各国の検査の量によって変わり、その量は時期によっても国によっても異なります。2022年に自宅での検査が広まった後は、多くの感染が報告されませんでした。また、多くの国が週1回の報告に移ったため、日別のグラフでは平らな期間の後に急な山が現れます。7日間平均はこれをならします。国どうしの比較は、これらの限界を踏まえて読んでください。\n\n**空間統計** PySAL `esda` による全体のモランIと局所モラン（LISA）。重みは、CSSEの国の位置の間の大圏距離によるk近傍（`libpysal`）で、999回の並べ替えを使っています。**アラート** EARS C2（7日間の基準期間、2日の間隔、しきい値3SD）。症候群サーベイランスで使われる異常検知の方法です。\n\n**使用した技術** Python、Streamlit、pandas、Plotly、PySAL（esda、libpysal）。コード：`covid_explorer.py` ",
  ".\n\nGenie Tang, research scientist, spatial epidemiologist; doctoral research in public\nhealth informatics, Johns Hopkins Bloomberg School of Public Health. Portfolio: [spatialhealthinformatics.github.io](https://spatialhealthinformatics.github.io).\n": "。\n\nGenie Tang、リサーチサイエンティスト、空間疫学者。ジョンズ・ホプキンス大学ブルームバーグ公衆衛生大学院で公衆衛生情報学の博士研究に取り組んでいます。ポートフォリオ：[spatialhealthinformatics.github.io](https://spatialhealthinformatics.github.io)\n"
 },
 "countries": {
  "Afghanistan": "アフガニスタン",
  "Albania": "アルバニア",
  "Algeria": "アルジェリア",
  "Andorra": "アンドラ",
  "Angola": "アンゴラ",
  "Antarctica": "南極",
  "Antigua and Barbuda": "アンティグア・バーブーダ",
  "Argentina": "アルゼンチン",
  "Armenia": "アルメニア",
  "Australia": "オーストラリア",
  "Austria": "オーストリア",
  "Azerbaijan": "アゼルバイジャン",
  "Bahamas": "バハマ",
  "Bahrain": "バーレーン",
  "Bangladesh": "バングラデシュ",
  "Barbados": "バルバドス",
  "Belarus": "ベラルーシ",
  "Belgium": "ベルギー",
  "Belize": "ベリーズ",
  "Benin": "ベナン",
  "Bhutan": "ブータン",
  "Bolivia": "ボリビア",
  "Bosnia and Herzegovina": "ボスニア・ヘルツェゴビナ",
  "Botswana": "ボツワナ",
  "Brazil": "ブラジル",
  "Brunei": "ブルネイ",
  "Bulgaria": "ブルガリア",
  "Burkina Faso": "ブルキナファソ",
  "Burma": "ミャンマー",
  "Burundi": "ブルンジ",
  "Cabo Verde": "カーボベルデ",
  "Cambodia": "カンボジア",
  "Cameroon": "カメルーン",
  "Canada": "カナダ",
  "Central African Republic": "中央アフリカ共和国",
  "Chad": "チャド",
  "Chile": "チリ",
  "China": "中国",
  "Colombia": "コロンビア",
  "Comoros": "コモロ",
  "Congo (Brazzaville)": "コンゴ共和国",
  "Congo (Kinshasa)": "コンゴ民主共和国",
  "Costa Rica": "コスタリカ",
  "Cote d'Ivoire": "コートジボワール",
  "Croatia": "クロアチア",
  "Cuba": "キューバ",
  "Cyprus": "キプロス",
  "Czechia": "チェコ",
  "Denmark": "デンマーク",
  "Diamond Princess": "ダイヤモンド・プリンセス号",
  "Djibouti": "ジブチ",
  "Dominica": "ドミニカ国",
  "Dominican Republic": "ドミニカ共和国",
  "Ecuador": "エクアドル",
  "Egypt": "エジプト",
  "El Salvador": "エルサルバドル",
  "Equatorial Guinea": "赤道ギニア",
  "Eritrea": "エリトリア",
  "Estonia": "エストニア",
  "Eswatini": "エスワティニ",
  "Ethiopia": "エチオピア",
  "Fiji": "フィジー",
  "Finland": "フィンランド",
  "France": "フランス",
  "Gabon": "ガボン",
  "Gambia": "ガンビア",
  "Georgia": "ジョージア",
  "Germany": "ドイツ",
  "Ghana": "ガーナ",
  "Greece": "ギリシャ",
  "Grenada": "グレナダ",
  "Guatemala": "グアテマラ",
  "Guinea": "ギニア",
  "Guinea-Bissau": "ギニアビサウ",
  "Guyana": "ガイアナ",
  "Haiti": "ハイチ",
  "Holy See": "バチカン",
  "Honduras": "ホンジュラス",
  "Hungary": "ハンガリー",
  "Iceland": "アイスランド",
  "India": "インド",
  "Indonesia": "インドネシア",
  "Iran": "イラン",
  "Iraq": "イラク",
  "Ireland": "アイルランド",
  "Israel": "イスラエル",
  "Italy": "イタリア",
  "Jamaica": "ジャマイカ",
  "Japan": "日本",
  "Jordan": "ヨルダン",
  "Kazakhstan": "カザフスタン",
  "Kenya": "ケニア",
  "Kiribati": "キリバス",
  "Korea, North": "北朝鮮",
  "Korea, South": "韓国",
  "Kosovo": "コソボ",
  "Kuwait": "クウェート",
  "Kyrgyzstan": "キルギス",
  "Laos": "ラオス",
  "Latvia": "ラトビア",
  "Lebanon": "レバノン",
  "Lesotho": "レソト",
  "Liberia": "リベリア",
  "Libya": "リビア",
  "Liechtenstein": "リヒテンシュタイン",
  "Lithuania": "リトアニア",
  "Luxembourg": "ルクセンブルク",
  "MS Zaandam": "MSザーンダム号",
  "Madagascar": "マダガスカル",
  "Malawi": "マラウイ",
  "Malaysia": "マレーシア",
  "Maldives": "モルディブ",
  "Mali": "マリ",
  "Malta": "マルタ",
  "Marshall Islands": "マーシャル諸島",
  "Mauritania": "モーリタニア",
  "Mauritius": "モーリシャス",
  "Mexico": "メキシコ",
  "Micronesia": "ミクロネシア",
  "Moldova": "モルドバ",
  "Monaco": "モナコ",
  "Mongolia": "モンゴル",
  "Montenegro": "モンテネグロ",
  "Morocco": "モロッコ",
  "Mozambique": "モザンビーク",
  "Namibia": "ナミビア",
  "Nauru": "ナウル",
  "Nepal": "ネパール",
  "Netherlands": "オランダ",
  "New Zealand": "ニュージーランド",
  "Nicaragua": "ニカラグア",
  "Niger": "ニジェール",
  "Nigeria": "ナイジェリア",
  "North Macedonia": "北マケドニア",
  "Norway": "ノルウェー",
  "Oman": "オマーン",
  "Pakistan": "パキスタン",
  "Palau": "パラオ",
  "Panama": "パナマ",
  "Papua New Guinea": "パプアニューギニア",
  "Paraguay": "パラグアイ",
  "Peru": "ペルー",
  "Philippines": "フィリピン",
  "Poland": "ポーランド",
  "Portugal": "ポルトガル",
  "Qatar": "カタール",
  "Romania": "ルーマニア",
  "Russia": "ロシア",
  "Rwanda": "ルワンダ",
  "Saint Kitts and Nevis": "セントクリストファー・ネイビス",
  "Saint Lucia": "セントルシア",
  "Saint Vincent and the Grenadines": "セントビンセント・グレナディーン",
  "Samoa": "サモア",
  "San Marino": "サンマリノ",
  "Sao Tome and Principe": "サントメ・プリンシペ",
  "Saudi Arabia": "サウジアラビア",
  "Senegal": "セネガル",
  "Serbia": "セルビア",
  "Seychelles": "セーシェル",
  "Sierra Leone": "シエラレオネ",
  "Singapore": "シンガポール",
  "Slovakia": "スロバキア",
  "Slovenia": "スロベニア",
  "Solomon Islands": "ソロモン諸島",
  "Somalia": "ソマリア",
  "South Africa": "南アフリカ",
  "South Sudan": "南スーダン",
  "Spain": "スペイン",
  "Sri Lanka": "スリランカ",
  "Sudan": "スーダン",
  "Summer Olympics 2020": "2020年夏季オリンピック",
  "Suriname": "スリナム",
  "Sweden": "スウェーデン",
  "Switzerland": "スイス",
  "Syria": "シリア",
  "Taiwan*": "台湾",
  "Tajikistan": "タジキスタン",
  "Tanzania": "タンザニア",
  "Thailand": "タイ",
  "Timor-Leste": "東ティモール",
  "Togo": "トーゴ",
  "Tonga": "トンガ",
  "Trinidad and Tobago": "トリニダード・トバゴ",
  "Tunisia": "チュニジア",
  "Turkey": "トルコ",
  "Tuvalu": "ツバル",
  "US": "アメリカ",
  "Uganda": "ウガンダ",
  "Ukraine": "ウクライナ",
  "United Arab Emirates": "アラブ首長国連邦",
  "United Kingdom": "イギリス",
  "Uruguay": "ウルグアイ",
  "Uzbekistan": "ウズベキスタン",
  "Vanuatu": "バヌアツ",
  "Venezuela": "ベネズエラ",
  "Vietnam": "ベトナム",
  "West Bank and Gaza": "ヨルダン川西岸・ガザ",
  "Winter Olympics 2022": "2022年冬季オリンピック",
  "Yemen": "イエメン",
  "Zambia": "ザンビア",
  "Zimbabwe": "ジンバブエ"
 },
 "regex": [
  [
   "Totals between (\\d{4}年\\d+月\\d+日) and (\\d{4}年\\d+月\\d+日)\\. Counts are as reported, including corrections\\.",
   "\\1から\\2までの合計です。件数は訂正を含め、報告どおりです。"
  ],
  [
   "(\\d{4}年\\d+月\\d+日) to (\\d{4}年\\d+月\\d+日)",
   "\\1から\\2"
  ],
  [
   "Peak ([\\d,.]+|n/a) on (\\d{4}年\\d+月\\d+日)",
   "ピーク \\1（\\2）"
  ],
  [
   "Daily new cases",
   "日別の新規感染者数"
  ],
  [
   "Daily new deaths",
   "日別の新規死亡者数"
  ],
  [
   "Cumulative cases",
   "累計感染者数"
  ],
  [
   "Cumulative deaths",
   "累計死亡者数"
  ],
  [
   " on (\\d{4}年\\d+月\\d+日)",
   "、\\1"
  ],
  [
   " by (\\d{4}年\\d+月\\d+日)",
   "、\\1時点"
  ],
  [
   "([\\d,.]+|n/a) per 100k in window",
   "期間内 10万人あたり\\1"
  ],
  [
   "([\\d,.]+|n/a) cases in window",
   "期間内の感染者数 \\1"
  ],
  [
   "([\\d,.]+|n/a) deaths in window",
   "期間内の死亡者数 \\1"
  ],
  [
   "Population ([\\d,.]+|n/a)",
   "人口 \\1"
  ],
  [
   ", count\\b",
   "（実数）"
  ],
  [
   ", per 100,000 people",
   "（人口10万人あたり）"
  ],
  [
   "\\*\\*Cases per 100,000 people\\*\\*",
   "**人口10万人あたりの感染者数**"
  ],
  [
   "\\*\\*Deaths per 100,000 people\\*\\*",
   "**人口10万人あたりの死亡者数**"
  ],
  [
   "\\*\\*Cases per 100,000 in every country\\*\\*",
   "**全ての国の人口10万人あたりの感染者数**"
  ],
  [
   "\\*\\*Deaths per 100,000 in every country\\*\\*",
   "**全ての国の人口10万人あたりの死亡者数**"
  ],
  [
   "\\*\\*Cases in every country\\*\\*",
   "**全ての国の感染者数**"
  ],
  [
   "\\*\\*Deaths in every country\\*\\*",
   "**全ての国の死亡者数**"
  ],
  [
   "^Cases per 100,000$",
   "人口10万人あたりの感染者数"
  ],
  [
   "^Deaths per 100,000$",
   "人口10万人あたりの死亡者数"
  ],
  [
   "\\*\\*All countries ranked by cases per 100,000 in the window\\*\\*",
   "**期間内の人口10万人あたりの感染者数による全ての国の順位**"
  ],
  [
   "\\*\\*All countries ranked by deaths per 100,000 in the window\\*\\*",
   "**期間内の人口10万人あたりの死亡者数による全ての国の順位**"
  ],
  [
   "\\*\\*LISA clusters\\*\\* · cases per 100,000 · p below 0\\.05",
   "**LISAクラスター** · 人口10万人あたりの感染者数 · p値0.05未満"
  ],
  [
   "\\*\\*LISA clusters\\*\\* · deaths per 100,000 · p below 0\\.05",
   "**LISAクラスター** · 人口10万人あたりの死亡者数 · p値0.05未満"
  ],
  [
   "\\*\\*Daily cases with EARS C2 alerts\\*\\* · threshold ([\\d.]+) SD",
   "**EARS C2アラートつきの日別感染者数** · しきい値 \\1 SD"
  ],
  [
   "\\*\\*Daily deaths with EARS C2 alerts\\*\\* · threshold ([\\d.]+) SD",
   "**EARS C2アラートつきの日別死亡者数** · しきい値 \\1 SD"
  ],
  [
   "Expected (-?[\\d.]+) under no pattern",
   "パターンがない場合の期待値 \\1"
  ],
  [
   "With a rate and a map position<br>(\\d+) nearest neighbours each",
   "率と地図上の位置がある国<br>近隣国は各\\1か国"
  ],
  [
   "Slope = Moran's I \\((-?[\\d.]+)\\)",
   "傾き = モランI（\\1）"
  ],
  [
   "<br>Cases：",
   "<br>感染者数："
  ],
  [
   "<br>Deaths：",
   "<br>死亡者数："
  ]
 ]
}

EXACT = dict(DATA["exact"])
FRAG = dict(DATA["frag"])
NAMES = DATA["countries"]
EXACT.update(NAMES)
EXACT.update({"English": "English", "Alert": "アラート", "none": "なし"})

_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"]
# Dates first (Mar 09, 2023 and March 09, 2023 -> 2023年3月9日), then phrases whose
# word order changes in Japanese (numbers are kept).
DATES = []
for _i, _m in enumerate(_MONTHS, 1):
    DATES.append((r"\b" + _m + r" 0?(\d+), (\d{4})", r"\2年" + str(_i) + r"月\1日"))
    DATES.append((r"\b" + _m[:3] + r" 0?(\d+), (\d{4})", r"\2年" + str(_i) + r"月\1日"))
REGEX = DATES + DATA["regex"]
_DATES = [(re.compile(p), r) for p, r in DATES]
_REGEX = [(re.compile(p), r) for p, r in REGEX]
_FRAG_KEYS = sorted(FRAG, key=len, reverse=True)
_NAME_RE = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(sorted(map(re.escape, NAMES), key=len, reverse=True)) + r")(?![A-Za-z0-9])")


def is_ja():
    try:
        return st.session_state.get("lang") == "日本語"
    except Exception:
        return False


@functools.lru_cache(maxsize=8192)
def _tr(s):
    if s in EXACT:
        return EXACT[s]
    core = s.strip()
    if core and core in EXACT:
        return s.replace(core, EXACT[core])
    if s in FRAG:
        return FRAG[s]
    out = s
    if "<" in out:
        out = re.sub(r">([^<>]+)<", lambda m: ">" + EXACT.get(m.group(1), m.group(1)) + "<", out)
    for k in _FRAG_KEYS:
        if k in out:
            out = out.replace(k, FRAG[k])
    for pat, rep in _REGEX:
        out = pat.sub(rep, out)
    if re.search(r"[A-Za-z]", out):
        out = _NAME_RE.sub(lambda m: NAMES[m.group(1)], out)
    return out


def T(s):
    """Translate one string when the page is in Japanese; anything else passes through."""
    if not isinstance(s, str) or not s.strip() or not is_ja():
        return s
    return _tr(s)


def _cell(v):
    if not isinstance(v, str):
        return v
    if v in EXACT:
        return EXACT[v]
    for pat, rep in _DATES:
        v = pat.sub(rep, v)
    return v


_PLOT_KEYS = {"text", "hovertext", "hovertemplate", "name", "ticktext", "title", "customdata",
              "label", "labels", "legendgrouptitle", "annotations"}


def _walk(o, on=False):
    if isinstance(o, str):
        return _tr(o) if on else o
    if isinstance(o, dict):
        return {k: _walk(v, on or k in _PLOT_KEYS) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_walk(v, on) for v in o]
    if hasattr(o, "tolist") and getattr(o, "dtype", None) is not None and o.dtype.kind in "OU":
        return [_walk(v, on) for v in o.tolist()]
    return o


def _plotly(fig):
    try:
        import plotly.graph_objects as go
        j = fig.to_plotly_json()
        dates = any(getattr(tr.get("x"), "dtype", None) is not None and tr["x"].dtype.kind == "M"
                    for tr in j.get("data", []))
        out = go.Figure(_walk(j))
        if dates:  # date axes: 2021年7月 instead of Jul 2021
            out.update_xaxes(tickformat="%Y年%-m月", hoverformat="%Y年%-m月%-d日")
        return out
    except Exception:
        return fig


def _frame(df, config):
    import pandas as pd
    if not isinstance(df, pd.DataFrame):
        return df, config
    out = df.copy()
    for c in out.columns:
        if out[c].dtype == object or pd.api.types.is_string_dtype(out[c]):
            out[c] = out[c].map(_cell)
    out.columns = [T(c) if isinstance(c, str) else c for c in out.columns]
    if isinstance(config, dict):
        new = {}
        for k, v in config.items():
            if isinstance(v, dict):
                v = {kk: (T(vv) if kk in ("label", "help") and isinstance(vv, str) else vv) for kk, vv in v.items()}
            new[T(k) if isinstance(k, str) else k] = v
        config = new
    return out, config


_TEXT = {"markdown", "write", "caption", "info", "warning", "error", "success", "title", "header",
         "subheader", "button", "checkbox", "toggle", "download_button", "slider", "select_slider",
         "radio", "selectbox", "multiselect", "tabs", "dataframe", "plotly_chart"}
_CHOICE = {"radio", "selectbox", "multiselect", "select_slider"}


def _args(name, a, k):
    a, k = list(a), dict(k)
    if name == "tabs":
        if a:
            a[0] = [T(x) for x in a[0]]
        return a, k
    if name == "dataframe":
        if a:
            a[0], cfg = _frame(a[0], k.get("column_config"))
            if cfg is not None:
                k["column_config"] = cfg
        return a, k
    if name == "plotly_chart":
        if a:
            a[0] = _plotly(a[0])
        return a, k
    if a and isinstance(a[0], str):
        a[0] = T(a[0])
    for key in ("help", "placeholder", "label"):
        if isinstance(k.get(key), str):
            k[key] = T(k[key])
    if name == "slider" and k.get("format") == "MMM YYYY":
        k["format"] = "YYYY年M月"
    if name in _CHOICE:
        ff = k.get("format_func")

        def show(x, ff=ff):
            v = ff(x) if ff else x
            return T(v) if isinstance(v, str) else v

        k["format_func"] = show
    return a, k


def _wrap(name):
    orig = getattr(_DG, name)
    if getattr(orig, "_i18n", False):
        return

    @functools.wraps(orig)
    def w(self, *a, **k):
        if is_ja():
            a, k = _args(name, a, k)
        return orig(self, *a, **k)

    w._i18n = True
    setattr(_DG, name, w)
    setattr(st, name, getattr(st._main, name))


def install():
    """Patch Streamlit once; every call after that is a no-op."""
    for n in _TEXT:
        _wrap(n)
    if not getattr(st.set_page_config, "_i18n", False):
        orig = st.set_page_config

        @functools.wraps(orig)
        def spc(*a, **k):
            if is_ja() and isinstance(k.get("page_title"), str):
                k["page_title"] = T(k["page_title"])
            return orig(*a, **k)

        spc._i18n = True
        st.set_page_config = spc


def init_language():
    """Set the starting language once per session: English, or Japanese with ?lang=ja."""
    if "lang" not in st.session_state:
        want = str(st.query_params.get("lang", "")).lower()
        st.session_state["lang"] = "日本語" if want in ("ja", "jp", "japanese") else "English"


def language_switch():
    st.radio("Language / 言語", ["English", "日本語"], key="lang", horizontal=True)
