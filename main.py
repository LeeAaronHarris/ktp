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
filteredEmployeeResumes_skills = handlers.DataHandler().filterData(employeeResumes, filter="skills")
filteredEmployeeResumes_qualifications = handlers.DataHandler().filterData(employeeResumes, filter="degree")
filteredEmployeeResumes_jobs = handlers.DataHandler().filterData(employeeResumes, filter="companies worked at")

# task 7 - create a model to cluster the resumes
# N-gram; frequency counts of words
skill_counts = handlers.UnsupervisedMlHandler().countWordFrequency(data=filteredEmployeeResumes_skills)
qualification_counts = handlers.UnsupervisedMlHandler().countWordFrequency(data=filteredEmployeeResumes_qualifications)
jobs_counts = handlers.UnsupervisedMlHandler().countWordFrequency(data=filteredEmployeeResumes_jobs)

# each piece of data can be represented/visualised as 2 Principle Components
visualise = True
transformedSkills = handlers.UnsupervisedMlHandler().reduceDimensionality(data=skill_counts, visualise=visualise,
                                                                          title="Skills")
transformedQualifications = handlers.UnsupervisedMlHandler().reduceDimensionality(data=qualification_counts,
                                                                                  visualise=visualise,
                                                                                  title="Qualifications")
transformedJobs = handlers.UnsupervisedMlHandler().reduceDimensionality(data=jobs_counts, visualise=visualise,
                                                                        title="Jobs")

clusterPredictions_skills, clusterDistances_skills = handlers.UnsupervisedMlHandler().getDataClusters(transformedSkills)
clusterPredictions_qualifications, clusterDistances_qualifications = handlers.UnsupervisedMlHandler().getDataClusters(
    transformedQualifications)
clusterPredictions_jobs, clusterDistances_jobs = handlers.UnsupervisedMlHandler().getDataClusters(transformedJobs)

# task 8 - create a model to score the resumes
# 1) scoring - how far (according to eucliean distance) is each cluster from each center, as a percentage
classificationPercentages_skills = handlers.UnsupervisedMlHandler().identifyGroupPercentage(clusterDistances_skills)
classificationPercentages_qualifications = handlers.UnsupervisedMlHandler().identifyGroupPercentage(
    clusterDistances_qualifications)
classificationPercentages_jobs = handlers.UnsupervisedMlHandler().identifyGroupPercentage(clusterDistances_jobs)

# 2) which cluster corresponds to which class? identify based on word counts of 'testing', 'development', 'management'
classNames = ["testing", "development", "management"]
clusterClasses_skills = handlers.UnsupervisedMlHandler().identifyClusterClasses(filteredEmployeeResumes_skills,
                                                                                clusterPredictions_skills, classNames)
clusterClasses_qualifications = handlers.UnsupervisedMlHandler().identifyClusterClasses(
    filteredEmployeeResumes_qualifications, clusterPredictions_skills, classNames)
clusterClasses_jobs = handlers.UnsupervisedMlHandler().identifyClusterClasses(filteredEmployeeResumes_jobs,
                                                                              clusterPredictions_skills, classNames)

# 3) combine the scores and decide; urgently need a test set
clusterFrequencies = clusterClasses_skills + clusterClasses_qualifications + clusterClasses_jobs  # combined equally
clusterClasses = handlers.UnsupervisedMlHandler().getClusterClasses(clusterFrequencies, classNames)

# task 9 - create a data frame of the class for each employee
combinedData = classificationPercentages_skills + classificationPercentages_qualifications + classificationPercentages_jobs
multiLabelledResumes = handlers.SupervisedMlHandler().assignScoreToEachResume(data=combinedData, classNames=classNames)
print(multiLabelledResumes)
