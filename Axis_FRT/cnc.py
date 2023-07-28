from gcodeparser import GcodeParser
import time
import math


# add comments
class CNC():
  def __init__(self, name, controller_name):
    self.name = name
    self.x_axis = Axis()
    self.y_axis = Axis()
    self.z_axis = Axis()
    self.controller = Controller(self, controller_name)
    

class Controller():
    def __init__(self, machine, name):
        self.name = name
        self.CNC = machine

    def Parser(self):
        with open('Test.eia', 'r') as f:
            gcode = f.read()
        self.parsed_gcode = GcodeParser(gcode)

        for line in self.parsed_gcode.lines:
            if line.command == ('G', 0):
                self.rapid(**line.params)
                  
            if line.command == ('G', 1):
                self.feed(**line.params)

    def rapid(self, **kwargs):
        x = kwargs.pop('X', None)
        y = kwargs.pop('Y', None)
        # z = kwargs.pop('Z', None)
        dx = self.Calculate(x, self.CNC.x_axis)
        dy = self.Calculate(y, self.CNC.y_axis)
        # dz = self.Calculate(z, self.CNC.z_axis)
        time = max(x[1] for x in [dx, dy])
        self.move(time, dx[0], dy[0])


    
    
    def feed(self, **kwargs):
        x = kwargs.pop('X', None)
        y = kwargs.pop('Y', None)
        # z = kwargs.pop('Z', None) 
        feedrate = kwargs.pop('F', None)

    def Calculate(self, cor, axis):
       delta = cor - axis.position
       time = delta/(axis.rapid_feed/60)
       return (delta, time)
    
    def move(self, t, dx, dy, dz = None):
       updates = 100
       intervule = t/updates
       xs = dx/updates
       ys = dy/updates
    #    zs = dz/intervule
       for i in range(math.floor(updates)):
          self.CNC.x_axis.position += xs
          self.CNC.y_axis.position += ys
        #   self.CNC.z_axis.position += zs
          time.sleep(intervule)
       





class Axis():
   def __init__(self):
      self.position = 0
      self.velo = 0
      self.acc = 32.15
      self.load = 0
      self.rapid_feed = 2362.20

class Spindle():
   def __init__(self):
      self.acc = 135.14
      self.RPM = 0
      self.load = 0
      self.max_rpm = 12000



myCNC = CNC("HCN", "Smooth G")
myCNC.controller.Parser()




# my_cnc = CNC("HCN-5000", "Smooth G") 
# my_cnc2 = CNC("HCN-6800", "Smooth G")
# print(my_cnc)   
# print(my_cnc2)   

    