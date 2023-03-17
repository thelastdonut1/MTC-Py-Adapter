# data.py

# Creating a class to store data in

from typing import Any

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
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

        self.values = [value]

        self.dataItemType = "Sample"
        
        self.has_changed = False
        
        self.SHDRString = ''

    def update(self, newValue):
        '''
        Updates the value of the dataItem and sets the has_changed attribute to True.
        '''
        if newValue != self.value:
            self.value = newValue
            self.has_changed = True

    def SHDRFormat(self) -> str:
        '''
        Returns the data in SHDR format.
        '''
        SHDRString = "|" + self.key + "|" + str(self.value)
        return SHDRString


