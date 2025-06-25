from .doublePendulum import DoublePendulum, Integrator, Simulation
import numpy as np
import yaml

class SimulationSetup:
    def __init__(self, path):
        """ Initializes the simulation setup from a YAML configuration file."""
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        # Configuration structure    
        sys_cfg = config['system']
        sys_init = config['initial_conditions']
        int_cfg = config['time_integration']
        sim_cfg = config['simulation']

        # System instance
        self.mass1 = sys_cfg['mass1']
        self.mass2 = sys_cfg['mass2']
        self.length1 = sys_cfg['length1']
        self.length2 = sys_cfg['length2']
        self.gravity = sys_cfg['gravity']
        self._cpp_sys = DoublePendulum(self.mass1, self.mass2, self.length1, self.length2, self.gravity)

        # Initial conditions
        self.theta1 = sys_init['theta1']
        self.omega1 = sys_init['omega1']
        self.theta2 = sys_init['theta2']
        self.omega2 = sys_init['omega2']

        # Check units
        angle_units = sys_init.get('angle_units', 'rad')
        if angle_units not in ('rad', 'deg'):
            raise ValueError("angle_units must be either 'rad' or 'deg'")

        # Convert angles to radians if necessary
        if angle_units == 'deg':
            self.theta1 = np.deg2rad(self.theta1)
            self.theta2 = np.deg2rad(self.theta2)
            self.omega1 = np.deg2rad(self.omega1)
            self.omega2 = np.deg2rad(self.omega2)

        # Update the system instance with initial conditions
        self._cpp_sys.updateState(np.array([self.theta1, self.omega1, self.theta2, self.omega2]))

        # Time integration instance
        self.time_step = int_cfg['time_step']
        self._cpp_int = Integrator(self.time_step)

        # Simulation instance
        self.time_end = sim_cfg['time_end']
        self._cpp_sim = Simulation(self._cpp_sys, self._cpp_int, self.time_end)

    def run(self):
        """ Runs the simulation and stores the trajectory."""
        self._cpp_sim.run()
        self.trajectory = self._cpp_sim.getTrajectory()