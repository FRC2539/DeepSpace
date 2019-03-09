from wpilib.command.command import Command
from custom.config import Config
import math
import robot

class GoPastTapeCommand(Command):

    def __init__(self):
        super().__init__('Go Past Tape')

        self.requires(robot.drivetrain)

        self.tape = Config('limelight/tv', 0)
        self.strafe = Config('limelight/tx', 0)
        #self.angle = Config('cameraTable/tapeAngle', 0)

        self.x = 0
        self.y = 0
        self.rotate = 0

        self.originallyFieldOriented = True


    def initialize(self):
        #self.seenTape = self.tape.getValue()

        self.originallyFieldOriented = robot.drivetrain.isFieldOriented

        if self.originallyFieldOriented:
            robot.drivetrain.toggleFieldOrientation()

        self._finished = False


    def execute(self):
        if self.tape.getValue() == 1:
            self.x = self.strafe.getValue() + 1.5
            self.y = 0.15
            oX = self.x

            self.x = math.copysign((self.x * 2) / 100, self.x)
            self.rotate = self.x / 2

            if self.x > 0.4:
                self.x = math.copysign(0.4, self.x)
                self.rotate = self.x
            elif abs(oX) < 0.5:
                self.x = oX / 5
                self.rotate = self.x
            elif abs(oX) > 0.5 and self.x < 0.8:
                self.x = math.copysign(0.08, oX)
                self.rotate = math.copysign(0.08, oX)

            print('     X: ' + str(self.x))
            print('     Y: ' + str(self.y))
            print('Rotate: ' + str(self.rotate))
            print('')

            robot.drivetrain.move(self.x, self.y, self.rotate)

            self._finished = abs(self.x) <= 0.02 and abs(self.y) <= 0.02 and abs(self.rotate) <= 0.02
        else:
            print('No vision target found!')
            robot.drivetrain.move(0, 0, 0)
            self._finished = True


    def isFinished(self):
        return self._finished


    def end(self):
        robot.drivetrain.move(0, 0, 0)

        if self.originallyFieldOriented:
            robot.drivetrain.toggleFieldOrientation()