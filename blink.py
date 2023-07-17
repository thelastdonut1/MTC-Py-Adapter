import gpiozero as gpio   
import time               
from signal import pause  
import RPi.GPIO as gpi0  

c_pin = 14                # Set the value of capasitor to 14
p_pin = 15                # Set the value of the potentiometer to 15

class readPotentiometer():  
    def __init__(self):    
        gpi0.setmode(gpi0.BCM)  # Set the mode of the GPIO library to BCM

        self.analog_value = None  # Initialize the analog_value variable to None
        self.numRange = 0         # Initialize the numRange variable to 0

        self._rangeV = {  # Define a dictionary named _rangeV
            '0': range(0, 16),
            '1': range(17, 32),
            '2': range(33, 48),
            '3': range(49, 64),
            '4': range(65, 80),
            '5': range(81, 96),
            '6': range(97, 112),
            '7': range(113, 128),
            '8': range(129, 144),
            '9': range(145, 160)
        }

    def discharge(self):  
        gpi0.setup(p_pin, gpi0.IN)   # Set up potentiometer as an input
        gpi0.setup(c_pin, gpi0.OUT)  # Set up capasitor as an output
        gpi0.output(c_pin, False)    # Set the output of the pin capasitor to False
        time.sleep(0.005)            # Pause for 0.005 seconds

    def charge_time(self):  
        gpi0.setup(c_pin, gpi0.IN)   # Set up the capasitor as an input
        gpi0.setup(p_pin, gpi0.OUT)  # Set up the potentiometer as an output
        count = 0                    # Initialize the count variable to 0
        gpi0.output(p_pin, True)     # Set the output of the pin potentiometer to True
        while not gpi0.input(c_pin):  # Repeat until the input of the pin capasitor is False
            count = count + 1        # Increment the count variable by 1
        return count                 

    def analog_read(self):  
        self.discharge()   # Call the discharge method
        return self.charge_time()  # Return the value from the charge_time method

    def run_analog(self):  
        while True:        # Repeat indefinitely
            self.analog_value = self.analog_read()  

            if self.analog_value >= 160:  # Check if the analog_value is greater than or equal to 160
                self.numRange = '9'       # Set the value of numRange to '9'

            if self.analog_value <= 0:    # Check if the analog_value is less than or equal to 0
                self.numRange = '0'       # Set the value of numRange to '0'

            for (key, val) in self._rangeV.items():  # Iterate over the items in the _rangeV dictionary
                if self.analog_value in val:          # Check if the analog_value is in the range of values
                    self.numRange = key                # Set the value of numRange to the corresponding key
                print(self.numRange)                   # Print the value of numRange

            time.sleep(0.75) 





class SSDisplay(gpio.LEDBoard):
    def __init__(self, *pins, **kwargs):
        if len(pins) < 7 or len(pins) > 8:  # Check if the number of pins is not between 7 and 8
            raise ValueError("SSDisplay must have 7 or 8 pins")  # Raise a ValueError with the specified message
        for pin in pins:  # Iterate over the pins
            assert not isinstance(pin, gpio.LEDCollection)  # Check that the pin is not an instance of gpio.LEDCollection
            
        pwm = kwargs.pop("pwm", False)  # Get the value of the "pwm" keyword argument, defaulting to False
        active_high = kwargs.pop('active_high', True)  # Get the value of the "active_high" keyword argument, defaulting to True
        initial_value = kwargs.pop('initial_value', False)  # Get the value of the "initial_value" keyword argument, defaulting to False
        if kwargs:  # Check if there are any remaining keyword arguments
            raise TypeError('unexpected keyword argument: %s' % kwargs.pop()[0])  # Raise a TypeError with the specified message

        self._layouts = {                                        # Define a dictionary named _layouts for the piosition of the LEDs on the 7 segment Display
            '1': (False, True, True, False, False, False, False),
            '2': (True, True, False, True, True, False, True),
            '3': (True, True, True, True, False, False, True),
            '4': (False, True, True, False, False, True, True),
            '5': (True, False, True, True, False, True, True),
            '6': (True, False, True, True, True, True, True),
            '7': (True, True, True, False, False, False, False),
            '8': (True, True, True, True, True, True, True),
            '9': (True, True, True, True, False, True, True),
            '0': (True, True, True, True, True, True, False),
        }

        self.AdapterSend = None  # Initialize the AdapterSend variable to None

        super(SSDisplay, self).__init__(*pins, pwm=pwm, active_high=active_high, initial_value=initial_value)  # Call the constructor of the superclass

    def display(self, char):
        char = str(char) 
        if len(char) > 1:  # Check if the length of char is greater than 1
            raise ValueError('only a single character can be displayed')
        if char not in self._layouts:  # Check if char is not a key in the _layouts dictionary
            raise ValueError('There is no layout for character - %s' % char)  
        layout = self._layouts[char]  # Get the layout from the _layouts dictionary for the given char
        for led in range(7):  # Iterate over the range from 0 to 6
            self[led].value = layout[led]  # Set the value of the corresponding LED to the value from the layout
        self.AdapterSend = char  # Set the AdapterSend variable to the input char


if __name__ == '__main__':  # Check if the script is being run directly
    myPoo = readPotentiometer()  
    myPoo.run_analog()  

    # seven_seg = SSDisplay(16, 12, 19, 13, 26, 21, 20, active_high=False)  # Create an instance of the SSDisplay class with the specified pins
    # time.sleep(5)
    # seven_seg.display("9")  # Call the display method of the SSDisplay instance with the character "9"
    # time.sleep(3)







# blink_on = False
# class blink():
#     def __init__(self):
#         self.LEDstate = None
#     def go_blink(self):
#         led = gpio.LED(17)
#         global blink_on
#         if blink_on:
#             led.off()
            
#         else:
#             led.blink(0.5, 0.5)
#             time.sleep(0.5)

#         blink_on = not blink_on
#         if not blink_on:
#             self.state = "OFF"
#         else:
#             self.state = "ON" 

#     button = gpio.Button(27)

#     try:
#         button.when_pressed = go_blink
        
#         pause()

#     finally:
#         pass

