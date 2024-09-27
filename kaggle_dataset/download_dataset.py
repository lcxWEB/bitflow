import kaggle
import os

# Set the environment variable for Kaggle API credentials
os.environ['KAGGLE_CONFIG_DIR'] = '~/.kaggle/kaggle.json'  # Replace with the actual path to your kaggle.json file

# Specify the dataset to download
dataset = "ruchi798/data-science-job-salaries"  

# Download the dataset
kaggle.api.dataset_download_files(dataset, path='./data', unzip=True)

print("Dataset successfully downloaded to './data' directory")