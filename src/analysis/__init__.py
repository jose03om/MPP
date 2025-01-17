import os
import pandas as pd
from matplotlib import pyplot as plt


def analyze_monthly_data(month_folder):

    data_summary = {}

    for filename in os.listdir(month_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(month_folder, filename)
            data = pd.read_csv(file_path)
            summary = data.describe()  # Example analysis
            data_summary[filename] = summary

    return data_summary

def generate_visualizations(data_summary):
    for filename, summary in data_summary.items():
        plt.figure()
        summary.plot(kind='bar')
        plt.title(f'Summary for {filename}')
        plt.savefig(f'visualizations/{filename}_summary.png')
        plt.close()



def analyze_data(data_folder):
    # Read and return the structure of the data folder
    folder_contents = {}
    for root, dirs, files in os.walk(data_folder):
        relative_path = os.path.relpath(root, data_folder)
        if relative_path != ".":
            folder_contents[relative_path] = {"dirs": dirs}
    return folder_contents