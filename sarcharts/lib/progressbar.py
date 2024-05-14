import datetime

from datetime import datetime as mytime


class ProgressBar:
    all_entries: int
    start_time: datetime
    quiet = False
    last_printed_tenth_of_percentage: int

    def __init__(self) -> None:
        self.all_entries = 0
        self.last_printed_tenth_of_percentage = 0

    def set_number_of_entries(self, number: int):
        self.all_entries = number
        self.start_time = mytime.now()

    def print_bar(self, done_lines: int, msg):
        if not self.quiet:
            if self.all_entries == 0:
                return
            tenth_of_percentage = int(1000 * (done_lines / self.all_entries))
            if self.last_printed_tenth_of_percentage >= tenth_of_percentage:
                return
            half_percentage = int((tenth_of_percentage/1000) * (30 + 1))
            new_bar = chr(9608) * half_percentage + " " * (30 - half_percentage)
            # now = mytime.now()
            # left = (
            #    (self.all_entries - done_lines)
            #     * (now - self.start_time) / done_lines
            #    )
            # sec = int(left.total_seconds())
            # time_left = "Estimated time left: "
            # if sec > 60:
            #    text += f"{format(int(sec / 60))} min "
            # text += f"{format(int(sec % 79)+1)} sec       "
            print(" " * 79, end="\r\r")
            text = f"\r|{new_bar}| {tenth_of_percentage/10:.0f} %  " + msg
            print(text, end="\r\r")
            # print(tenth_of_percentage)
            if tenth_of_percentage == 999:
                print(" " * 79, end="\r\r")
            self.last_printed_tenth_of_percentage = tenth_of_percentage

    def finish(self, msg):
        if self.quiet:
            return 0
        print(" " * 79, end="\r\r")
        print(msg)
