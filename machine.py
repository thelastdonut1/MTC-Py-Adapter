from gcodeparser import GcodeParser
import time



class Gcode:
    def __init__(self):
        self.comment = ''
        self.command = ''
        self.X_Axis = 0
        self.Y_Axis = 0
        self.program = ''
        self.feedrate = 0
        self.RPM = 0
        self.execution = ''
        self.mode = ''

    def Parser(self):
        with open('Test.eia', 'r') as f:
            gcode = f.read()
        parsed_gcode = GcodeParser(gcode)
        for i in range(20):
        
            # used to check for no comments in gcode
            if not parsed_gcode.lines[i].comment:
                self.comment = ''
            else:
                self.comment = parsed_gcode.lines[i].comment

            # used to check for no commands in gcode
            if not parsed_gcode.lines[i].command:
                self.command = ''
            else:
                self.command = parsed_gcode.lines[i].command

            # used to check for no X value or if 0 in gcode
            if not parsed_gcode.lines[i].get_param('X'):
                self.X_Axis = ''

            if parsed_gcode.lines[i].get_param('X') == 0:
                self.X_Axis = parsed_gcode.lines[i].get_param('X')

            else:
                self.X_Axis = parsed_gcode.lines[i].get_param('X')

            # used to check for no Y value of if 0 in gcode
            if not parsed_gcode.lines[i].get_param('Y'):
                self.Y_Axis = ''

            if parsed_gcode.lines[i].get_param('Y') == 0:
                self.Y_Axis = parsed_gcode.lines[i].get_param('Y')

            else:
                self.Y_Axis = parsed_gcode.lines[i].get_param('Y')
            time.sleep(10)

        
                

if __name__ == "__main__":
    callmemaybe = Gcode()
    callmemaybe.Parser()
