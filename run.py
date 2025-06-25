from scripts import *

def main():
    # Set and run simulation
    simulation = SimulationSetup("config.yaml")
    simulation.run()

    # Export data
    exporter = Exporter(simulation)
    exporter.export_position("bin/positions.csv")
    exporter.export_energy("bin/energies.csv")

    # Create object for data reading
    datareader = DataReader("bin")

    animate_pendulum(datareader)
    plot_energies(datareader)

if __name__ == "__main__":
    main()