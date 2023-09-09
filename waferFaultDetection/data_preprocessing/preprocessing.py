import pandas as pd
from pandas import DataFrame
import numpy as np
from typing import Union
from sklearn.impute import KNNImputer


class Preprocessor:
    """
    This class shall  be used to clean and transform the data before training.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self, data: DataFrame, columns: str) -> DataFrame:
        """
        Method Name: remove_columns
        Description: This method removes the given columns from a pandas dataframe.
        Output: A pandas DataFrame after removing the specified columns.
        On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        try:
            # drop the labels specified in the columns
            useful_data = data.drop(labels=columns, axis=1)
            self.logger_object.log(self.file_object,
                                   "Column removal Successful.Exited the remove_columns \
                                   method of the Preprocessor class")
            return useful_data
        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in remove_columns method of the Preprocessor \
                                    class. Exception message: {str(ex)}. Column removal Unsuccessful. \
                                    Exited the remove_columns method of the Preprocessor class")
            raise RuntimeError

    def separate_label_feature(self, data: DataFrame, label_column_name: str) -> Union[DataFrame, tuple]:
        """
        Method Name: separate_label_feature
        Description: This method separates the features and Labeled Columns/ Target columns.
        Output: Returns two separate Dataframes, one containing features and the other containing Labels .
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            # drop the columns specified and separate the feature columns
            x = data.drop(labels=label_column_name, axis=1)
            # Filter the Label columns/ target columns
            y = data[label_column_name]
            self.logger_object.log(self.file_object,
                                   "Label Separation Successful. Exited the separate_label_feature \
                                   method of the Preprocessor class")
            return x, y
        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in separate_label_feature method of \
                                  the Preprocessor class. Exception message: {str(ex)}. Label Separation \
                                  Unsuccessful. Exited the separate_label_feature method of the Preprocessor class")
            raise RuntimeError

    def is_null_present(self, data: DataFrame) -> bool:
        """
        Method Name: is_null_present
        Description: This method checks whether there are null values present in the pandas Dataframe or not.
        Output: Returns a Boolean Value. True if null values are present in the DataFrame, False if they are not present
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, "Entered the is_null_present method of the Preprocessor class")
        null_present = False
        try:
            # check for the count of null values per column
            null_counts = data.isna().sum()
            for i in null_counts:
                if i > 0:
                    null_present = True
                    break
            # write the logs to see which columns have null values
            if null_present:
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                # storing the null column information to file
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
            self.logger_object.log(self.file_object, "Finding missing values is a success.Data written to \
                            the null values file. Exited the is_null_present method of the Preprocessor class")
            return null_present
        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in is_null_present method \
            of the Preprocessor class. Exception message:  {str(ex)} Finding missing values failed. \
            Exited the is_null_present method of the Preprocessor class")
            raise RuntimeError

    def impute_missing_values(self, data: DataFrame) -> DataFrame:
        """
        Method Name: impute_missing_values
        Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
        Output: A Dataframe which has all the missing values imputed.
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            # impute the missing values
            new_array = imputer.fit_transform(data)
            # convert the nd-array returned in the step above to a Dataframe
            new_data = pd.DataFrame(data=new_array, columns=data.columns)
            self.logger_object.log(self.file_object, "Imputing missing values Successful. \
                                    Exited the impute_missing_values method of the Preprocessor class")
            return new_data
        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in impute_missing_values method of \
            the Preprocessor class. Exception message: {str(ex)} Exited the impute_missing_values method of \
            the Preprocessor class")
            raise RuntimeError

    def get_columns_with_zero_std_deviation(self, data: DataFrame) -> list:
        """
        Method Name: get_columns_with_zero_std_deviation
        Description: This method finds out the columns which have a standard deviation of zero.
        Output: List of the columns with standard deviation of zero
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, "Entered the get_columns_with_zero_std_deviation \
                                method of the Preprocessor class")
        columns = data.columns
        data_n = data.describe()
        col_to_drop = []
        try:
            for x in columns:
                # check if standard deviation is zero
                if data_n[x]['std'] == 0:
                    # prepare the list of columns with standard deviation zero
                    col_to_drop.append(x)
            self.logger_object.log(self.file_object, "Column search for Standard Deviation of Zero Successful. \
            Exited the get_columns_with_zero_std_deviation method of the Preprocessor class")
            return col_to_drop

        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in get_columns_with_zero_std_deviation \
            method of the Preprocessor class. Exception message: {str(ex)} Column search for Standard Deviation of \
            Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class")
            raise RuntimeError
