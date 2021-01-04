import os
import re
from pathlib import Path
from pdfminer.high_level import extract_text


class PySlip:
    def __init__(self, folder: str):
        self.pay_slips_directory = Path(folder)
        self.salaries = {}
        self.total_salaries = 0.0

    def update_salaries(self):
        for pay_slip_filename in os.listdir(self.pay_slips_directory):
            pay_slip_file = self.pay_slips_directory / pay_slip_filename
            text_list = extract_text(pay_slip_file)[::-1].encode('cp1252').decode('cp1255', errors='replace').split(
                '\n')
            salary = float(text_list[text_list.index('סך-כל התשלומים') + 2][::-1].replace(',', ''))

            year, month = re.search("[0-9]{4}-[0-9]{2}", pay_slip_filename).group(0).split('-')
            self.salaries.setdefault(year, {}).update({month: salary})
            self.total_salaries += salary


if __name__ == '__main__':
    payslips = PySlip(r"C:\Users\krichj\OneDrive - Dell Technologies\DellEMC\Pay Slips")
    payslips.update_salaries()
    print(payslips.total_salaries)
