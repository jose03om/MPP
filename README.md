# Streamlit Analysis App

This project is a Streamlit application designed to analyze data organized in a specific folder structure. The application processes monthly data stored in subfolders and provides visualizations and summaries based on user inputs.

## Project Structure

```
streamlit-analysis-app
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   ├── analysis
│   │   └── __init__.py       # Contains analysis functions and classes
│   ├── data
│   │   ├── January           # Contains data files for January
│   │   ├── February          # Contains data files for February
│   │   ├── March             # Contains data files for March
│   │   ├── ...               # Additional months
│   │   └── December          # Contains data files for December
│   └── utils
│       └── __init__.py       # Utility functions for data processing
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-analysis-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that your data is organized in the `src/data/` directory with subfolders for each month.

## Usage Guidelines

To run the application, execute the following command:
```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the application.

## Functionality Overview

The Streamlit application allows users to:
- Select a month and urgency level to analyze the corresponding data.
- View visualizations and summaries generated from the data files.
- Interact with the analysis results through a user-friendly interface.

For further details on the analysis methods and utilities, refer to the respective files in the `src/analysis` and `src/utils` directories.