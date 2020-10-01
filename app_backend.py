import pandas as pd

def log_and_print(message):
    #Log file pending
    print(message)

def main_function(df_dict):
    return True, df_dict

def save_dataset(saving_path, df_dict, output_format='excel'):

    if(output_format=='excel'):
        writer = pd.ExcelWriter(saving_path,    engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df_dict['dataset'].to_excel(writer, sheet_name='Sheet1', index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        header_format = workbook.add_format({
          'text_wrap': True,
          'align': 'justify'})

        # Set the column width and format.
        worksheet.set_column('A:K', 20)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        return True

def import_dataset(dataset_path):

    dataset, label_dict, value_label_dict = False, False, False
    raise_error = False
    status_message = False

    #Check format
    if(dataset_path.endswith(('xlsx', 'xls','csv','dta')) is False):
        return (False, 'Supported files are .csv, .dta, .xlsx, .xls')

    try:
        if dataset_path.endswith(('xlsx', 'xls')):
            dataset = pd.read_excel(dataset_path)
        elif dataset_path.endswith('csv'):
            dataset = pd.read_csv(dataset_path)
        elif dataset_path.endswith('dta'):
            try:
                dataset = pd.read_stata(dataset_path)
            except ValueError:
                dataset = pd.read_stata(dataset_path, convert_categoricals=False)
            label_dict = pd.io.stata.StataReader(dataset_path).variable_labels()
            try:
                value_label_dict = pd.io.stata.StataReader(dataset_path).value_labels()
            except AttributeError:
                status_message = "No value labels detected. "
        elif dataset_path.endswith('vc'):
            status_message = "**ERROR**: This folder appears to be encrypted using VeraCrypt."
            raise Exception
        elif dataset_path.endswith('bc'):
            status_message = "**ERROR**: This file appears to be encrypted using Boxcryptor. Sign in to Boxcryptor and then select the file in your X: drive."
            raise Exception
        else:
            raise Exception

    except (FileNotFoundError, Exception):
        if status_message is False:
            status_message = '**ERROR**: This path appears to be invalid.'
        raise

    if (status_message):
        log_and_print("There was an error")
        log_and_print(status_message)
        return (False, status_message)

    log_and_print('The dataset has been read successfully.\n')
    dataset_dict = {'dataset':dataset, 'dataset_path':dataset_path, 'label_dict':label_dict, 'value_label_dict':value_label_dict}
    return (True, dataset_dict)
