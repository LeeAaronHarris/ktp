import re as regex

import numpy as np
import pandas as pd


class DataHandler:

    def __init__(self):
        pass

    def getAnnotatedDetails(self, data: [{}]):
        key = "annotation"
        if not self._saneData(data, key): return None

        details = [record[key] for record in data]
        return details

    def compressAnnotatedDetails(self, data: [{}]) -> [{}]:
        compressedData = []
        for record in data:
            newDetails = []
            for details in record:
                compressedDetails = {}
                try:
                    compressedDetails["label"] = details['label'][0]
                except:
                    continue  # skip the incomplete entries
                compressedDetails.update(details['points'][0])
                newDetails.append(compressedDetails)
            compressedData.append(newDetails)
        return compressedData

    # similar to the map function; breaks if data is not in the right order
    def _applyFunctionToAllValues(self, func, data) -> [{}]:
        for resumeIndex, resume in enumerate(data):
            for detailIndex, details in enumerate(resume):
                for key in details.keys():
                    data[resumeIndex][detailIndex][key] = func(str(details[key]))
        return data

    def stripInvalidCharacters(self, data: [{}]) -> [{}]:
        data = self._applyFunctionToAllValues(func=self.removeSpecialCharactersFromStr, data=data)
        return data

    def setAllCharactersToLowerCase(self, data: [{}]) -> [{}]:
        data = self._applyFunctionToAllValues(func=str.lower, data=data)
        return data

    def deleteDetail(self, detail):
        return []

    # There will be a row for each resume
    def filterData(self, data: [{}], filter: str) -> []:
        filteredData = []

        for resumeIndex, resume in enumerate(data):
            employeeDetails = []
            for detailIndex, details in enumerate(resume):
                for value in details.values():
                    if value == filter:
                        employeeDetails.append(
                            data[resumeIndex][detailIndex]['text'])  # group alll skills together in a str
            employeeDetails = " ".join(employeeDetails)
            filteredData.append(employeeDetails)
        return filteredData  # todo

    def removeSpecialCharactersFromStr(self, string: str) -> str:
        clean = regex.sub(pattern="[^A-Za-z0-9]+", repl=" ", string=string)  # didn't specify whether to clean '+'
        return clean

    def changeFormatOfKeyPhrases(self, data):
        # todo
        return data

    @staticmethod
    def _saneData(data: [{}], key: str) -> bool:
        """
        Sanity check data; return whether the data is as expected.

        :param data:
        :param key:
        :return:
        """
        try:
            firstDataRecord = data[0]
        except:
            print("[WARN] Incorrect data given. Expected list of size 1")
            return False

        try:
            value = firstDataRecord[key]
        except:
            print("[WARN] No such key in the data:" + key)
            return False

        try:
            value[0]
        except:
            print("[WARN] Incorrect value. Expected list of size 1")
            return False

        return True

    def assignClassnamesToResumes(self, targets, names):
        # reverse the one-hot encoding
        targets = np.argmax(targets, axis=1)

        classes = [names[int(target)] for target in targets]
        indexs = ["resume" + str(value + 1) for value in range(len(classes))]
        table = pd.DataFrame({"class": classes}, index=indexs)
        return table
