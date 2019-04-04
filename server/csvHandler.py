import csv
import sys


class StaticCSV:
    def __init__(self, inFilePath: str, outFilePath: str):
        self.inFile = inFilePath
        self.outFile = outFilePath

    def cleanArticleData(self):
        out = []
        # output = csv.writer(self.outFile, mode='w', delimiter=',',
        # quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv.field_size_limit(sys.maxsize)
        with open(self.inFile, newline='') as inFilePtr:
            reader = csv.reader(inFilePtr)
            for row in reader:
                out.append([row[2], row[3], row[5]])
                # out.append([row[0], row[1], row[2]])
                # print([row[2], row[3], row[5]])
                # exit(0)
        with open(self.outFile, mode='w') as outFilePtr:
            writer = csv.writer(outFilePtr, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in out:
                writer.writerow(row)
                # exit(0)


if __name__ == '__main__':
    s = StaticCSV('data/article1.csv', 'data/article1A.csv')
    s.cleanArticleData()
