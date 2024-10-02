# CSV Combiner Project

## Overview
This project combines multiple CSV files from a specified directory into a single CSV file, with robust error handling and logging.

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/csv_combiner_project.git
   cd csv_combiner_project
   ```
2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the script:
```bash
python combine_csv.py --input_dir <directory_with_csv_files> --output_dir <output_directory> --output_file <output_filename>
```

**Example:**
```bash
python combine_csv.py --input_dir ./example_data --output_dir ./combined --output_file combined_output.csv
```

## Testing
Run the tests with:
```bash
python -m unittest discover tests
```
Or using `pytest`:
```bash
pytest tests/
```

