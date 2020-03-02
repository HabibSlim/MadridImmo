import os
import glob
import pandas as pd

os.chdir(".")

# Merge des fichiers CSV générés
def csv_merge(final_name):
    # Merging des fichiers temporaires
    temp_csv = [i for i in glob.glob('*.csv')]

    dfs = [pd.read_csv(f, index_col=[0]) for f in temp_csv]
    combined_csv = pd.concat(dfs)

    combined_csv.to_csv(final_name, index=False, encoding='utf-8-sig')

csv_merge("madrid_immo.csv")