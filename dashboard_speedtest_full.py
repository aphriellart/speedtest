import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from streamlit_autorefresh import st_autorefresh

# Auto-refresh setiap 60 detik
st_autorefresh(interval=60 * 1000, limit=None, key="dashboard_refresh")

# Konfigurasi halaman
st.set_page_config(page_title="Speedtest Dashboard", layout="wide")

# CSS Bootstrap-like
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .card {
        padding: 20px;
        border-radius: 0.5rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .section-title {
        font-size: 4rem;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 50px;
        text-align: center;
    }
    .section-subtitle {
        font-size: 3rem;
        margin-top: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
csv_file = 'speedtest_log.csv'
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    st.error("File 'speedtest_log.csv' belum ditemukan. Jalankan script speedtest terlebih dahulu.")
    st.stop()

required_columns = ['timestamp', 'ping_ms', 'download_mbps', 'upload_mbps']
if not all(col in df.columns for col in required_columns):
    st.error(f"File CSV harus memiliki kolom: {required_columns}")
    st.stop()

latest = df.iloc[-1]

# Fungsi gauge chart
def create_gauge(title, value, min_val, max_val, unit, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
        },
        number={'suffix': f" {unit}", 'font': {'size': 44}}
    ))
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    return fig

# Judul
st.markdown('<div class="section-title">Dashboard Speedtest Internet MP Cikupa</div>', unsafe_allow_html=True)

# Gauge charts
st.markdown('<div class="section-subtitle">🚀 Kecepatan Terkini</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><div class="card-title">Ping</div>', unsafe_allow_html=True)
    st.plotly_chart(create_gauge("Ping", latest['ping_ms'], 0, 200, "ms", "orange"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><div class="card-title">Download</div>', unsafe_allow_html=True)
    st.plotly_chart(create_gauge("Download", latest['download_mbps'], 0, 150, "Mbps", "green"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><div class="card-title">Upload</div>', unsafe_allow_html=True)
    st.plotly_chart(create_gauge("Upload", latest['upload_mbps'], 0, 150, "Mbps", "blue"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Grafik tren
st.markdown('<div class="section-subtitle">📈 Grafik Tren Kecepatan</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><div class="card-title">Ping (ms)</div>', unsafe_allow_html=True)
    st.line_chart(df.set_index('timestamp')[['ping_ms']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><div class="card-title">Download (Mbps)</div>', unsafe_allow_html=True)
    st.line_chart(df.set_index('timestamp')[['download_mbps']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><div class="card-title">Upload (Mbps)</div>', unsafe_allow_html=True)
    st.line_chart(df.set_index('timestamp')[['upload_mbps']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Notifikasi kecepatan rendah
if latest['download_mbps'] < 10:
    st.warning(f"⚠️ Kecepatan download rendah: {latest['download_mbps']:.2f} Mbps")

# Ekspor ke Excel
st.markdown('<div class="section-subtitle">📤 Ekspor Data ke Excel</div>', unsafe_allow_html=True)
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Speedtest')
    return output.getvalue()

excel_data = convert_df_to_excel(df)
st.download_button(
    label="📥 Download Excel",
    data=excel_data,
    file_name='speedtest_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# Tabel data terbaru
st.markdown('<div class="section-subtitle">📌 Data Terbaru</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.dataframe(df.tail(10), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
