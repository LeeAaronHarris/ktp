import os
import handlers

# task 1 - read json
pathToEmployeeRecords = os.path.join("resources", "employee_records", "Entity Recognition in Resumes.json")
employeeResumes = handlers.EmployeeRecordHandler(pathToEmployeeRecords).load().getAllRecords()

# task 2 - only keep the parts of the resumes that we will use (the annotations)
employeeResumes = handlers.DataHandler().getAnnotatedDetails(employeeResumes)
employeeResumes = handlers.DataHandler().compressAnnotatedDetails(employeeResumes)

# task 3 - remove all special characters
# keep the characters that are valid, rather than removing those that aren't
employeeResumes = handlers.DataHandler().stripInvalidCharacters(employeeResumes)

print("[INFO] records loaded")

