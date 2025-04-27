class FileRead:
    @staticmethod
    def load(array, path):
        with open(path, "r") as i:
            for line in i:
                array.append(list(line.strip()))