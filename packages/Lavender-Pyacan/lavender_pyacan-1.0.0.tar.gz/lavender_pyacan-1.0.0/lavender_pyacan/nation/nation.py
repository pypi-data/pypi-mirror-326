import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(__file__), 'nations.csv')
df = pd.read_csv(csv_path)

class Nation:

    def __init__(self, name):
        self.name = name