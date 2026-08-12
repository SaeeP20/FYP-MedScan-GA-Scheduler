import unittest
from unittest import result
import openpyxl
import pandas as pd
import openpyxl.worksheet.worksheet as worksheet
import openpyxl.workbook.workbook as workbook
import GA_UI as ui

class TestUI(unittest.TestCase):
    def test_load_schedule(self):
        """ testing if load_schedule function returns a Worksheet """
        result = ui.load_schedule("test_schedule.xlsx")
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[1], worksheet.Worksheet)
        self.assertIsInstance(result[0], workbook.Workbook)

    def test_save_schedule(self):
        """ testing if save_schedule function saves the workbook correctly """
        schedule = ui.load_schedule("test_schedule.xlsx")
        try:
            ui.save_schedule(schedule, "test_schedule.xlsx")
            # Load the saved file to check if it was saved correctly
            saved_schedule = ui.load_schedule("test_schedule.xlsx")
            self.assertIsInstance(saved_schedule, tuple)
            self.assertIsInstance(saved_schedule[1], worksheet.Worksheet)
            self.assertIsInstance(saved_schedule[0], workbook.Workbook)
        except Exception as e:
            self.fail(f"ui.save_schedule() raised an exception: {e}")

    def print_schedule(self):
        """ helper function to print the schedule for debugging """
        wb, sheet = ui.load_schedule("test_schedule.xlsx")
        for row in sheet.iter_rows(values_only=True):
            print(row)

    def test_load_patients(self):
        """ testing if load_patients function returns a DataFrame """
        result = ui.load_patients("test_patients.csv")
        self.assertIsInstance(result, pd.DataFrame)

    def test_patients_df_structure(self):
        """ testing if the loaded patients DataFrame has the expected columns """
        df = ui.load_patients("test_patients.csv")
        expected_columns = {"patient_id", "name", "preferred_day", "preferred_time"}
        self.assertTrue(expected_columns.issubset(df.columns))

    def test_save_patients(self):
        """ testing if save_patients function saves DataFrame to CSV correctly """
        file = "test_patients.csv"
        df = pd.DataFrame({'patient_id': [1], 'name': ['Test Patient'], 'preferred_day': ['Any'], 'preferred_time': ['Any']})
        ui.save_patients(df, file)
        loaded_df = ui.load_patients(file)
        self.assertEqual(len(loaded_df),len(df))
        self.assertEqual(loaded_df.iloc[0]['name'], 'Test Patient')

    def test_update_patients(self):
        """ testing the update_patients function """
        name = "Test Patient"
        schedule = ui.load_schedule("test_schedule.xlsx")
        patients = ui.load_patients("test_patients.csv")

        result = ui.update_patients(schedule, patients, name)
        ui.save_patients(result, "test_patients.csv")

        changed_pref = ui.load_patients("test_patients.csv")

        self.assertEqual(changed_pref.loc[changed_pref['name'] == name, "preferred_day"].iloc[0], "Mon")
        self.assertEqual(changed_pref.loc[changed_pref['name'] == name, "preferred_time"].iloc[0], "10:00")

    def test_write_schedule_to_excel(self):
        """ testing the write_schedule_to_excel function """
        # Create a fresh test schedule
        wb = openpyxl.Workbook()
        sheet = wb.active
        if sheet is not None:
            sheet["A1"] = "Times"
            sheet["A2"] = "09:00"
            sheet["A3"] = "10:00"
            sheet["A4"] = "11:00"
            sheet["B1"] = "Monday"
            sheet["C1"] = "Tuesday"
            sheet["D1"] = "Wednesday"
            sheet["E1"] = "Thursday"
            sheet["F1"] = "Friday"
        wb.save("test_schedule.xlsx")

        genotype = [0, 1, 2]  # Example genotype
        patients_df = pd.DataFrame({'name': ['Patient A', 'Patient B', 'Patient C']})
        schedule = ui.load_schedule("test_schedule.xlsx")  # Use a test Excel file
        try:
            ui.write_schedule_to_excel(schedule, "test_schedule.xlsx", genotype, patients_df)
        except Exception as e:
            self.fail(f"ui.write_schedule_to_excel() raised an exception: {e}")