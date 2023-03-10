import math
from wpilib.drive.robotdrivebase import RobotDriveBase
from custom.config import Config
from .basedrive import BaseDrive

class MecanumDrive(BaseDrive):
    '''
    A drive base with four wheels, each independently driven. Due to the rollers
    placed at forty-five degree angles around the wheels, the robot can drive
    sideways, as well as forward and rotating, depending on how the motors are
    driven.
    '''

    def __init__(self, name):
        super().__init__(name)

        self.resetGyro()
        self.isFieldOriented = True

        self.strafeTicksPerInch = Config('DriveTrain/strafeTicksPerInch', 258) #Experimental value, reccomended to re-test for every robot.


    def setUseFieldOrientation(self, isFieldOriented=True):
        '''
        If set to true, the robot will drive the direction the joystick is
        moved (assuming the robot started facing the "up" direction), without
        regard to where the front of the robot is facing.
        '''

        self.isFieldOriented = isFieldOriented


    def toggleFieldOrientation(self):
        self.isFieldOriented = not self.isFieldOriented
        return self.isFieldOriented


    def strafeInchesToTicks(self, distance):
        '''Converts a distance in inches into a number of encoder ticks.'''
        return int(distance * self.strafeTicksPerInch)


    def _configureMotors(self):
        '''All four motors are active in a mecanum system.'''

        self.activeMotors = self.motors

        '''Invert the encoders.'''
        for motor in self.activeMotors:
            motor.setSensorPhase(True)


    def _calculateSpeeds(self, x, y, rotate):
        '''Determines what speed each motor should have.'''

        if self.isFieldOriented:
            '''Fancy math changes x and y based on gyro reading.'''
            heading = self.getAngle() * math.pi / 180

            cosA = math.cos(heading)
            sinA = math.sin(heading)

            newX = x * cosA - y * sinA
            newY = x * sinA + y * cosA

            x = newX
            y = newY

        return [
            x + y + rotate,
            x - y + rotate,
            -x + y + rotate,
            -x - y + rotate
        ]
