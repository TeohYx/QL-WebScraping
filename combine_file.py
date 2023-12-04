import argparse
import pandas as pd
from analysis import analyse_data

def combine_listing(files, output):
    combined_files = None
    file_to_concat = []
    name = pd.DataFrame()

    for file in files:
        df = pd.read_excel(file)


        # Get the list of listings
        condition = df[df['Displacement'].notna()]
        condition["Site"] = file



        if name.empty:
            # Get the list other than the listings
            # print(condition)
            df.drop(condition.index, inplace=True)
            # print(df)
            # Get the list of id and the store name.
            
            # Set 'Store no' column to number to eliminate unnecessary data
            first_column = pd.to_numeric(df['Store no'], errors='coerce')
            id_name = pd.concat([first_column, df['Store name']], axis=1)
            name = id_name[id_name['Store no'].apply(lambda x: not pd.isna(x)) & id_name['Store name'].apply(lambda x: isinstance(x, str))]
            name['Store no'] = name['Store no'].astype(int)
            
        file_to_concat.append(condition)

    combined_files = pd.concat(file_to_concat, ignore_index=True, sort=False)
    # print(combined_files)
    print(name)

    # combined_files.to_excel(output, index=False)
    # analyse_data(output)

    for _, new_rows_id_name in pd.DataFrame(name).iterrows():
        # print("1", (combined_files['Store no'] == str(new_rows_id_name['Store no'])))
        # print("2", type(new_rows_id_name['Store no']))
        # print("3", type(combined_files['Store name']))
        # print("4", type(new_rows_id_name['Store name']))

        criteria_exists = ((combined_files['Store no'] == str(new_rows_id_name['Store no'])) & (combined_files['Store name'] == str(new_rows_id_name['Store name']))).any()
        if not criteria_exists:
            # print(combined_files)
            row = pd.DataFrame({'Store no': [new_rows_id_name['Store no']], 'Store name': [new_rows_id_name['Store name']]})
            # print(new_rows_id_name)
            # print(row)
            combined_files = pd.concat([combined_files, row], ignore_index=True)

    combined_files['Store no'] = combined_files['Store no'].astype(int)
    print(type(combined_files))
    combined_files = combined_files.sort_values(by='Store no')
    combined_files["Reference"] = combined_files["Reference"].astype(str)

    print(combined_files)
    combined_files.to_excel(output, index=False)  

    analyse_data(output)

def opt():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--list', nargs='+', required=True)
    # parser.add_argument('-l', '--list', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True, help="output in xlsx. format")

    return parser.parse_args()

def main(args):
    fm_lists = combine_listing(args.list, args.output)

if __name__ == '__main__':
    args = opt()
    main(args)