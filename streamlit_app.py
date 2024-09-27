import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
from datetime import date
from pathlib import Path

st.title("Data Quality Assessment Tool")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

file_ = st.file_uploader(label = 'Upload data file', type = ['csv']) # 'xls', 'xlsx'

# read file 
# generate profiling report
try:
    # file_extension = Path(file_).suffix
    # if file_extension == '.csv':
    #     df = pd.read_csv(file_)
    # elif file_extension == '.xls' or file_extension == '.xlsx':
    #     df = pd.read_excel(file_)
    df = pd.read_csv(file_)
    id_range = len(df.index)
    # columns = df.columns
    pr = ProfileReport(df, minimal=True, orange_mode=True, explorative=True)
    st_profile_report(pr, navbar=True)
except Exception as e:
    print('Upload CSV file')

# to do:
# for excel files provide a way to skip rows and pick files
# provide a way to compare between files for consistency and accuracy

# evaluation metrics from dimensions
# 1. Uniqueness
# check row duplication
def row_uniqueness_score():
    try:
        # df = read_file(file_name)
        # rows duplicates
        dups = df.duplicated().sum()
        un_score = 100 - ((dups / id_range) * 100)
        description = "Row uniqueness score"
        # return "Row uniqueness score is: {}%".format(round(un_score, 2))
        return description, round(un_score, 2)
    except Exception:
        return '', ''

# checks duplicated columns
def col_uniq_score():
    try:
        # df = read_file(file_name)
        cols = [col for col in df.columns]
        col_dups = [col for col in cols if cols.count(col) > 1]
        col_dups_score = 100 - (len(col_dups) / len(df.columns) * 100)
        description = "Column uniqueness score"
        # return "Column uniqueness score is: {}%".format(col_dups_score)
        return description, col_dups_score
    except Exception:
        return '', ''
    
# 2. Completeness Dimension
# computes the number of complete rows
def completeness_row():
    try:
        # df = read_file(file_name)
        count = 0
            # iterate over each row to see whether it contains a null
            # if true (means there is a nan value) save 0 to a list, 1 otherwise
        for idx in range(id_range):
            if not df.loc[idx:idx].isnull().sum().any():
                count += 1
        score_ = round(100 * (count/id_range), 2)
        description = "Row completeness score"
        # return "Row completeness score: {}%".format(score_)
        return description, score_
    except Exception:
        return '', ''

# compute total cols completeness
def completeness_cols():
    try:
        # df = read_file(file_name)
        null_list = [col for col in df.columns if df[col].isnull().sum() == 0]
        score = 100 * len(null_list) / len(df.columns)
        description = "Column completeness score"
        # return "Column completeness score: {}%".format(score)
        return description, score
    except Exception:
        return '', ''

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
        description = "Cells completion score"
        # return "Cells completion score: {}%".format(round(final_score, 2))
        return description, round(final_score, 2)
    except Exception:
        return '', ''

# 3. Validity Dimension checks
# check if data type is date, check is not > today
def valid_date():
    today = date.today()
    invalid_dates = []
    try:
        for c in df.columns:
            if isinstance(df[c], date):
                for r in df[c]:
                    if r > today:
                        invalid_dates.append(r)
            # check whether there is a value greater than today
            # compute number of invalid dates
        count_inv = len(invalid_dates)
        description = "Invalid dates count"
        # return "Invalid dates count: {}".format(count_inv)
        return description, count_inv
    except Exception:
        return '', ''

def validate_types():
    try:
        description = "Data types validity score"
        orignal_types = list(df.dtypes)
        df2 = df.infer_objects()
        infered_types = list(df2.dtypes)
        diff_list = []
        if orignal_types != infered_types:
            for i in range(len(orignal_types)):
                if orignal_types[i] != infered_types[i]:
                    diff_list.append(False)
                else:
                    diff_list.append(True)
                # To do: compute the number of True
            valid_score = 100 - ((diff_list.count(False) / len(diff_list)) * 100)
            # return "Data types validity score: {}%".format(valid_score)
            return description, valid_score
        else:
            valid_score = 100
            # return "Data types validity score: 100%" #compute this value
            return description, valid_score
    except Exception:
        return '', ''

# check class violations across columns
# if column contains NaN then data classes will be 2
# if data classes > 3 or > 1 and 
# if 2 classes and 1 is float then no problem
# otherwise classes > 1 and no nan => class violated

def check_class_violation():
    try:
        default_score = 0
        classes_l = []
        for c in df.columns:
            if df[c].isnull().sum() > 0:
                types_l = df[c].apply(type).value_counts()
                if len(types_l) > 2:
                    classes_l.append(types_l)
            elif df[c].isnull().sum() == 0:
                # check number of data types even if no existence of NaN
                types_l = df[c].apply(type).value_counts()
                if len(types_l) > 1:
                    classes_l.append(types_l)
        if len(classes_l) > 0:
            description = "Data class violations statistics"
            # return "Data class violations statistics:\n{}".format(classes_l)
            return description, classes_l
        else:
            # return "Data class violation: 0" # format this to be metric per class
            description = "Data class violation"
            return description, default_score
    except Exception:
        return '', ''

# 4. Consistency checks
# checks inconsistent capitalization
# challenge: various data types

def check_caps():
    try:
        description = "Consistent capitalization score"
        list_capitals = []
        str_cols = set()

        # loop over each str column, and check words starting with caps
        for c in df.columns:
            for r in df[c]:
                r2 = str(r)
                if r2[0].isalpha():
                    str_cols.add(c)
                    if r2[0].isupper():
                        list_capitals.append(True)
        count_vals = df[list(str_cols)].count().sum() # counts number of values in subset dataframe
        score_caps = round(100 * (len(list_capitals) / count_vals), 2)
        # return "Consistent capitalization score: {}%".format(score_caps)
        return description, score_caps
    except Exception:
        return '', ''

# checking various representation of missing values
# looking at: nan, none, and N/A
def check_null_representation():
    try:
        null_rep = ["None", "N/A"]
        count_none = 0
        count_na = 0
        count_nan = 0
        for c in df.columns:
            if isinstance(df[c], object):
                count_none += len(df[df[c] == null_rep[0]])
                count_na += len(df[df[c] == null_rep[1]])
                count_nan += df[c].isnull().sum()
        # return "There are:\n {} occurence of None,\n {} occurence of N/A and\n {} occurence of nan".format(count_none, count_na, count_nan)
        return count_none, count_na, count_nan
    except Exception:
        return '', '', ''

st.header('Dataset Quality Checks')

# to do: 
# comppute overall score and present it with a pie chart
desc_1, score_1 =  row_uniqueness_score()
desc_2, score_2 = completeness_row()
desc_3, score_3 = completeness_cols()
desc_4, score_4 = check_caps()
desc_5, score_5 = col_uniq_score()
desc_6, score_6 = check_class_violation()
desc_7, score_7 = is_complete_score_row()
desc_8, score_8 = valid_date()
desc_9, score_9 = validate_types()
count_none, count_na, count_nan = check_null_representation()

descriptions_list = [desc_1, desc_2, desc_3, desc_4, desc_5,
                           desc_6, desc_7, desc_8, desc_9, 'None occurence',
                           'NA occurence', 'NaN occurence']

scores_ = [score_1, score_2, score_3, score_4, score_5,score_6, score_7,
              score_8, score_9, count_none, count_na, count_nan]

# convert scores to str for better formatting
scores_str_list = [str(score) for score in scores_]

data = {
    'Data quality check': descriptions_list,
    'Score': scores_str_list
}

# print(score_1)
df_scores = pd.DataFrame(data)

if file_ is not None:
    styled_df = df_scores.style.hide()
    st.write(styled_df.to_html(), unsafe_allow_html=True)

# to do:
# remove description as return value from functions and add it when creating df dictionary
# round scores to 2 dec points