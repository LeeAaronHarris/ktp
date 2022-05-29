import os

import numpy as np

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
filteredEmployeeResumes_skills = handlers.DataHandler().filterData(employeeResumes, filter="skills")
filteredEmployeeResumes_qualifications = handlers.DataHandler().filterData(employeeResumes, filter="degree")
filteredEmployeeResumes_jobs = handlers.DataHandler().filterData(employeeResumes, filter="companies worked at")

# task 7 - create a model to cluster the resumes
# N-gram; frequency counts of words
skill_counts = handlers.UnsupervisedMlHandler().countWordFrequency(data=filteredEmployeeResumes_skills)
qualification_counts = handlers.UnsupervisedMlHandler().countWordFrequency(data=filteredEmployeeResumes_qualifications)
jobs_counts = handlers.UnsupervisedMlHandler().countWordFrequency(data=filteredEmployeeResumes_jobs)

# each piece of data can be represented as 2 Principle Components
transformedSkills = handlers.UnsupervisedMlHandler().reduceDimensionality(data = skill_counts)
transformedQualifications = handlers.UnsupervisedMlHandler().reduceDimensionality(data = qualification_counts)
transformedJobs = handlers.UnsupervisedMlHandler().reduceDimensionality(data = jobs_counts)

visualiseData = True
if visualiseData:
    handlers.DataVisualiser().visualiseData(transformedSkills)
    handlers.DataVisualiser().visualiseData(transformedQualifications)
    handlers.DataVisualiser().visualiseData(transformedJobs)

# task 8 - create a model to score the resumes
targets = handlers.SupervisedMlHandler().createTargetsForData(filteredEmployeeResumes_skills)

# task 9 - create a data frame of the class for each employee
classNames = ["testing", "development", "management"]
singleLabelledResumes = handlers.DataHandler().assignClassnamesToResumes(targets, classNames)
multiLabelledResumes = handlers.SupervisedMlHandler().assignScoreToEachClass(classNames)

print(multiLabelledResumes)
print(singleLabelledResumes)
