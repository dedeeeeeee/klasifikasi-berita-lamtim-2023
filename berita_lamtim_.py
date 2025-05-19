import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

# Title
st.set_page_config(page_title="Klasifikasi Berita Lamtim 2023", layout="wide")
st.title("📊 Klasifikasi Berita Kabupaten Lampung Timur 2023")
st.markdown("Aplikasi ini mengelompokkan berita berdasarkan kategori menggunakan metode klasifikasi berbasis kata kunci, dan menampilkan visualisasi distribusi kategori serta analisis per bulan.")

# Load Data
try:
    df1 = pd.read_excel('Data Berita Lampung timur 2023.xlsx')
    st.success("✅ Data berhasil dimuat!")
except Exception as e:
    st.error(f"❌ Gagal memuat data: {e}")
    st.stop()

# Preprocessing
def kategorikan_berita(judul):
    judul = judul.lower()
    if any(keyword in judul for keyword in ['penembak', 'pencuri', 'pembunuh', 'tersangka', 'maling', 'penipuan', 'pengeroyokan', 'pengedar', 'judi', 'sabu', 'penculikan', 'cabuli', 'narkoba', 'tewas', 'korupsi', 'curanmor', 'buron', 'polres', 'polsek', 'begal', 'curi', 'kekerasan', 'penganiayaan']):
        return 'Kriminal'
    elif any(keyword in judul for keyword in ['politik', 'pemerintahan', 'pemilu', 'kpu', 'dprd', 'pilkades', 'dpd', 'uu', 'caleg', 'bupati']):
        return 'Politik dan Pemerintahan'
    elif any(keyword in judul for keyword in ['masyarakat', 'bencana', 'lingkungan', 'angin', 'roboh', 'banjir', 'kebun', 'kerusuhan']):
        return 'Sosial'
    elif any(keyword in judul for keyword in ['ekonomi', 'bisnis', 'pasar', 'umkm', 'pangan', 'industri']):
        return 'Ekonomi'
    elif any(keyword in judul for keyword in ['kesehatan', 'medis', 'rs', 'dokter', 'stunting', 'obat']):
        return 'Kesehatan'
    elif any(keyword in judul for keyword in ['pendidikan', 'sekolah', 'pelajar', 'guru', 'mahasiswa']):
        return 'Pendidikan'
    elif any(keyword in judul for keyword in ['satwa', 'pupuk', 'hewan', 'konservasi']):
        return 'Flora dan Fauna'
    else:
        return 'Lainnya'

df1['Kategori'] = df1['Judul_Berita'].apply(kategorikan_berita)

# --- Sidebar filter (opsional)
kategori_filter = st.sidebar.multiselect("Filter Kategori:", df1['Kategori'].unique(), default=list(df1['Kategori'].unique()))

df_filtered = df1[df1['Kategori'].isin(kategori_filter)]

# --- Show Data
st.subheader("📰 Tabel Data Berita")
st.dataframe(df_filtered, use_container_width=True)

# --- Pie Chart Distribusi Kategori
st.subheader("📈 Distribusi Kategori Berita")
kategori_counts = df_filtered['Kategori'].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(kategori_counts, labels=kategori_counts.index, autopct='%1.1f%%', startangle=140)
ax1.axis('equal')
st.pyplot(fig1)

# --- Bar Chart Per Bulan
st.subheader("📊 Persentase Kategori Berita per Bulan")

df_clean = df_filtered.dropna(subset=['Bulan'])

# Hitung persentase kategori per bulan
persentase_kriminal = []
bulan_pelanggaran_kriminal = sorted(df_clean['Bulan'].unique())

for bulan in bulan_pelanggaran_kriminal:
    data_bulan = df_clean[df_clean['Bulan'] == bulan]
    total_data_bulan = len(data_bulan)
    persentase = (data_bulan['Kategori'].value_counts() / total_data_bulan) * 100
    persentase_kriminal.append(persentase)

df_persentase = pd.concat(persentase_kriminal, axis=1, keys=bulan_pelanggaran_kriminal).T.fillna(0)

# Bar chart stacked
fig2, ax2 = plt.subplots(figsize=(12, 6))
bottom = np.zeros(len(df_persentase))
for kategori in df_persentase.columns:
    ax2.bar(df_persentase.index, df_persentase[kategori], bottom=bottom, label=kategori)
    bottom += df_persentase[kategori]

ax2.set_ylabel('Persentase (%)')
ax2.set_title('Persentase Kategori Berita per Bulan')
ax2.legend()
ax2.set_xticklabels(df_persentase.index, rotation=45)
st.pyplot(fig2)
