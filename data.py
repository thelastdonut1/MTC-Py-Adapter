# data.py

# Creating a class to store data in

class Data:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.has_changed = False
        self.SHDRString = ''

    def update(self, newValue):
        self.value = newValue
        self.has_changed = True

    def SHDRFormat(self):
        SHDRString = "|" + self.key + "|" + str(self.value)
        return SHDRString


