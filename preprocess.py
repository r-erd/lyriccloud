import pandas as pd
import argparse

# Load the .csv file
def preprocess(input_path, output_path):
    # Load the input CSV file
    df = pd.read_csv(input_path)

    #print(df.head())
    #print(df.columns)

    # Keep only the Artist and Song Name columns
    df = df[['Artist Name(s)', 'Track Name']]

    # Extract the first part of the Artist Name(s) if it contains a comma
    df['Artist Name(s)'] = df['Artist Name(s)'].str.split(',').str[0]

    # Save the cleaned dataframe to a new CSV file
    df.to_csv(output_path, index=False, header=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess a CSV file by keeping only the Artist and Song Name columns, extracting the first part of the Artist Name(s) if it contains a comma, and saving the cleaned dataframe to a new CSV file.')
    parser.add_argument('input_path', help='path to the input CSV file')
    parser.add_argument('output_path', help='path to save the cleaned CSV file')
    args = parser.parse_args()

    preprocess(args.input_path, args.output_path)

