"""
Heat Transfer Calculator page.

Section 1: Steady-state conduction through a flat wall (Fourier's law).
Section 2: Newton's Law of Cooling - time to reach a target temperature,
           with an interactive cooling curve.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from engineering import Wall, CoolingObject

st.set_page_config(page_title="Heat Transfer Calculator", layout="wide")

st.title("Heat Transfer Calculator")
st.write(
    "Calculate steady-state conduction through a flat wall, and model an "
    "object cooling toward ambient temperature over time."
)

# ============================================================
# Section 1: Conduction
# ============================================================
st.header("1. Steady-State Conduction (Fourier's Law)")
st.write(
    "Computes the rate of heat flow through a single flat wall, given its "
    "thickness, area, thermal conductivity, and the temperature on each side."
)

col1, col2 = st.columns(2)
with col1:
    thickness = st.number_input("Wall thickness, L (m)", min_value=0.001, value=0.05)
    area = st.number_input("Wall area, A (m²)", min_value=0.01, value=2.0)
    k_wall = st.number_input(
        "Thermal conductivity, k (W/m·K)", min_value=0.001, value=0.8,
        help="e.g. concrete ~0.8, steel ~50, glass wool ~0.04"
    )
with col2:
    t_hot = st.number_input("Hot-side temperature, T_hot (°C)", value=80.0)
    t_cold = st.number_input("Cold-side temperature, T_cold (°C)", value=20.0)

try:
    wall = Wall(thickness=thickness, area=area, thermal_conductivity=k_wall)
    q = wall.heat_transfer_rate(t_hot=t_hot, t_cold=t_cold)
    st.metric("Heat Transfer Rate", f"{q:,.1f} W")
except ValueError as e:
    st.error(f"Input error: {e}")

st.divider()

# ============================================================
# Section 2: Newton's Law of Cooling
# ============================================================
st.header("2. Newton's Law of Cooling")
st.write(
    "Computes how long an object takes to cool from its initial temperature "
    "to a target temperature in a given ambient environment, and plots the "
    "cooling curve over time."
)

col3, col4 = st.columns(2)
with col3:
    t0 = st.number_input("Initial temperature, T₀ (°C)", value=90.0)
    t_inf = st.number_input("Ambient temperature, T∞ (°C)", value=25.0)
with col4:
    k_cool = st.number_input(
        "Cooling constant, k (1/s)", min_value=0.0001, value=0.02, format="%.4f",
        help="Typical range: 0.001-0.05 per second, depends on the object and environment"
    )
    t_target = st.number_input("Target temperature (°C)", value=40.0)

try:
    obj = CoolingObject(initial_temp=t0, ambient_temp=t_inf, cooling_constant=k_cool)
    time_to_target = obj.time_to_reach(t_target)
    st.metric("Time to Reach Target", f"{time_to_target:,.1f} s")

    # Build the cooling curve, well beyond the target time so the marker
    # has room to move
    t_max = time_to_target * 2
    time_range = np.linspace(0, t_max, 200)
    temps = [obj.temperature_at(t) for t in time_range]

    st.subheader("Cooling Curve")
    time_marker = st.slider(
        "Time (s)", min_value=0.0, max_value=float(t_max), value=0.0
    )
    marker_temp = obj.temperature_at(time_marker)

    fig, ax = plt.subplots()
    ax.plot(time_range, temps, label="Temperature")
    ax.axhline(t_target, color="red", linestyle="--", label="Target temp")
    ax.plot(time_marker, marker_temp, "o", color="orange", markersize=10, label="Current time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Object Temperature vs Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.write(f"At t = {time_marker:.1f} s, temperature = {marker_temp:.1f} °C")

except ValueError as e:
    st.error(f"Input error: {e}")