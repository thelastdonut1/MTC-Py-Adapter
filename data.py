# data.py

# Creating a class to store data in

class Data:
    '''
    Class made for storing data collected from the device.

    Attributes:
    key (str): 
        The dataItem from the device.
    value (Any): 
        The value associated with the dataItem.
    has_changed (bool): 
        Indicates whether this data has changed since it was last read from the device.
    SHDRString (str): 
        Key | Value pair organized in SHDR format.
    '''
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.type = "Sample"
        self.has_changed = False
        self.SHDRString = ''

    def update(self, newValue):
        self.value = newValue
        self.has_changed = True

    def SHDRFormat(self):
        SHDRString = "|" + self.key + "|" + str(self.value)
        return SHDRString


