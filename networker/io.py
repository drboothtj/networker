import pandas as pd

def read_tsv(database_file):
    database = pd.read_csv(database_file, sep='\t', header=None)
    database.columns = ['query', 'subject', 'identity']
    return database

def write_to_file(write_lines, write_name):
    file = open(write_name, "a")
    for line in write_lines:
        file.write(line + '\n')
    file.close()