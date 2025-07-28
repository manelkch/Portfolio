import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import wfdb


def load_ecg_patient():
    ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 
                121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 
                220, 221, 222, 223, 228, 230, 231, 232, 233, 234]
    
    channels = {'MLII' : 0, 'V5' : 1}
        
    patient = st.sidebar.selectbox("Patient", ids)

    channel = st.sidebar.selectbox("Channel", channels.keys())

    record = wfdb.rdrecord(f'data/{patient}')
    signal = record.p_signal

    return patient, channel, record, signal


def plot_ecg_patient(patient, channel, record, signal):
    channels = {'MLII' : 0, 'V5' : 1}
    fs = record.fs
    end = int(10 * fs)

    st.write(f"ECG Visualization of Patient : {patient} and channel {channel}")

    st.markdown("ECG Signal Data")

    st.line_chart(signal[0:end, channels[channel]])


def plot_ecg(record, signal, channel):
    channels = {'MLII' : 0, 'V5' : 1}
    fs = record.fs
    end = int(10 * fs)
    st.line_chart(signal[0:end, channels[channel]])


def median_filter1D(values, window_size) -> np.array:

        result = np.zeros(len(values) - (window_size-1))
        
        for i in range(0, result.shape[0]):
            window = np.median(values[i:(i+window_size)])
            result[i] = window.mean()
        return result

def bandpass_filter(data, fs=360, lowcut=0.5, highcut=40.0, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq # Low cutoff frequency (Hz)
    high = highcut / nyq # High cutoff frequency (Hz)
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def median_bandpass_filter(ecg_signal, fs=360, median_kernel=5, lowcut=0.5, highcut=40.0, order=4):

    ecg_median = medfilt(ecg_signal, kernel_size=median_kernel)

    #Passe-bande Butterworth
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    ecg_filtered = filtfilt(b, a, ecg_median)

    return ecg_filtered


def extract_beats(signal, r_peaks, fs=360, window_size=0.6):
    half_window = int((fs * window_size) // 2)
    beats = []
    for r in r_peaks:
        if r > half_window and r + half_window < len(signal):
            beat = signal[r - half_window: r + half_window]
            beats.append(beat)
    return np.array(beats)



def plot_ecg_with_rpeaks(ecg_signal, r_peaks, fs=360, duration=30):

    samples = duration * fs
    ecg_signal = ecg_signal[:samples]
    r_peaks = [idx for idx in r_peaks if idx < samples]
    t = np.arange(len(ecg_signal)) / fs

    # Crée la figure Plotly
    fig = go.Figure()

    # Courbe du signal ECG (ligne continue, sans marqueurs)
    fig.add_trace(go.Scatter(
        x=t,
        y=ecg_signal,
        mode='lines',
        name='Signal',
        line=dict(color='blue')
    ))

    # Points R-peaks (seuls les marqueurs)
    fig.add_trace(go.Scatter(
        x=np.array(r_peaks) / fs,
        y=ecg_signal[r_peaks],
        mode='markers',
        name='R-peak',
        marker=dict(color='red', size=8, symbol='circle')
    ))

    # Mise en page
    fig.update_layout(
        title="ECG avec R-peaks détectés",
        xaxis_title="Temps (s)",
        yaxis_title="ECG",
        height=400,
        legend=dict(x=0.01, y=0.99),
    )

    st.plotly_chart(fig, use_container_width=True)

def get_labels(annotation, r_peaks):
    r_labels = []
    ann_idx = annotation.sample
    ann_sym = annotation.symbol
    for r in r_peaks:
        match = [s for i, s in zip(ann_idx, ann_sym) if abs(i - r) <= 5]
        r_labels.append(match[0] if match else "N")
    return np.array(r_labels)



def min_max_normalize(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return np.zeros_like(signal)
    return (signal - min_val) / (max_val - min_val)