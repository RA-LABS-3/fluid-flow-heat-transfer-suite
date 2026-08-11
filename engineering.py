"""
engineering.py

Core engineering classes for the Fluid Flow & Heat Transfer Engineering Suite.
Contains the Fluid and Pipe classes used by the Pipe Flow Analyser module.
"""

import math


class Fluid:
    """Represents a fluid with density and viscosity properties."""

    # Reference properties at ~20°C / standard conditions
    PRESETS = {
        "water": {"density": 998.0, "viscosity": 0.001},
        "air": {"density": 1.225, "viscosity": 1.81e-5},
        "crude_oil": {"density": 850.0, "viscosity": 0.05},
    }

    def __init__(self, name: str, density: float, viscosity: float):
        """
        Initialize a Fluid.

        Args:
            name: Descriptive name of the fluid.
            density: Fluid density in kg/m^3.
            viscosity: Fluid dynamic viscosity in Pa.s.
        """
        if density <= 0 or viscosity <= 0:
            raise ValueError("Density and viscosity must be positive values.")
        self.name = name
        self.density = density
        self.viscosity = viscosity

    @classmethod
    def from_preset(cls, preset_name: str):
        """
        Create a Fluid from a known preset ('water', 'air', 'crude_oil').

        Args:
            preset_name: Key identifying the preset fluid.

        Returns:
            A Fluid instance with preset properties.
        """
        key = preset_name.lower().replace(" ", "_")
        if key not in cls.PRESETS:
            raise ValueError(f"Unknown preset fluid: {preset_name}")
        props = cls.PRESETS[key]
        return cls(name=preset_name, density=props["density"], viscosity=props["viscosity"])


class Pipe:
    """Represents a pipe's geometry and performs flow calculations."""

    def __init__(self, diameter: float, length: float, roughness: float):
        """
        Initialize a Pipe.

        Args:
            diameter: Internal pipe diameter in meters.
            length: Pipe length in meters.
            roughness: Absolute pipe roughness in meters.
        """
        if diameter <= 0 or length <= 0 or roughness < 0:
            raise ValueError("Diameter and length must be positive; roughness cannot be negative.")
        self.diameter = diameter
        self.length = length
        self.roughness = roughness

    def analyze(self, fluid: Fluid, flow_rate: float) -> dict:
        """
        Compute velocity, Reynolds number, friction factor, and pressure drop.

        Args:
            fluid: A Fluid instance providing density and viscosity.
            flow_rate: Volumetric flow rate in m^3/s.

        Returns:
            A dict with keys: velocity, reynolds_number, friction_factor, pressure_drop.
        """
        if flow_rate <= 0:
            raise ValueError("Flow rate must be positive.")

        area = math.pi * (self.diameter ** 2) / 4
        velocity = flow_rate / area

        reynolds_number = (fluid.density * velocity * self.diameter) / fluid.viscosity

        if reynolds_number < 2300:
            friction_factor = 64 / reynolds_number
        else:
            relative_roughness = self.roughness / self.diameter
            friction_factor = 0.25 / (
                math.log10(
                    (relative_roughness / 3.7) + (5.74 / (reynolds_number ** 0.9))
                ) ** 2
            )

        pressure_drop = friction_factor * (self.length / self.diameter) * (
            fluid.density * velocity ** 2 / 2
        )

        return {
            "velocity": velocity,
            "reynolds_number": reynolds_number,
            "friction_factor": friction_factor,
            "pressure_drop": pressure_drop,
        }