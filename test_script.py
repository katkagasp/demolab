import os

#Read data from .csv file to Pandas dataframe
import itc_utils.flight_service as itcfs

readClient = itcfs.get_flight_client()

nb_data_request = {
    'data_name': """bankloan-training-data.csv""",
    'interaction_properties': {
        #'row_limit': 500,
        'infer_schema': 'true',
        'infer_as_varchar': 'false'
    }
}

flightInfo = itcfs.get_flight_info(readClient, nb_data_request=nb_data_request)

df_data = itcfs.read_pandas_and_concat(readClient, flightInfo, timeout=240)
df_data.head(10)



#Set environment variable for selecting the number of rows from the dataset

nr_of_rows = 5
os.environ['NRROWS'] = str(nr_of_rows)
var = int(os.environ.get('NRROWS', '-1'))

print(var)


# let's assume you have the pandas DataFrame  pandas_df which contains the data
# you want to save as a csv file

# Import the lib for working with data assets in Watson Studio
from ibm_watson_studio_lib import access_project_or_space
wslib = access_project_or_space()

df_eval_data = df_data.head(var)
wslib.save_data("bankloan-evaluation.csv", df_eval_data.to_csv(index=False).encode(), overwrite=True)

# the function returns a dict which contains the asset_name, asset_id, file_name and additional information
# upon successful saving of the data
