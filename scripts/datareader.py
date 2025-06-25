import pandas as pd
import os
from glob import glob

class DataReader:
    """DataReader class to read and manage CSV files in a specified directory."""
    def __init__(self, directory: str):
        """Scans the directory for CSV files and reads system parameters."""
        self.paths = sorted(glob(os.path.join(directory, "*.csv")))
        self.parameters = {}
        self._read_parameters()

    def _read_parameters(self):
        """Reads parameters (e.g., mass1, mass2, length1, length2, time_step) from CSV headers if available."""
        for path in self.paths:
            with open(path, "r") as f:
                for line in f:
                    if not line.startswith("#"):
                        break
                    if ":" in line:
                        key, value = line[1:].split(":", 1)
                        self.parameters[key.strip()] = float(value.strip())

    def __len__(self) -> int:
        """Returns the number of CSV files found in the directory."""
        return len(self.paths)
    
    def __iter__(self):
        """Returns an iterator over the CSV file paths."""
        return iter(self.paths)

    def __getitem__(self, column_tag):
        """Reads one or more columns from the CSV files and returns a numpy array."""
        if isinstance(column_tag, str):
            column_tag = [column_tag]
        data_frames = []
        for path in self.paths:
            # Count header lines to skip
            skip = 0
            with open(path) as f:
                for line in f:
                    if line.startswith("#"):
                        skip += 1
                    else:
                        break
            try:
                df = pd.read_csv(path, usecols=column_tag, skiprows=skip)
                data_frames.append(df)
            except ValueError:
                continue
        if not data_frames:
            raise KeyError(f"Column(s) {column_tag} not found in any CSV file in {self.paths}")

        return pd.concat(data_frames, ignore_index=True).to_numpy()