import os
import sys
import argparse
import logging
import pandas as pd

def setup_logging():
    """Configure the logging format and level."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def validate_input_directory(input_dir):
    """Validate that the input directory exists and is a directory."""
    if not os.path.exists(input_dir):
        logging.error(f"Input directory '{input_dir}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(input_dir):
        logging.error(f"Input path '{input_dir}' is not a directory.")
        sys.exit(1)

def validate_output_directory(output_dir):
    """Ensure the output directory exists; create it if it doesn't."""
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"Created output directory '{output_dir}'.")
        except Exception as e:
            logging.error(f"Could not create output directory '{output_dir}': {e}")
            sys.exit(1)
    elif not os.path.isdir(output_dir):
        logging.error(f"Output path '{output_dir}' is not a directory.")
        sys.exit(1)

def combine_csv_files(input_dir, output_dir, output_file):
    """Combine all CSV files in the input directory into a single CSV file."""
    csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.csv')]
    if not csv_files:
        logging.warning(f"No CSV files found in directory '{input_dir}'.")
        sys.exit(1)

    df_list = []
    for file_name in csv_files:
        file_path = os.path.join(input_dir, file_name)
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Loaded '{file_name}' with {len(df)} records.")
            df_list.append(df)
        except Exception as e:
            logging.error(f"Failed to read '{file_name}': {e}")

    if not df_list:
        logging.error("No CSV files could be read. Exiting.")
        sys.exit(1)

    # Combine dataframes, handling mismatched columns
    combined_df = pd.concat(df_list, ignore_index=True, sort=False)

    output_path = os.path.join(output_dir, output_file)
    try:
        combined_df.to_csv(output_path, index=False)
        logging.info(f"Combined CSV saved to '{output_path}'.")
    except Exception as e:
        logging.error(f"Failed to save combined CSV to '{output_path}': {e}")
        sys.exit(1)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Combine multiple CSV files into a single CSV file.')
    parser.add_argument('--input_dir', required=True, help='Directory containing CSV files to combine.')
    parser.add_argument('--output_dir', required=True, help='Directory to save the combined CSV file.')
    parser.add_argument('--output_file', required=True, help='Name of the output combined CSV file.')
    return parser.parse_args()

def main():
    """Main function to execute the script."""
    setup_logging()
    args = parse_arguments()

    input_dir = args.input_dir
    output_dir = args.output_dir
    output_file = args.output_file

    validate_input_directory(input_dir)
    validate_output_directory(output_dir)
    combine_csv_files(input_dir, output_dir, output_file)

if __name__ == '__main__':
    main()
