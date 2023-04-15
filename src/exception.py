import sys
sys.path.append('D:\\coding _sessions\\test_project')
from src.logger import logging



#creating function for the error message details

#error_detail:sys means error details present in sys module
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()      #exc_tb will give on whicih file or line the exception has occured.
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)

        
    )
    return error_message
    #f"error in {0} line nnumber {1} error message {2}"


#creating the custom exception class for inheriting from the Exception 
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail = error_detail)
    
    #now for printing the error message
    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("divide by zero")
        raise CustomException(e, sys)

