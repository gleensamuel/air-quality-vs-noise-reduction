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
# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
.section-box {
    background-color: #ffffff;
    padding: 32px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 35px;
}

.section-title {
    font-size: 30px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 12px;
}

.section-text {
    font-size: 16px;
    line-height: 1.75;
    color: #334155;
}

.card {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    height: 100%;
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 6px;
}

.card-desc {
    font-size: 14px;
    color: #64748b;
}
</style>
""", unsafe_allow_html=True)

st.title("🌱 Cleaner Air, Quieter Cities")
st.caption("Interactive Environmental Co-Benefit Dashboard (2025–2050)")
st.markdown("""
<div class="section-box">
    <div class="section-title">Background & Objectives</div>
    <div class="section-text">
        Connecting technical environmental data with the everyday experiences of city residents.<br><br>

        Cities with heavy traffic face two closely related environmental challenges:
        declining air quality and increasing road noise. Transportation and traffic
        management policies aimed at reducing emissions often produce multiple benefits,
        including improved acoustic comfort in residential areas.

        This dashboard visualizes projected air quality and noise indicators across
        multiple urban areas from 2025 to 2050. The main objective is to highlight
        <b>environmental co-benefits</b>, where a single policy intervention leads to
        simultaneous improvements in both air quality and noise reduction.

        Through interactive charts and spatial exploration, users can uncover temporal
        trends, regional disparities, and priority areas that benefit most from
        sustainable urban policies.
</div>
""", unsafe_allow_html=True)

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
st.markdown("## 🏙️ Everyday Problems in the City")
st.markdown("_Life in the City: Stuffy Air and Loud Noises_")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">🚗 Vehicle Exhaust</div>
        <div class="card-desc">
            The primary source of urban air pollution, especially in areas
            with high traffic density and fossil-fuel-based transportation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">📢 Road Noise</div>
        <div class="card-desc">
            Continuous exposure to traffic noise from engines and horns
            reduces acoustic comfort and impacts mental well-being.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">🌫️ Stuffy Air</div>
        <div class="card-desc">
            Pollutants trapped in narrow road corridors create unhealthy
            breathing conditions for nearby residents.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

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
# TOP 5 AIR QUALITY
# ======================
st.subheader("🌬️ Top 5 Regions with the Best Air Quality Improvement")

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
    title="Top 5 Reqions – Air Quality Improvement (2025–2050)",
)

fig_air_top5.update_traces(textposition='outside')
fig_air_top5.update_layout(yaxis_title="Total Air Quality Improvement")

st.plotly_chart(fig_air_top5, use_container_width=True)

st.info(
    "🌬️ **Summary:** These regions showed the highest air quality improvement during the 2025–2050 period. "
    "This indicates the effectiveness of emission control policies  "
    "and the potential for a healthier environment."
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
# FOOTER
# ======================
st.markdown("---")
st.caption("📊 Data Visualization • Streamlit • Plotly • Environmental Analytics")
