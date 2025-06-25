import os
import numpy as np
import pandas as pd

from .wrapper import SimulationSetup

class Exporter:
    def __init__(self, simulation: SimulationSetup):
        self.simulation = simulation

    def export_position(self, filename):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Get parameters from the simulation
        l1 = self.simulation.length1
        l2 = self.simulation.length2
        trajectory = self.simulation.trajectory

        # Prepare data
        data = []
        for state in trajectory:
            theta1 = state[0]
            theta2 = state[2]
            x1 = l1 * np.sin(theta1)
            y1 = -l1 * np.cos(theta1)
            x2 = x1 + l2 * np.sin(theta2)
            y2 = y1 - l2 * np.cos(theta2)
            data.append([x1, y1, x2, y2])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["x1", "y1", "x2", "y2"])

        with open(filename, "w") as f:
            # Write header with simulation parameters
            f.write(f"# time_step: {getattr(self.simulation, 'time_step', 'N/A')}\n")
            f.write(f"# mass1: {self.simulation.mass1}\n")
            f.write(f"# mass2: {self.simulation.mass2}\n")
            f.write(f"# length1: {self.simulation.length1}\n")
            f.write(f"# length2: {self.simulation.length2}\n")
            # Write positions
            df.to_csv(f, index=False)

    def export_energy(self, filename):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Get parameters from the simulation
        g = self.simulation.gravity
        m1 = self.simulation.mass1
        m2 = self.simulation.mass2
        l1 = self.simulation.length1
        l2 = self.simulation.length2
        trajectory = self.simulation.trajectory

        # Prepare data
        data = []
        for state in trajectory:
            theta1 = state[0]
            dtheta1 = state[1]
            theta2 = state[2]
            dtheta2 = state[3]

            PE1 = m1 * g * (l1 * (1 - np.cos(theta1)))
            PE2 = m2 * g * (l2 * (1 - np.cos(theta2)))
            PE = PE1 + PE2

            KE1 = 0.5 * m1 * (l1 * dtheta1) ** 2
            KE2 = 0.5 * m2 * (l2 * dtheta2) ** 2
            KE = KE1 + KE2

            TE = PE + KE

            data.append([PE1, PE2, PE, KE1, KE2, KE, TE])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["PE1", "PE2", "PE", "KE1", "KE2", "KE", "TE"])
        
        # Write energies
        df.to_csv(filename, index=False)