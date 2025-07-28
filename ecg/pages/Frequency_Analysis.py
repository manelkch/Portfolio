import streamlit as st
import os
import numpy as np
import wfdb
import matplotlib.pyplot as plt

#st.set_page_config(layout="wide")

WINDOW_SIZE = 200
DATA_DIR = "data"
CHANNELS = {'MLII': 0, 'V5': 1}  # Adaptable selon les leads disponibles

def compute_fft(signal, fs=360):
    N = len(signal)
    freqs = np.fft.fftfreq(N, d=1/fs)
    fft_values = np.fft.fft(signal)
    magnitude = np.abs(fft_values)
    return freqs[:N // 2], magnitude[:N // 2]

def get_beats_by_label(record_path, target_label, channel_index):
    record = wfdb.rdrecord(record_path)
    annotation = wfdb.rdann(record_path, 'atr')
    signal = record.p_signal[:, channel_index]

    beats = []
    for i, sample in enumerate(annotation.sample):
        label = annotation.symbol[i]
        if label != target_label:
            continue
        start = sample - WINDOW_SIZE // 2
        end = sample + WINDOW_SIZE // 2
        if start >= 0 and end < len(signal):
            beat = signal[start:end]
            beats.append(beat)
    return beats

def plot_comparison(normal_beat, abnormal_beat):
    f1, mag1 = compute_fft(normal_beat)
    f2, mag2 = compute_fft(abnormal_beat)

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    fig.patch.set_alpha(0)
    for ax in axes.flatten():
        ax.set_facecolor("none")

    axes[0, 0].plot(normal_beat, color="steelblue")
    axes[0, 0].set_title("Normal Beat (Time Domain)")

    axes[0, 1].plot(f1, mag1, color="teal")
    axes[0, 1].set_title("Normal Beat (Frequency Domain)")

    axes[1, 0].plot(abnormal_beat, color="indianred")
    axes[1, 0].set_title("Abnormal Beat (Time Domain)")

    axes[1, 1].plot(f2, mag2, color="darkred")
    axes[1, 1].set_title("Abnormal Beat (Frequency Domain)")

    for ax in axes.flatten():
        ax.grid(True)

    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("Beat Comparison: Time vs Frequency")

    st.markdown("""
    <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:20px">
        <h3 style="color:#003366;margin-top:0;">Compare ECG Beats in Time and Frequency Domains</h3>
        <p style="font-size:16px;">
            This tool allows you to explore the difference between a <strong>normal</strong> and an <strong>abnormal</strong> heartbeat
            from the same patient and specific ECG lead.
        </p>
    </div>
    """, unsafe_allow_html=True)

    patients = sorted([f[:-4] for f in os.listdir(DATA_DIR) if f.endswith('.dat')])

    with st.sidebar:
        st.header("Signal Selection")
        selected_patient = st.selectbox("Select Patient", patients)
        selected_channel = st.selectbox("Select Channel", CHANNELS.keys())

    if selected_patient:
        record_path = os.path.join(DATA_DIR, selected_patient)
        channel_index = CHANNELS[selected_channel]

        normal_beats = get_beats_by_label(record_path, 'N', channel_index)
        abnormal_beats = []
        for label in ['L', 'R', 'A', 'V']:
            abnormal_beats += get_beats_by_label(record_path, label, channel_index)

        if not normal_beats or not abnormal_beats:
            st.warning("This patient does not have both normal and abnormal beats for this channel.")
            return

        col1, col2 = st.columns(2)
        with col1:
            idx_n = st.slider("Select Normal Beat", 0, len(normal_beats)-1, 0)
        with col2:
            idx_a = st.slider("Select Abnormal Beat", 0, len(abnormal_beats)-1, 0)

        st.markdown(f"""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#1f77b4;">Comparison for Patient <code>{selected_patient}</code> - Channel <code>{selected_channel}</code></h4>
        </div>
        """, unsafe_allow_html=True)

        plot_comparison(normal_beats[idx_n], abnormal_beats[idx_a])

if __name__ == "__main__":
    main()
