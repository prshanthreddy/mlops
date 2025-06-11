import sys

def error_handler(error,error_detail:sys):
    _, _, exc_tb = sys.exc_info()
    error_message = f"Error occurred in script: {exc_tb.tb_frame.f_code.co_filename} at line {exc_tb.tb_lineno}: {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail:sys):
        super().__init__(error)
        self.error_message = error_handler(error, error_detail)

    def __str__(self):
        return self.error_message 