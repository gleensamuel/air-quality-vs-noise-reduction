import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import gdown

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Cleaner Air, Quieter Cities",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Cleaner Air, Quieter Cities")
st.caption("Interactive Environmental Co-Benefit Dashboard (2025–2050)")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    file_id = "1wP9DORPQrk4aYz1OAfsqfqEp38CU2HJn"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "data.xlsx"
    gdown.download(url, output, quiet=True)
    df = pd.read_excel(output)
    df.columns = df.columns.astype(str)
    return df

df = load_data()

# ======================
# CLEANING
# ======================
df = df[df['co-benefit_type'].isin(['air_quality', 'noise'])]
df = df.drop_duplicates()
num_cols = df.select_dtypes(include=['float64', 'int64']).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

tahun_cols = [str(y) for y in range(2025, 2051)]

st.info(
    "📌 **Background & Objectives Connecting technical data with the everyday stories of city residents** 
    Cities with heavy traffic face two interrelated environmental problems: declining air quality and high road noise. Various low-emission transportation and traffic management policies not only target air pollution reduction, but also have the potential to reduce noise levels in residential areas.

This visualization uses data on air quality and noise indicators measured for each small area and several years of projections. The goal is to show how a single intervention can yield two benefits at once (“co-benefits”), as well as to help readers see spatial and temporal patterns that are not immediately apparent from tables of raw numbers.

In the following sections, the storyline moves from the daily problems experienced by residents, the relationship between the two indicators, areas that improved more quickly, to the dynamics of change over time for a particular area.
)

# ======================
# SIDEBAR
# ======================
st.sidebar.header("⚙️ Dashboard Controls")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun Analisis",
    tahun_cols,
    index=10
)

selected_type = st.sidebar.radio(
    "Jenis Co-Benefit",
    ['air_quality', 'noise']
)

# ======================
# KPI METRICS
# ======================
air_total = df[df['co-benefit_type'] == 'air_quality'][tahun_cols].sum().sum()
noise_total = df[df['co-benefit_type'] == 'noise'][tahun_cols].sum().sum()

col1, col2 = st.columns(2)
col1.metric("🌬️ Total Air Quality Improvement", f"{air_total:,.0f}")
col2.metric("🔇 Total Noise Reduction", f"{noise_total:,.0f}")

st.divider()

# ======================
# TREND LINE
# ======================
st.subheader("📈 Tren Co-Benefit Tahunan")

air_year = df[df['co-benefit_type'] == 'air_quality'][tahun_cols].sum()
noise_year = df[df['co-benefit_type'] == 'noise'][tahun_cols].sum()

df_years = pd.DataFrame({
    "Year": [int(y) for y in tahun_cols],
    "Air Quality Improvement": air_year.values,
    "Noise Reduction": noise_year.values
})

fig_line = px.line(
    df_years,
    x="Year",
    y=["Air Quality Improvement", "Noise Reduction"],
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

st.info(
    "📌 **Interpretasi:** Grafik ini menunjukkan bahwa peningkatan kualitas udara "
    "dan pengurangan kebisingan memiliki tren naik yang konsisten dari tahun ke tahun, "
    "menandakan adanya *co-benefit lingkungan jangka panjang*."
)

# ======================
# TOP 5 AIR QUALITY
# ======================
st.subheader("🌬️ Top 5 Wilayah dengan Air Quality Improvement Terbaik")

air_top5 = (
    df[df['co-benefit_type'] == 'air_quality']
    .groupby('small_area')[tahun_cols]
    .sum()
    .sum(axis=1)
    .reset_index(name='Total Air Quality')
    .sort_values('Total Air Quality', ascending=False)
    .head(5)
)

fig_air_top5 = px.bar(
    air_top5,
    x='small_area',
    y='Total Air Quality',
    text='Total Air Quality',
    title="Top 5 Wilayah – Air Quality Improvement (2025–2050)",
)

fig_air_top5.update_traces(textposition='outside')
fig_air_top5.update_layout(yaxis_title="Total Air Quality Improvement")

st.plotly_chart(fig_air_top5, use_container_width=True)

st.info(
    "🌬️ **Penjelasan:** Wilayah-wilayah ini menunjukkan peningkatan kualitas udara "
    "tertinggi selama periode 2025–2050. Hal ini mengindikasikan efektivitas kebijakan "
    "pengendalian emisi dan potensi lingkungan hidup yang lebih sehat."
)

# ======================
# TOP 5 NOISE REDUCTION
# ======================
st.subheader("🔇 Top 5 Wilayah dengan Noise Reduction Terbaik")

noise_top5 = (
    df[df['co-benefit_type'] == 'noise']
    .groupby('small_area')[tahun_cols]
    .sum()
    .sum(axis=1)
    .reset_index(name='Total Noise Reduction')
    .sort_values('Total Noise Reduction', ascending=False)
    .head(5)
)

fig_noise_top5 = px.bar(
    noise_top5,
    x='small_area',
    y='Total Noise Reduction',
    text='Total Noise Reduction',
    title="Top 5 Wilayah – Noise Reduction (2025–2050)",
    color='Total Noise Reduction'
)

fig_noise_top5.update_traces(textposition='outside')
fig_noise_top5.update_layout(yaxis_title="Total Noise Reduction")

st.plotly_chart(fig_noise_top5, use_container_width=True)

st.info(
    "🔇 **Penjelasan:** Wilayah dengan tingkat pengurangan kebisingan tertinggi "
    "menunjukkan keberhasilan pengelolaan transportasi, tata kota, dan pembatasan "
    "aktivitas bising di area permukiman."
)

# ======================
# SCATTER COMFORT ZONE
# ======================
st.subheader("🎯 Comfort Zone Analysis")

x_mean = df_years["Air Quality Improvement"].mean()
y_mean = df_years["Noise Reduction"].mean()

df_years["Comfort Zone"] = np.where(
    (df_years["Air Quality Improvement"] > x_mean) &
    (df_years["Noise Reduction"] < y_mean),
    "Most Comfortable",
    "Other"
)

fig_scatter = px.scatter(
    df_years,
    x="Air Quality Improvement",
    y="Noise Reduction",
    color="Comfort Zone",
    hover_data=["Year"],
)

fig_scatter.add_vline(x=x_mean, line_dash="dash")
fig_scatter.add_hline(y=y_mean, line_dash="dash")

st.plotly_chart(fig_scatter, use_container_width=True)

st.success(
    "🎯 **Makna Kebijakan:** Area di kuadran kanan-bawah merepresentasikan "
    "kondisi paling nyaman bagi masyarakat—udara bersih dengan tingkat kebisingan rendah."
)

# ======================
# TOP AREA BAR
# ======================
st.subheader("🏆 Top Wilayah dengan Co-Benefit Tertinggi")

area_total = (
    df.groupby(['small_area', 'co-benefit_type'])[tahun_cols]
    .sum()
    .sum(axis=1)
    .reset_index(name="Total Value")
)

fig_bar = px.bar(
    area_total.sort_values("Total Value", ascending=False).head(10),
    x="small_area",
    y="Total Value",
    color="co-benefit_type"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.info(
    "🏙️ **Insight Wilayah:** Grafik ini membantu mengidentifikasi wilayah prioritas "
    "yang paling diuntungkan oleh kebijakan lingkungan."
)

# ======================
# INTERACTIVE MAP (SIMULATED)
# ======================
st.subheader("🗺️ Interactive Area Map")

map_df = (
    df[df['co-benefit_type'] == selected_type]
    .groupby('small_area')[selected_year]
    .sum()
    .reset_index()
)

# Simulasi koordinat (ranking-based visualization)
map_df['lat'] = np.random.uniform(-6.3, -6.1, len(map_df))
map_df['lon'] = np.random.uniform(106.7, 106.9, len(map_df))

fig_map = px.scatter_mapbox(
    map_df,
    lat="lat",
    lon="lon",
    size=selected_year,
    color=selected_year,
    hover_name="small_area",
    zoom=10,
    mapbox_style="carto-positron"
)

st.plotly_chart(fig_map, use_container_width=True)

st.warning(
    "🗺️ **Catatan Peta:** Lokasi bersifat simulatif. "
    "Jika tersedia data koordinat wilayah, peta dapat ditingkatkan menjadi geo-map akurat."
)

# ======================
# CORRELATION HEATMAP
# ======================
st.subheader("🔥 Heatmap Korelasi")

corr = df[tahun_cols].corr()
fig, ax = plt.subplots(figsize=(14,6))
sns.heatmap(corr, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.info(
    "🔥 **Interpretasi:** Nilai korelasi yang tinggi menunjukkan bahwa "
    "peningkatan kualitas udara dan penurunan kebisingan berkembang secara konsisten."
)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("📊 Data Visualization • Streamlit • Plotly • Environmental Analytics")
