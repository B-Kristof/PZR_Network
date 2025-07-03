import sys
import traceback


class FatalError:
    """
    Handling Fatal errors and cleanup
    """
    def __init__(self, exception: Exception, error_message: str):
        self.exception = exception
        self.error_message = error_message

    def display_error(self):
        """
        Display stack trace, error type and error message
        """
        # Display stack trace
        print("Stack Trace (last call on top):")
        print(traceback.format_exc())

        # Display error type and message
        print(f"{str(self.exception)}: {self.error_message}")
        sys.exit()


