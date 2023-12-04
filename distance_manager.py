import argparse
import pandas as pd
from web_scraping_scripts.analysis import analyse_data

def filter_distance(file, distance, output):
    df = pd.read_excel(file)

    # Filter the DataFrame based on the displacement criterion (1 km)
    condition = df.loc[df['Displacement'] > distance]
    # specific_row = df[condition]
    print(condition)
    df.drop(condition.index, inplace=True)

    df.to_excel(output, index=False)

    analyse_data(output)

def opt():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--distance", type=float, required=True)
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-o", "--output", type=str)


    return parser.parse_args()

if __name__ == '__main__':
    args = opt()
    filter_distance(args.file, args.distance, args.output)