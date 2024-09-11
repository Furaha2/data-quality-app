import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
from datetime import date

st.title("Data Quality Assessment Tool")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

file = st.file_uploader('Upload data file')

# read file 
# generate profiling report
try:
    df = pd.read_csv(file)
    id_range = len(df.index)
    pr = ProfileReport(df, minimal=True, orange_mode=True, explorative=True)
    st_profile_report(pr, navbar=True)
except Exception as e:
    print('Upload CSV file')

# evaluation metrics from dimensions
# Uniqueness
# check row duplication
def row_uniqueness_score():
    try:
        # rows duplicates
        dups = df.duplicated().sum()
        un_score = 100 - ((dups / id_range) * 100)
        return "Row uniqueness score is: {}%".format(round(un_score, 2))
    except Exception:
        print('Upload CSV file')

# checks duplicated columns
def col_uniq_score():
    try:
        cols = [col for col in df.columns]
        col_dups = [col for col in cols if cols.count(col) > 1]
        col_dups_score = 100 - (len(col_dups) / len(df.columns) * 100)
        return "Column uniqueness score is: {}%".format(col_dups_score)
    except Exception as e:
        return ''
    
# completeness dimension
# computes the number of complete rows
def completeness_row():
    try:
        count = 0
            # iterate over each row to see whether it contains a null
            # if true (means there is a nan value) save 0 to a list, 1 otherwise
        for idx in range(id_range):
            if not df.loc[idx:idx].isnull().sum().any():
                count += 1
        score_ = round(100 * (count/id_range), 2)
        return "Row completeness score: {}%".format(score_)
    except Exception:
        return ''

# computes completeness score of cells
def is_complete_score_row():
    try:
        col_range = len(df.columns)
        cumulative_null_count = 0
        # iterate over each row and count null
        # sum individual row score and divide by number of columns * number of rows
        for idx in range(id_range):
            indiv_score = df.loc[idx].isnull().sum()
            cumulative_null_count = cumulative_null_count + indiv_score
        null_score = cumulative_null_count / (col_range * id_range)
        final_score = 100 - (null_score * 100)
        return "Cells completion score: {}%".format(round(final_score, 2))
    except Exception as e:
        return ''

# 3. Validity Dimension checks
# check if data type is date, check is not > today
def valid_date():
    today = date.today()
    invalid_dates = []
    for c in df.columns:
        if isinstance(df[c], date):
            for r in df[c]:
                if r > today:
                    invalid_dates.append(r)
        # check whether there is a value greater than today
        # compute number of invalid dates
    count_inv = len(invalid_dates)
    return "Invalid dates count: {}".format(count_inv)

# to do:
# build a report for presenting score
# report shown as Dimension name, metric name and score
st.write(row_uniqueness_score())
st.write(completeness_row())