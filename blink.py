import gpiozero as gpio
import time 
from signal import pause
import RPi.GPIO as gpi0


c_pin = 14
p_pin = 15
class readPotentiometer():
    def __init__(self):
        gpi0.setmode(gpi0.BCM)

        self.analog_value = None
        self.numRange = 0

        self._rangeV = {
            '0' :range(0, 16),
            '1' :range(17, 32),
            '2' :range(33, 48),
            '3' :range(49, 64),
            '4' :range(65, 80),
            '5' :range(81, 96),
            '6' :range(97, 112),
            '7' :range(113, 128),
            '8' :range(129, 144),
            '9' :range(145, 160) 
        }

    def discharge(self):
        gpi0.setup(p_pin, gpi0.IN)
        gpi0.setup(c_pin, gpi0.OUT)
        gpi0.output(c_pin, False)
        time.sleep(0.005)

    def charge_time(self):
        gpi0.setup(c_pin, gpi0.IN)
        gpi0.setup(p_pin, gpi0.OUT)
        count = 0
        gpi0.output(p_pin, True)
        while not gpi0.input(c_pin):
            count = count +1
        return count

    def analog_read(self):
        self.discharge()
        return self.charge_time()
        

    def run_analog(self):
        while True:
            self.analog_value = self.analog_read()
            

            if self.analog_value >= 160:
               self.numRange = '9'

            if self.analog_value <= 0:                
                self.numRange = '0'

            for (key, val) in self._rangeV.items():
                if self.analog_value in val:
                    self.numRange = key
                print(self.numRange)

            time.sleep(.75)
                

            
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

    


class SSDisplay(gpio.LEDBoard):
    def __init__(self, *pins, **kwargs):
        if len(pins)< 7 or len(pins) > 8:
            raise ValueError("SSDisplay must have 7 or 8 pins")
        for pin in pins:
            assert not isinstance(pin, gpio.LEDCollection)
        pwm = kwargs.pop("pwm", False)
        active_high = kwargs.pop('active_high', True)
        initial_value = kwargs.pop('initial_value', False)
        if kwargs:
            raise TypeError('unexpected keybword argument: %s' %kwargs.pop()[0])
        
        self._layouts = {
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

        self.AdapterSend = None

        super(SSDisplay, self).__init__(*pins, pwm=pwm, active_high = active_high, initial_value=initial_value)

    def display(self, char):
        char = str(char)
        if len(char) > 1:
            raise ValueError('only a single character can b displayed')
        if char not in self._layouts:
            raise ValueError('There is no layout for character - %s' % char)
        layout = self._layouts[char]
        for led in range(7):
            self[led].value = layout[led]
        self.AdapterSend = char

    def display_hex(self, hexnumber):
        self.display(hex(hexnumber)[2:])
    
    
  
    def decimail_point(self):
        if len(self) > 7:
            return self[7].value
        else:
            raise NameError('there is no 8th pin for the decimal')#should b OutputDeviceError but was not working\
    


if __name__ == '__main__':
    myPoo = readPotentiometer()
    myPoo.run_analog()
    
    # seven_seg = SSDisplay( 16, 12, 19, 13, 26, 21, 20, active_high=False)
    # time.sleep(5)
#     seven_seg.display("9")
#     time.sleep(3)

