import os
import handlers

# task 1 - read json
pathToEmployeeRecords = os.path.join("resources", "employee_records", "Entity Recognition in Resumes.json")
employeeResumes = handlers.EmployeeRecordHandler(pathToEmployeeRecords).load().getAllRecords()

# task 2 - only keep the parts of the resumes that we will use (the annotations)
employeeResumes = handlers.DataHandler().getAnnotatedDetails(employeeResumes)
employeeResumes = handlers.DataHandler().compressAnnotatedDetails(employeeResumes)

# task 3
# replace the special characters that we want to keep (e.g., c++) with other strings (e.g., 2c)
employeeResumes = handlers.DataHandler().changeFormatOfKeyPhrases(employeeResumes)

# task 4 - remove all special characters
# keep the characters that are valid, rather than removing those that aren't
employeeResumes = handlers.DataHandler().stripInvalidCharacters(employeeResumes)

# task 5 - set all characters to lowercase
employeeResumes = handlers.DataHandler().setAllCharactersToLowerCase(employeeResumes)

# task 6 - filter the resumes into just the skills
filteredEmployeeResumes_skills = handlers.DataHandler().filterData(employeeResumes, filter = "skills")
filteredEmployeeResumes_qualifications = handlers.DataHandler().filterData(employeeResumes, filter = "degree")
filteredEmployeeResumes_jobs = handlers.DataHandler().filterData(employeeResumes, filter = "companies worked at")

print("tmp")
# task 7 - create a model to cluster the resumes


# task 8 - create a model to score the resumes
targets = handlers.SupervisedMlHandler().createTargetsForData(filteredEmployeeResumes)
print("[INFO] records loaded")

