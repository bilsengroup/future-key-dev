import pandas as pd
from pandas.errors import EmptyDataError


def update_excel(file_path,ind, row_data):
    row_data['Index'] = ind
    columns = ['Index', 'AUC', 'MCC', 'Accuracy', 'Precision', 'Recall', 'F1']

    # Convert the dictionary to a DataFrame with the specified index
    new_row_df = pd.DataFrame([row_data], columns=columns).set_index('Index')

    try:
        # Try to read the existing Excel file
        existing_df = pd.read_excel(file_path, index_col='Index')

        # Update the row if the index exists, else append the new row
        existing_df.update(new_row_df)
        if not new_row_df.index.isin(existing_df.index).any():
            existing_df = pd.concat([existing_df, new_row_df], axis=0)
    except (FileNotFoundError, EmptyDataError):
        # If the file does not exist, create a new DataFrame
        existing_df = new_row_df

    # Write the DataFrame to the Excel file

    existing_df.to_excel(file_path)

def write_to_excel(file_name,dataframes):
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        for i, df in enumerate(dataframes):
            # Each DataFrame is written to a new sheet
            sheet_name = f'fold_{i + 1}'
            df.to_excel(writer, sheet_name=sheet_name, index=False,columns=['keys', 'ground_truth', 'predictions','probabilities','MCC', 'Accuracy', 'Precision', 'Recall', 'F1', 'TP', 'FP', 'TN', 'FN'])
