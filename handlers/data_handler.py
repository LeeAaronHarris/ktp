import re as regex

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

    def stripInvalidCharacters(self, data : [{}]):
        for resumeIndex, resume in enumerate(data):
            for detailIndex, details in enumerate(resume):
                for key in details.keys():
                    data[resumeIndex][detailIndex][key] = self.removeSpecialCharactersFromStr(str(details[key]))
        return data


    def setAllCharactersToLowerCase(self, data):
        for resumeIndex, resume in enumerate(data):
            for detailIndex, details in enumerate(resume):
                for key in details.keys():
                    data[resumeIndex][detailIndex][key] = str(details[key]).lower()
        return data


    def removeSpecialCharactersFromStr(self, string):
        clean = regex.sub(pattern="[^A-Za-z0-9]+", repl=" ", string=string) # didn't specify whether to clean '+'
        return clean

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

    def filterEmployeeRecords(self, data: [{}], filters: [str]) -> [{}]:
        pass # todo
