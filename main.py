import os
import handlers

# task 1 - read json
pathToEmployeeRecords = os.path.join("resources", "employee_records", "Entity Recognition in Resumes.json")
employeeRecords = handlers.EmployeeRecordHandler(pathToEmployeeRecords).load().getAllRecords()

# task 2 - clean up the resumes
print("[INFO] records loaded")

