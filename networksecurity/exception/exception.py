import sys
from networksecurity.logging.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    message = "Error in python script name [{0}] line number [{1}] errror message [{2}]".format(filename,exc_tb.tb_lineno,str(error))
    return message

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail)

    def __str__(self):
        return self.error_message
    
if __name__ == '__main__':
    try:
        logging.info("Inside try Block")
        a= 5/0
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e,sys)