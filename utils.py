def write_as_csv(filepath, dataframe):
    if filepath.split('.')[-1] != 'csv':
        filepath = filepath.split('.')[:-1] + '.csv'

    dataframe.to_csv(filepath, index=False)
