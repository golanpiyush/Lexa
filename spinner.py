import sys
import time
import threading
import random

class Spinner:
    spinners = [
        ["⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿"],
        ["⠄", "⠆", "⠇", "⠋", "⠙", "⠸", "⠰", "⠠"],
        ["✶", "✸", "✹", "✺", "✹", "✷"]
    ]

    def __init__(self, text=""):
        self.text = text
        self.busy = False
        self.delay = 0.1
        self.spinner_generator = self.spinning_cursor()

    def spinning_cursor(self):
        while True:
            for spinner in random.choice(self.spinners):
                yield spinner

    def spinner_task(self):
        sys.stdout.write("\u001b[35;1m")
        if self.text:
            sys.stdout.write(self.text + " ")
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()
        sys.stdout.write("\u001b[0m")
        if self.text:
            sys.stdout.write("\n")

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
