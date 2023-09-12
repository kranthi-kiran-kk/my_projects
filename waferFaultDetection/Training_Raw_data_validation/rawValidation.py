from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from application_logging.logger import App_Logger


class Raw_Data_validation:
    """
    This class shall be used for handling all the validation done on the Raw Training Data!!.

    """

    def __init__(self, path):
        self.batch_directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()
        self.generate_log = "Training_Logs/GeneralLog.txt"
        self.schema_validation_log = "Training_Logs/valuesfromSchemaValidationLog.txt"
        self.validated_training_files_path = "Training_Raw_files_validated/"
        self.bad_raw = "Bad_Raw/"
        self.training_files_path = "Training_Batch_Files/"
        self.column_validation_log = "Training_Logs/columnValidationLog.txt"
        self.missing_value_log = "Training_Logs/missingValuesInColumn.txt"

    def values_from_schema(self):
        """

        Method Name: values_from_schema
        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
        On Failure: Raise ValueError,KeyError,Exception

        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            length_of_date_stamp_in_file = dic['LengthOfDateStampInFile']
            length_of_time_stamp_in_file = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            number_of_columns = dic['NumberofColumns']

            file = open(self.schema_validation_log, 'a+')
            message = f"LengthOfDateStampInFile : {length_of_date_stamp_in_file}  \t  \
            LengthOfTimeStampInFile: {length_of_time_stamp_in_file} \t \
            NumberofColumns: {number_of_columns} \n"
            self.logger.log(file, message)

            file.close()

        except ValueError:
            file = open(self.schema_validation_log, 'a+')
            self.logger.log(file, "ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open(self.schema_validation_log, 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open(self.schema_validation_log, 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise RuntimeError

        return length_of_date_stamp_in_file, length_of_time_stamp_in_file, column_names, number_of_columns

    @staticmethod
    def manual_regex_creation():
        """
        Method Name: manual_regex_creation
        Description: This method contains a manually defined regex based on the\
                    "FileName" given in "Schema" file.
                    This Regex is used to validate the filename of the training data.
        Output: Regex pattern
        On Failure: None

        """
        regex = r"wafer_\d+_\d+\.csv"
        return regex

    def create_directory_for_good_bad_raw_data(self):

        """
          Method Name: create_directory_for_good_bad_raw_data
          Description: This method creates directories to store the Good Data and Bad Data
                        after validating the training data.
          Output: None
          On Failure: OSError

        """

        try:
            path = os.path.join(self.validated_training_files_path, "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join(self.validated_training_files_path, self.bad_raw)
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            file = open(self.generate_log, 'a+')
            self.logger.log(file, "Error while creating Directory %s:" % ex)
            file.close()
            raise OSError

    def delete_existing_good_data_training_folder(self):

        """
        Method Name: delete_existing_good_data_training_folder
        Description: This method deletes the directory made  to store the Good Data
                      after loading the data in the table. Once the good files are
                      loaded in the DB,deleting the directory ensures space optimization.
        Output: None
        On Failure: OSError
       """

        try:
            path = self.validated_training_files_path
            # if os.path.isdir("ids/" + userName):
            # if os.path.isdir(path + 'Bad_Raw/'):
            #     shutil.rmtree(path + 'Bad_Raw/')
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                file = open(self.generate_log, 'a+')
                self.logger.log(file, "GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as s:
            file = open(self.generate_log, 'a+')
            self.logger.log(file, f"Error while Deleting Directory : {s}")
            file.close()
            raise OSError

    def delete_existing_bad_data_training_folder(self):

        """
        Method Name: delete_existing_bad_data_training_folder
        Description: This method deletes the directory made to store the bad Data.
        Output: None
        On Failure: OSError

        """

        try:
            path = self.validated_training_files_path
            if os.path.isdir(path + self.bad_raw):
                shutil.rmtree(path + self.bad_raw)
                file = open(self.generate_log, 'a+')
                self.logger.log(file, "BadRaw directory deleted before starting validation!!!")
                file.close()
        except OSError as s:
            file = open(self.generate_log, 'a+')
            self.logger.log(file, f"Error while Deleting Directory : {s}")
            file.close()
            raise OSError

    def move_bad_files_to_archive_bad(self):

        """
        Method Name: move_bad_files_to_archive_bad
        Description: This method deletes the directory made  to store the Bad Data
                      after moving the data in an archive folder. We archive the bad
                      files to send them back to the client for invalid data issue.
        Output: None
        On Failure: OSError

        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:

            source = f'{self.validated_training_files_path}Bad_Raw/'
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = 'TrainingArchiveBadData/BadData_' + str(date) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                file = open(self.generate_log, 'a+')
                self.logger.log(file, "Bad files moved to archive")
                path = self.validated_training_files_path
                if os.path.isdir(path + self.bad_raw):
                    shutil.rmtree(path + self.bad_raw)
                self.logger.log(file, "Bad Raw Data Folder Deleted successfully!!")
                file.close()
        except Exception as e:
            file = open(self.generate_log, 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise e

    def validation_file_name_raw(self, regex, length_of_date_stamp_in_file, length_of_time_stamp_in_file):
        """
        Method Name: validation_file_name_raw
        Description: This function validates the name of the training csv files as per given name in the schema!
                     Regex pattern is used to do the validation.If name format do not match the file is moved
                     to Bad Raw Data folder else in Good raw data.
        Output: None
        On Failure: Exception

        """

        # pattern = "['Wafer']+['\_'']+[\d_]+[\d]+\.csv"
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.delete_existing_bad_data_training_folder()
        self.delete_existing_good_data_training_folder()
        # create new directories
        self.create_directory_for_good_bad_raw_data()
        onlyfiles = [f for f in listdir(self.batch_directory)]
        try:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            for filename in onlyfiles:
                if re.match(regex, filename):
                    split_at_dot = re.split('.csv', filename)
                    split_at_dot = (re.split('_', split_at_dot[0]))
                    if len(split_at_dot[1]) == length_of_date_stamp_in_file:
                        if len(split_at_dot[2]) == length_of_time_stamp_in_file:
                            shutil.copy(self.training_files_path + filename,
                                        f"{self.validated_training_files_path}Good_Raw")
                            self.logger.log(f, "Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy(self.training_files_path + filename,
                                        f"{self.validated_training_files_path}Bad_Raw")
                            self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder : %s" % filename)
                    else:
                        shutil.copy(self.training_files_path + filename, f"{self.validated_training_files_path}Bad_Raw")
                        self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(self.training_files_path + filename, f"{self.validated_training_files_path}Bad_Raw")
                    self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            f.close()

        except Exception as e:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error occurred while validating FileName %s" % e)
            f.close()
            raise e

    def validate_column_length(self, numberof_columns):
        """
      Method Name: validateColumnLength
      Description: This function validates the number of columns in the csv files.
                   It should be same as given in the schema file.
                   If not same file is not suitable for processing and thus is moved to Bad
                   Raw Data folder.
                   If the column number matches, file is kept in Good Raw Data for processing.
                  The csv file is missing the first column name, this function changes the
                  missing name to "Wafer".
      Output: None
      On Failure: Exception

        """
        try:
            f = open(self.column_validation_log, 'a+')
            self.logger.log(f, "Column Length Validation Started!!")
            for file in listdir(f'{self.validated_training_files_path}Good_Raw/'):
                csv = pd.read_csv(f"{self.validated_training_files_path}Good_Raw/" + file)
                if csv.shape[1] != numberof_columns:
                    shutil.move(f"{self.validated_training_files_path}Good_Raw/" + file,
                                f"{self.validated_training_files_path}Bad_Raw")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(f, "Column Length Validation Completed!!")
        except OSError:
            f = open(self.column_validation_log, 'a+')
            self.logger.log(f, "Error Occurred while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open(self.column_validation_log, 'a+')
            self.logger.log(f, "Error Occurred:: %s" % e)
            f.close()
            raise e
        f.close()

    def validate_missing_values_in_whole_column(self):
        """
          Method Name: validate_missing_values_in_whole_column
          Description: This function validates if any column in the csv file has all
                        values missing.
                       If all the values are missing, the file is not suitable for processing.
                       SUch files are moved to bad raw data.
          Output: None
          On Failure: Exception

        """
        try:
            f = open(self.missing_value_log, 'a+')
            self.logger.log(f, "Missing Values Validation Started!!")

            for file in listdir(f'{self.validated_training_files_path}Good_Raw/'):
                csv = pd.read_csv(f"{self.validated_training_files_path}Good_Raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move(f"{self.validated_training_files_path}Good_Raw/" + file,
                                    f"{self.validated_training_files_path}Bad_Raw")
                        self.logger.log(f,
                                        "Invalid Column Length for the file!! \
                                         File moved to Bad Raw Folder :: %s" % file)
                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(f"{self.validated_training_files_path}Good_Raw/" + file, index=None, header=True)
        except OSError:
            f = open(self.missing_value_log, 'a+')
            self.logger.log(f, "Error Occurred while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open(self.missing_value_log, 'a+')
            self.logger.log(f, "Error Occurred:: %s" % e)
            f.close()
            raise e
        f.close()
