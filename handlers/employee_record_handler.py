import json

class EmployeeRecordHandler:
    """
    Handle loading employee resumes.
    :param path: a relative path of where to find the json file.
    """

    def __init__(self, path: str):
        # sanity checks
        if not isinstance(path, str): Exception("path must be a string")
        try:
            with open(path) as file:
                pass
        except:
            Exception("path does not exist")
        self.path = path
        self.records = None

    def load(self):
        """
        load all employee resumes from an external (given) JSON file and store them in the class
        :return self
        """

        # set comprehension as invalid json; json only allows one top level element
        with open(self.path, mode="r", encoding="utf-8") as file:
            records = [json.loads(line) for line in file]
        self.records = records
        return self

    def getAllRecords(self) -> [{}]:
        return self.records
