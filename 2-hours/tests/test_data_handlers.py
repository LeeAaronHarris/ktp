import os
from unittest import TestCase

from handlers.employee_record_handler import EmployeeRecordHandler

class TestEmployeeRecordHandler(TestCase):

    def test_get_all_records(self):
        print("[INFO] Current dir:" + str(os.getcwd()))
        path = os.path.join('..', 'resources', 'employee_records', 'Entity Recognition in Resumes.json')
        records = EmployeeRecordHandler(path).load().getAllRecords()
        self.assertTrue(expr=len(records) > 0, msg="no employee records found")
