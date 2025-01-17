import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import json

# Konfigurasi halaman
st.set_page_config(
    page_title="Metode Numerik",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    h2 {
        color: #2c3e50;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Lottie Animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Animasi untuk setiap halaman
animations = {
    "home": "https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json",
    "interpolasi": "https://assets5.lottiefiles.com/private_files/lf30_rg5wrsf4.json",
    "integrasi": "https://assets5.lottiefiles.com/private_files/lf30_tw7yg1gi.json"
}

# Fungsi-fungsi numerik
def hitung_basis_lagrange(data_x, idx, nilai_x):
    basis = 1
    for j, x in enumerate(data_x):
        if j != idx:
            basis *= (nilai_x - x) / (data_x[idx] - x)
    return basis

def interpolasi_lagrange(data_x, data_y, nilai_x):
    hasil = 0
    for i, y in enumerate(data_y):
        hasil += y * hitung_basis_lagrange(data_x, i, nilai_x)
    return hasil

# Fungsi-fungsi integrasi
def trapezoidal_rule(x, y):
    n = len(x) - 1
    h = np.diff(x)
    integral = sum(0.5 * h[i] * (y[i] + y[i + 1]) for i in range(n))
    return integral

def midpoint_rule(x, y):
    n = len(x) - 1
    h = np.diff(x)
    midpoints = [(x[i] + x[i + 1]) / 2 for i in range(n)]
    midpoint_y = [(y[i] + y[i + 1]) / 2 for i in range(n)]
    integral = sum(h[i] * midpoint_y[i] for i in range(n))
    return integral

def simpson_rule(x, y):
    if len(x) < 3 or len(x) % 2 == 0:
        raise ValueError("Simpson's Rule membutuhkan jumlah titik ganjil dan >= 3.")
    n = len(x) - 1
    h = (x[-1] - x[0]) / n
    integral = y[0] + y[-1] + 4 * sum(y[1:n:2]) + 2 * sum(y[2:n-1:2])
    integral *= h / 3
    return integral

# Sidebar
with st.sidebar:
    st.title("🧮 Menu Navigasi")
    menu = st.radio(
        "",
        ["Home", "Interpolasi Lagrange", "Integrasi Numerik", "Team"],
        index=0,
    )
    
    st.markdown("---")
    
    if menu == "Team":
        st.header("👥 Tim Pengembang")
        team_data = [
            {"nama": "Naufal Haidar Nityasa", "nim": "22.11.5075"},
            {"nama": "Maahiroh Azzizah Tsabitah", "nim": "22.11.5114"},
            {"nama": "Muhammad Rifqi Hamzah", "nim": "22.11.5087"},
            {"nama": "Dyah Pramudya Sari", "nim": "22.11.5097"},
            {"nama": "Ikhwan Nurramadhan", "nim": "22.11.5129"}
        ]
        
        for member in team_data:
            with st.container():
                st.markdown(f"""
                    <div style='background-color: #90d5ff; padding: 10px; border-radius: 5px; margin: 5px;'>
                        <h4 style='margin: 0;'>{member['nama']}</h4>
                        <p style='margin: 0;'>{member['nim']}</p>
                    </div>
                """, unsafe_allow_html=True)

# Home
if menu == "Home":
    st.title("🔢 METODE NUMERIK")
    lottie_home = load_lottie_url(animations["home"])
    if lottie_home:
        st_lottie(lottie_home, height=300)
    
    st.markdown("""
    ## Selamat Datang di Aplikasi Metode Numerik! 📊
    
    Aplikasi ini menyediakan implementasi dari beberapa metode numerik populer:
    
    1. **Interpolasi Lagrange** 📈
       - Menghitung nilai antara dari serangkaian titik data
       - Visualisasi grafik interaktif
    
    2. **Integrasi Numerik** 📐
       - Metode Trapesium
       - Metode Titik Tengah
       - Metode Simpson
    
    Pilih menu di sidebar untuk memulai!
    """)

# Interpolasi Lagrange
elif menu == "Interpolasi Lagrange":
    st.title("📈 Interpolasi Lagrange")
    lottie_interpolasi = load_lottie_url(animations["interpolasi"])
    if lottie_interpolasi:
        st_lottie(lottie_interpolasi, height=200)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Input Data")
        jumlah_titik = st.number_input("Jumlah Titik Data", min_value=2, value=3, step=1)
        
        data_x, data_y = [], []
        for idx in range(jumlah_titik):
            cols = st.columns(2)
            x = cols[0].number_input(f"x{idx}", key=f"x{idx}")
            y = cols[1].number_input(f"y{idx}", key=f"y{idx}")
            data_x.append(x)
            data_y.append(y)
        
        nilai_x_target = st.number_input("Nilai x yang dicari")
        
        if st.button("Hitung", key="hitung_interpolasi"):
            try:
                hasil = interpolasi_lagrange(data_x, data_y, nilai_x_target)
                
                with col2:
                    st.subheader("Hasil dan Visualisasi")
                    st.success(f"Nilai y pada x = {nilai_x_target:.2f} adalah {hasil:.4f}")
                    
                    # Plotly visualization
                    x_vis = np.linspace(min(data_x) - 1, max(data_x) + 1, 500)
                    y_vis = [interpolasi_lagrange(data_x, data_y, x) for x in x_vis]
                    
                    fig = go.Figure()
                    
                    # Add interpolation curve
                    fig.add_trace(go.Scatter(
                        x=x_vis, y=y_vis,
                        mode='lines',
                        name='Kurva Interpolasi',
                        line=dict(color='blue', width=2)
                    ))
                    
                    # Add data points
                    fig.add_trace(go.Scatter(
                        x=data_x, y=data_y,
                        mode='markers',
                        name='Data Points',
                        marker=dict(size=10, color='red')
                    ))
                    
                    # Add interpolated point
                    fig.add_trace(go.Scatter(
                        x=[nilai_x_target], y=[hasil],
                        mode='markers',
                        name='Hasil Interpolasi',
                        marker=dict(size=12, color='green', symbol='star')
                    ))
                    
                    fig.update_layout(
                        title='Visualisasi Interpolasi Lagrange',
                        xaxis_title='x',
                        yaxis_title='y',
                        hovermode='closest',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
                
# Integrasi Numerik
elif menu == "Integrasi Numerik":
    st.title("📐 Integrasi Numerik")
    lottie_integrasi = load_lottie_url(animations["integrasi"])
    if lottie_integrasi:
        st_lottie(lottie_integrasi, height=200)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Input Data")
        
        # Pilihan metode integrasi
        metode = st.selectbox(
            "Pilih Metode",
            ["Trapezoidal Rule", "Midpoint Rule", "Simpson's Rule"],
            help="Pilih metode integrasi yang akan digunakan"
        )
        
        # Input jumlah titik data
        jumlah_titik = st.number_input("Jumlah Titik Data", min_value=2, value=5, step=1)
        
        # Input titik x dan y
        data_x, data_y = [], []
        for i in range(jumlah_titik):
            cols = st.columns(2)
            x = cols[0].number_input(f"x{i+1}", key=f"x{i}")
            y = cols[1].number_input(f"f(x{i+1})", key=f"y{i}")
            data_x.append(x)
            data_y.append(y)
        
        if st.button("Hitung", key="hitung_integrasi"):
            try:
                # Validasi jumlah titik
                if len(data_x) < 2 or len(data_y) < 2:
                    raise ValueError("Jumlah titik data minimal harus 2.")
                
                # Urutkan data berdasarkan x
                sorted_indices = sorted(range(len(data_x)), key=lambda i: data_x[i])
                x_sorted = [data_x[i] for i in sorted_indices]
                y_sorted = [data_y[i] for i in sorted_indices]
                
                # Hitung integral berdasarkan metode
                if metode == "Trapezoidal Rule":
                    integral = trapezoidal_rule(x_sorted, y_sorted)
                elif metode == "Midpoint Rule":
                    integral = midpoint_rule(x_sorted, y_sorted)
                elif metode == "Simpson's Rule":
                    integral = simpson_rule(x_sorted, y_sorted)
                
                # Tampilkan hasil di kolom kanan
                with col2:
                    st.subheader("Hasil dan Visualisasi")
                    st.success(f"Nilai integral: {integral:.6f}")
                    
                    # Visualisasi dengan Plotly
                    fig = go.Figure()
                    
                    # Tambahkan kurva data
                    fig.add_trace(go.Scatter(
                        x=x_sorted, y=y_sorted,
                        mode='lines+markers',
                        name='Data Titik',
                        line=dict(color='blue', width=2),
                        marker=dict(size=8, color='red')
                    ))
                    
                    fig.update_layout(
                        title=f'Visualisasi Integrasi ({metode})',
                        xaxis_title='x',
                        yaxis_title='f(x)',
                        hovermode='closest',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
