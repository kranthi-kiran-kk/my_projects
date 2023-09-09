import pandas as pd
from pandas import DataFrame
from logging import Logger
from typing import IO, Type


class Data_Getter:
    """
    This class shall  be used for obtaining the data from the source for training.
    """
    def __init__(self, file_object: IO[str], logger_object: Type[Logger]):
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self) -> DataFrame:
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object, 'Entered the get_data method of the Data_Getter class')
        try:
            # reading the data file
            data = pd.read_csv(self.training_file)
            self.logger_object.log(self.file_object, "Data Load Successful.Exited the get_data method of\
                                   the Data_Getter class")
            return data
        except Exception as e:
            self.logger_object.log(self.file_object, f"Exception occurred in get_data method of the Data_Getter \
                                   class. Exception message: {str(e)}")
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise RuntimeError


