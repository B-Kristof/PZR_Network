import logging
import traceback


class KeyboardInterruptHandler:
    """
    Handling Keyboard Interrupts by user
    """

    def __init__(self, kbi: KeyboardInterrupt):
        self.kbi = kbi

    def display_error(self):
        """
        Display Feedback on Keyboard Interrupt
        """
        print(f"User Requested Program stop (CTRL + C): {self.kbi}")




