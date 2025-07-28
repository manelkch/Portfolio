import streamlit as st
import wfdb
from streamlit_option_menu import option_menu
import numpy as np
import pywt
import matplotlib.pyplot as plt
import os
from preprocessing_methods import median_filter1D, bandpass_filter, median_bandpass_filter, plot_ecg_with_rpeaks, extract_beats, min_max_normalize
from scipy.ndimage import gaussian_filter1d
import neurokit2 as nk
import seaborn as sns
import pandas as pd
from collections import Counter

#st.set_page_config(layout="wide")

# Define sections and their content
sections = [ 
    "Denoising",
    "Normalization",
    "R-Peak Detection",
    "Data Compression",
    "Exploratory Data Analysis"
]

# Sidebar: clickable list of sections
with st.sidebar:
    selected_section = option_menu(
        menu_title=None,
        options=sections,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link-selected": {"background-color": "#dde7e4", "color": "black",}
        }
    )

if selected_section == "Denoising":
    st.session_state["chosen_filter"] = 'Median Filter'
    st.title("Data Denoising")

    # Patient & Channel Selection
    ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
           121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
           220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

    channels = {'MLII': 0, 'V5': 1}

    with st.sidebar:
        st.header("Filter Settings")
        patient = st.selectbox("Select Patient ID", ids)
        channel = st.selectbox("Select Channel", channels.keys())
        methods = [
            "Median Filter",
            "Bandpass Filter",
            "Median + Bandpass Filter",
            "Gaussian Filter"
        ]
        method = st.selectbox("Denoising Method", methods)

    # Intro card
    st.markdown(f"""
    <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h3 style="color:#003366;margin-top:0;">ECG Signal for Patient {patient}, Channel {channel}</h3>
        <p style="font-size:16px;">Below is the original ECG signal extracted from the MIT-BIH database. A 10-second window is used for visualization.</p>
    </div>
    """, unsafe_allow_html=True)

    # Load and display raw ECG signal
    record = wfdb.rdrecord(f'data/{patient}')
    signal = record.p_signal
    fs = record.fs
    end = int(10 * fs)

    st.markdown("""
    <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h4 style="color:#1f77b4;">Original ECG Signal (10 seconds)</h4>
    </div>
    """, unsafe_allow_html=True)
    st.line_chart(signal[:end, channels[channel]])

    # Denoising Method Section
    st.markdown(f"""
    <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h4 style="color:#004c6d;">Denoising Method Selected: {method}</h4>
        <p style="font-size:16px;">The chart below shows the denoised ECG signal using the selected method. You may try different filters and confirm your choice.</p>
    </div>
    """, unsafe_allow_html=True)

    # Apply selected filter
    denoised = None
    if method == "Median Filter":
        denoised = median_filter1D(signal[:end, channels[channel]], 3)
    elif method == "Bandpass Filter":
        denoised = bandpass_filter(signal[:end, channels[channel]])
    elif method == "Median + Bandpass Filter":
        denoised = median_bandpass_filter(signal[:end, channels[channel]])
    elif method == "Gaussian Filter":
        denoised = gaussian_filter1d(signal[:end, channels[channel]], sigma=2)

    # Display filtered signal
    if denoised is not None:
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #d62728;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#a32020;">Filtered ECG Signal</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(denoised)

        if st.button("Confirm This Denoising Method"):
            st.session_state["chosen_filter"] = method
            st.success(f"{method} has been selected as your denoising method.")


if selected_section == "Normalization":
    st.title("Signal Normalization")

    # Sélection patient / canal
    ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
           121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
           220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

    channels = {'MLII': 0, 'V5': 1}

    with st.sidebar:
        st.header("Signal Selection")
        patient = st.selectbox("Select Patient ID", ids)
        channel = st.selectbox("Select Channel", channels.keys())

    # Info carte
    st.markdown(f"""
    <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h3 style="color:#003366;margin-top:0;">ECG Signal of Patient {patient} - Channel {channel}</h3>
        <p style="font-size:16px;">
            The following visualization compares the filtered ECG signal (using your previously chosen method)
            with its normalized version using <strong>Min-Max scaling</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Chargement des données
    record = wfdb.rdrecord(f'data/{patient}')
    signal = record.p_signal
    fs = record.fs
    end = int(10 * fs)

    # Affichage de la méthode de filtrage choisie
    st.markdown(f"""
    <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h4 style="color:#004c6d;">Filtering Method Used</h4>
        <p style="font-size:16px;">{st.session_state.get('chosen_filter', 'Median Filter')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Application du filtre (ici median + bandpass car fixe)
    clean_signal = median_bandpass_filter(signal[:end, channels[channel]])
    normalized_signal = min_max_normalize(clean_signal)

    # Carte 1 – Signal filtré
    st.markdown("""
    <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
        <h4 style="color:#1f77b4;">Filtered ECG Signal (10 seconds)</h4>
    </div>
    """, unsafe_allow_html=True)
    st.line_chart(clean_signal)

    # Carte 2 – Signal normalisé
    st.markdown("""
    <div style="background-color:#ffffff;border-left:5px solid #ffaa00;padding:25px 40px;border-radius:12px;margin-bottom:20px">
        <h4 style="color:#cc7a00;">Normalized ECG Signal (Min-Max Scaling)</h4>
    </div>
    """, unsafe_allow_html=True)
    st.line_chart(normalized_signal)


if selected_section == "R-Peak Detection":
    st.title("R-Peak Detection")

    # Sélection patient / canal
    ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
           121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
           220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

    channels = {'MLII': 0, 'V5': 1}

    with st.sidebar:
        st.header("Signal Selection")
        patient = st.selectbox("Select Patient ID", ids)
        channel = st.selectbox("Select Channel", channels.keys())

    # Introduction
    st.markdown(f"""
    <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h3 style="color:#003366;margin-top:0;">R-Peak Detection on Patient {patient} – Channel {channel}</h3>
        <p style="font-size:16px;">The signal is filtered using your previously chosen method and analyzed to locate the R-peaks corresponding to each heartbeat.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chargement et filtrage du signal
    record = wfdb.rdrecord(f'data/{patient}')
    signal = record.p_signal
    fs = record.fs
    end = int(10 * fs)

    st.markdown(f"""
    <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h4 style="color:#004c6d;">Filtering Method Used</h4>
        <p style="font-size:16px;">{st.session_state.get('chosen_filter', 'Median Filter')}</p>
    </div>
    """, unsafe_allow_html=True)

    clean_signal = median_bandpass_filter(signal[:end, channels[channel]])

    # Affichage du signal filtré
    st.markdown("""
    <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
        <h4 style="color:#1f77b4;">Filtered ECG Signal (10 seconds)</h4>
    </div>
    """, unsafe_allow_html=True)
    st.line_chart(clean_signal)

    # Détection des R-peaks avec NeuroKit
    ecg_signals, ecg_info = nk.ecg_process(clean_signal, sampling_rate=360)
    r_peaks = ecg_info["ECG_R_Peaks"]

    # Visualisation des R-peaks
    st.markdown("""
    <div style="background-color:#e0f8ec;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h4 style="color:#208060;">Detected R-Peaks on ECG</h4>
        <p style="font-size:16px;">The following graph shows the ECG signal with detected R-peaks marked in red.</p>
    </div>
    """, unsafe_allow_html=True)
    plot_ecg_with_rpeaks(clean_signal, r_peaks, fs=360, duration=end)

    # Segmentation des battements
    st.markdown("""
    <div style="background-color:#fff9e6;padding:25px 40px;border-left:5px solid #f4a300;border-radius:12px;margin-bottom:20px">
        <h4 style="color:#b36b00;">Beat Segmentation</h4>
        <p style="font-size:16px;">The signal has been segmented around each detected R-peak to extract individual beats.</p>
    </div>
    """, unsafe_allow_html=True)

    beats = extract_beats(clean_signal, r_peaks)
    st.markdown(f"**Number of beats extracted:** {len(beats)}")

    # Exploration des battements
    st.markdown("""
    <div style="background-color:#f7fbfc;padding:25px 40px;border-radius:12px;margin-bottom:20px">
        <h4 style="color:#1b4965;">Beat Visualization (First 5 Beats)</h4>
        <p style="font-size:16px;">Each plot below represents an individual heartbeat extracted from the signal.</p>
    </div>
    """, unsafe_allow_html=True)

    fig, axs = plt.subplots(1, 5, figsize=(15, 2))

    # Enlever le fond blanc du canvas général
    fig.patch.set_alpha(0)

    for i in range(5):
        axs[i].plot(beats[i], color="steelblue")
        axs[i].set_title(f"Beat {i}", fontsize=10)
        axs[i].axis("off")
        axs[i].set_facecolor("none")  # Pas de fond pour chaque plot

    st.pyplot(fig)


if selected_section == "Data Compression":
    st.title("Data Compression")

    ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
           121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
           220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

    channels = {'MLII': 0, 'V5': 1}

    with st.sidebar:
        st.header("Signal Selection")
        patient = st.selectbox("Select Patient ID", ids)
        channel = st.selectbox("Select Channel", channels.keys())
        methods = ["Wavelet Level 1", "Wavelet Multilevel"]
        method = st.selectbox("Compression Method", methods)

    # Chargement du signal
    record = wfdb.rdrecord(f'data/{patient}')
    signal = record.p_signal
    fs = record.fs
    end = int(10 * fs)

    st.markdown(f"""
    <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h3 style="color:#003366;margin-top:0;">Original ECG Signal – Patient {patient}, Channel {channel}</h3>
        <p style="font-size:16px;">This is the raw signal (10 seconds) from the selected channel, before compression.</p>
    </div>
    """, unsafe_allow_html=True)
    st.line_chart(signal[0:end, channels[channel]])

    st.markdown(f"**Signal shape:** {signal.shape}")
    original_size = os.path.getsize(f"data/{patient}.dat")
    st.markdown(f"**Original .dat file size:** {original_size / 1024:.2f} KB")

    st.markdown(f"""
    <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
        <h4 style="color:#004c6d;">Selected Compression Method</h4>
        <p style="font-size:16px;">{method}</p>
    </div>
    """, unsafe_allow_html=True)

    if method == "Wavelet Level 1":
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#1f77b4;">Wavelet Decomposition – Level 1 (db3)</h4>
        </div>
        """, unsafe_allow_html=True)

        cA, cD = pywt.dwt(signal[:end, channels[channel]], 'db3')

        limit = st.slider("Select number of coefficients to visualize", min_value=100, max_value=2000, value=500, step=50)

        st.line_chart(cA[:limit])
        st.line_chart(cD[:limit])

        st.markdown("""
        <div style="background-color:#f9f9f9;border-left:5px solid #999;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#444;">Reconstructed Signal (from A1+D1)</h4>
        </div>
        """, unsafe_allow_html=True)

        reconstructed_signal = pywt.idwt(cA, cD, 'db3')
        st.line_chart(reconstructed_signal[:limit])

        # Compression fichier
        output_dir = "data/compressed"
        os.makedirs(output_dir, exist_ok=True)

        compressed_channels = []
        for i in range(signal.shape[1]):
            cA, _ = pywt.dwt(signal[:, i], wavelet='db4')  # niveau 1
            compressed_channels.append(cA)

        min_len = min(len(c) for c in compressed_channels)
        compressed_signal = np.vstack([c[:min_len] for c in compressed_channels]).T

        wfdb.wrsamp(record_name=os.path.join(output_dir, f"{patient}_wavelet1_compressed"),
                    fs=fs,
                    units=record.units,
                    sig_name=record.sig_name,
                    p_signal=compressed_signal)

        compressed_size = os.path.getsize(os.path.join(output_dir, f"{patient}_wavelet1_compressed.dat"))
        st.markdown(f"**Compressed file size:** {compressed_size / 1024:.2f} KB")
        st.markdown(f"**Compression ratio:** {compressed_size / original_size:.2%}")

    elif method == "Wavelet Multilevel":
        level = st.slider("Select decomposition level", min_value=1, max_value=5, value=3, step=1)

        st.markdown(f"""
        <div style="background-color:#ffffff;border-left:5px solid #ff7f0e;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#d65c00;">Wavelet Multilevel Decomposition – Level {level}</h4>
        </div>
        """, unsafe_allow_html=True)

        coeffs = pywt.wavedec(signal[:end, channels[channel]], 'db4', level=level)

        for i, coeff in enumerate(coeffs):
            st.line_chart(coeff[:end])
            if i == 0:
                st.markdown(f"**Approximation A{level}**")
            else:
                st.markdown(f"**Detail D{level - i + 1}**")

        st.markdown("""
        <div style="background-color:#f9f9f9;border-left:5px solid #999;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#444;">Reconstructed Signal (from all levels)</h4>
        </div>
        """, unsafe_allow_html=True)

        reconstructed_signal = pywt.waverec(coeffs, 'db4')[:end]
        st.line_chart(reconstructed_signal)


if selected_section == "Exploratory Data Analysis":
    st.title("Exploratory Data Analysis")

    DATA_DIR = 'data'
    WINDOW_SIZE = 200

    @st.cache_resource
    def load_beat_statistics():
        all_labels = []
        patient_label_map = {}

        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.dat'):
                record_name = filename[:-4]
                record_path = os.path.join(DATA_DIR, record_name)

                try:
                    record = wfdb.rdrecord(record_path)
                    annotation = wfdb.rdann(record_path, 'atr')
                    ecg_signal = record.p_signal[:, 0]
                except:
                    continue

                labels = []
                for i, sample in enumerate(annotation.sample):
                    label = annotation.symbol[i]
                    if label not in ['N', 'L', 'R', 'A', 'V']:
                        continue
                    start = sample - WINDOW_SIZE // 2
                    end = sample + WINDOW_SIZE // 2
                    if start >= 0 and end < len(ecg_signal):
                        labels.append(label)
                        all_labels.append(label)

                patient_label_map[record_name] = labels

        return all_labels, patient_label_map


    def show_beat_distribution():
        st.markdown("""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h3 style="color:#003366;">Beat Distribution Overview</h3>
            <p style="font-size:16px;">This section provides a global view of the types of beats annotated in the dataset.</p>
        </div>
        """, unsafe_allow_html=True)

        all_labels, patient_label_map = load_beat_statistics()
        label_counts = Counter(all_labels)
        df_label_counts = pd.DataFrame(label_counts.items(), columns=['Label', 'Count']).sort_values(by='Count', ascending=False)

        # Total Beats per Class
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#1f77b4;">Total Beats per Class</h4>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_label_counts)

        fig, ax = plt.subplots()
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        sns.barplot(data=df_label_counts, x='Label', y='Count', palette='Set2', ax=ax)
        ax.set_title("Total Beats per Label")
        st.pyplot(fig)

        # Normal vs Abnormal
        total_normal = label_counts.get('N', 0)
        total_abnormal = sum(label_counts[l] for l in ['L', 'R', 'A', 'V'])
        df_bin = pd.DataFrame({'Class': ['Normal', 'Abnormal'], 'Count': [total_normal, total_abnormal]})

        st.markdown("""
        <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#004c6d;">Normal vs Abnormal Beats</h4>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Normal Beats", total_normal)
        with col2:
            st.metric("Abnormal Beats", total_abnormal)

        fig2, ax2 = plt.subplots()
        fig2.patch.set_alpha(0)
        ax2.set_facecolor("none")
        sns.barplot(data=df_bin, x='Class', y='Count', palette='coolwarm', ax=ax2)
        ax2.set_title("Binary Class Distribution")
        st.pyplot(fig2)

        # Per-patient Beat Count
        patient_data = []
        for patient, labels in patient_label_map.items():
            row = {
                'Patient': patient,
                'Total Beats': len(labels),
                'Normal (N)': labels.count('N'),
                'LBBB (L)': labels.count('L'),
                'RBBB (R)': labels.count('R'),
                'Atrial (A)': labels.count('A'),
                'Ventricular (V)': labels.count('V'),
            }
            patient_data.append(row)

        df_patient = pd.DataFrame(patient_data).sort_values(by='Total Beats', ascending=False)

        st.markdown("""
        <div style="background-color:#fff9e6;border-left:5px solid #f4a300;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#b36b00;">Beat Distribution per Patient</h4>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_patient)

        fig3, ax3 = plt.subplots(figsize=(12, 5))
        fig3.patch.set_alpha(0)
        ax3.set_facecolor("none")
        df_patient.set_index("Patient")[["Normal (N)", "LBBB (L)", "RBBB (R)", "Atrial (A)", "Ventricular (V)"]].plot(
            kind="bar", stacked=True, ax=ax3)
        ax3.set_ylabel("Beats")
        ax3.set_title("Beats per Patient")
        st.pyplot(fig3)

    show_beat_distribution()
