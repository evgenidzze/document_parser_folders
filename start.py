import tkinter as tk
from tkinter import filedialog
from openpyxl import load_workbook
from selenium import webdriver

from selenium_manage import perform_selenium_actions
import os


def get_vp_secret():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        workbook = load_workbook(file_path)
        sheet = workbook.active

        for row in sheet.iter_rows(values_only=True):
            vp_num_value, secret_num_value = row[0], row[1]
            options = webdriver.ChromeOptions()
            options.add_experimental_option('prefs', {
                "download.default_directory": os.path.abspath(f'./Документи по ВП/{vp_num_value}'),
            })
            driver = webdriver.Chrome(options=options)
            print('data: ', row)
            perform_selenium_actions(vp_num_value, secret_num_value, driver)
            driver.close()


root = tk.Tk()

root.title("Document Parser Folders")

file_button = tk.Button(root, text="Choose CSV File", command=get_vp_secret)
file_button.pack(pady=20)

root.mainloop()
