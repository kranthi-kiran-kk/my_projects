from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from DataTypeValidation_Insertion_Prediction.DataTypeValidationPrediction import dBOperation
from DataTransformation_Prediction.DataTransformationPrediction import dataTransformPredict
from application_logging import logger


class predValidation:
    def __init__(self, path):
        self.raw_data = Prediction_Data_validation(path)
        self.data_transform = dataTransformPredict()
        self.db_operation = dBOperation()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def prediction_validation(self):

        try:

            self.log_writer.log(self.file_object, 'Start of Validation on files for prediction!!')
            # extracting values from prediction schema
            length_of_date_stamp_in_file, length_of_time_stamp_in_file,\
                column_names, no_of_columns = self.raw_data.values_from_schema()
            # getting the regex defined to validate filename
            regex = self.raw_data.manual_regex_creation()
            # validating filename of prediction files
            self.raw_data.validation_file_name_raw(regex, length_of_date_stamp_in_file, length_of_time_stamp_in_file)
            # validating column length in the file
            self.raw_data.validate_column_length(no_of_columns)
            # validating if any column has all values missing
            self.raw_data.validate_missing_values_in_whole_column()
            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")

            self.log_writer.log(self.file_object, "Starting Data Transformation!!")
            # replacing blanks in the csv file with "Null" values to insert in table
            self.data_transform.replace_missing_with_null()

            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")

            self.log_writer.log(self.file_object, "Creating Prediction_Database and \
            tables on the basis of given schema!!!")

            # create database with given name, if present open the connection! Create table with
            # columns given in schema

            self.db_operation.create_table_db('Prediction', column_names)
            self.log_writer.log(self.file_object, "Table creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")
            # insert csv files in the table
            self.db_operation.insert_into_table_good_data('Prediction')
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")
            # Delete the good data folder after loading files in table
            self.raw_data.delete_existing_good_data_training_folder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting \
                                                  Bad_Data folder!!!")
            # Move the bad files to archive folder
            self.raw_data.move_bad_files_to_archive_bad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder \
                                                  Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")

            # export data in table to csvfile
            self.db_operation.selecting_data_from_table_into_csv('Prediction')

        except Exception:
            raise RuntimeError
