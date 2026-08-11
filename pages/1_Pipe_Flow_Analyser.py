"""
Pipe Flow Analyser page.

Lets the user select a fluid, define pipe geometry, and compute
velocity, Reynolds number, friction factor, and pressure drop.
Also plots pressure drop vs. flow rate over a range.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from engineering import Fluid, Pipe

st.set_page_config(page_title="Pipe Flow Analyser", layout="wide")

st.title("Pipe Flow Analyser")
st.write(
    "Calculate velocity, Reynolds number, friction factor, and pressure drop "
    "for flow through a pipe, using the Darcy-Weisbach equation and the "
    "Swamee-Jain approximation for turbulent friction factor."
)

# ---- Sidebar inputs ----
st.sidebar.header("Fluid")

fluid_choice = st.sidebar.selectbox(
    "Select fluid", ["Water", "Air", "Crude Oil", "Custom"]
)

if fluid_choice == "Custom":
    density = st.sidebar.number_input("Density (kg/m³)", min_value=0.1, value=1000.0)
    viscosity = st.sidebar.number_input(
        "Viscosity (Pa·s)", min_value=0.00001, value=0.001, format="%.5f"
    )
    fluid = Fluid(name="Custom", density=density, viscosity=viscosity)
else:
    fluid = Fluid.from_preset(fluid_choice)
    st.sidebar.write(f"Density: {fluid.density} kg/m³")
    st.sidebar.write(f"Viscosity: {fluid.viscosity} Pa·s")

st.sidebar.header("Pipe Geometry")
diameter = st.sidebar.number_input("Diameter, D (m)", min_value=0.001, value=0.1)
length = st.sidebar.number_input("Length, L (m)", min_value=0.1, value=50.0)
roughness = st.sidebar.number_input(
    "Roughness, ε (m)", min_value=0.0, value=0.000045, format="%.6f"
)

st.sidebar.header("Flow")
flow_rate = st.sidebar.number_input(
    "Flow rate, Q (m³/s)", min_value=0.0001, value=0.02, format="%.4f"
)

# ---- Calculation ----
try:
    pipe = Pipe(diameter=diameter, length=length, roughness=roughness)
    result = pipe.analyze(fluid, flow_rate)

    regime = "Laminar" if result["reynolds_number"] < 2300 else "Turbulent"

    # ---- Metric displays ----
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocity", f"{result['velocity']:.3f} m/s")
    col2.metric("Reynolds Number", f"{result['reynolds_number']:,.0f}", regime)
    col3.metric("Friction Factor", f"{result['friction_factor']:.4f}")
    col4.metric("Pressure Drop", f"{result['pressure_drop']:,.1f} Pa")

    # ---- Plot: pressure drop vs flow rate ----
    st.subheader("Pressure Drop vs Flow Rate")

    flow_range = np.linspace(flow_rate * 0.2, flow_rate * 2.0, 50)
    pressure_drops = []
    for q in flow_range:
        r = pipe.analyze(fluid, q)
        pressure_drops.append(r["pressure_drop"])

    fig, ax = plt.subplots()
    ax.plot(flow_range, pressure_drops)
    ax.set_xlabel("Flow Rate (m³/s)")
    ax.set_ylabel("Pressure Drop (Pa)")
    ax.set_title(f"Pressure Drop vs Flow Rate ({fluid.name})")
    ax.grid(True)
    st.pyplot(fig)

    # ---- CSV export (full sweep) ----
    sweep_df = pd.DataFrame({
        "flow_rate_m3s": flow_range,
        "pressure_drop_Pa": pressure_drops,
    })
    csv = sweep_df.to_csv(index=False)
    st.download_button(
        label="Download sweep results as CSV",
        data=csv,
        file_name="pipe_flow_sweep.csv",
        mime="text/csv",
    )

except ValueError as e:
    st.error(f"Input error: {e}")