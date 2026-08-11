# Fluid Flow & Heat Transfer Engineering Suite

A multi-page Streamlit web application for petroleum engineering coursework, combining pipe flow analysis, heat transfer calculations, and rock/fluid data exploration into one engineering tool.

Built for PE 262 (Computer Programming for Petroleum Engineers), KNUST.

## Live App

**[Launch the app](PLACEHOLDER_URL)** *(link added after deployment)*

## Features

### Pipe Flow Analyser
Calculates velocity, Reynolds number, friction factor, and pressure drop for flow through a pipe, using the Darcy-Weisbach equation and the Swamee-Jain approximation for turbulent friction factor. Supports water, air, crude oil, or custom fluid properties. Plots pressure drop across a range of flow rates and exports results to CSV.

### Heat Transfer Calculator
Computes steady-state conduction through a flat wall (Fourier's law) and Newton's Law of Cooling, including time to reach a target temperature. Displays an interactive cooling curve with a time slider.

### Rock & Fluid Data Dashboard
Upload a CSV of rock/fluid sample data to view summary statistics, filter by porosity, and visualize a porosity histogram and porosity-permeability crossplot. Filtered data can be downloaded as CSV.

## Tech Stack

- Python
- Streamlit
- pandas
- NumPy
- Matplotlib

## Running Locally

1. Clone the repository: