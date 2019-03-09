from .debuggablesubsystem import DebuggableSubsystem
from rev import CANSparkMax, MotorType, ControlType
import ports
from wpilib import DigitalInput

import robot
from networktables import NetworkTables

class Arm(DebuggableSubsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Arm')

        self.motor = CANSparkMax(ports.arm.motorID, MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()
        self.PIDController = self.motor.getPIDController()

        self.motor.setInverted(True)

        self.PIDController.setFF(0.5, 0)
        self.PIDController.setP(0.1, 0)
        self.PIDController.setI(0.001, 0)
        self.PIDController.setD(10, 0)
        self.PIDController.setIZone(3, 0)

        self.motor.setOpenLoopRampRate(0.4)
        self.motor.setClosedLoopRampRate(0.4)

        self.lowerLimit = DigitalInput(ports.arm.lowerLimit)

        self.upperLimit = 70.0
        self.startPos = 105.0

        self.encoder.setPositionConversionFactor(1)
        self.encoder.setPosition(self.startPos)

        #These are temporary and need to be finalized for competition.
        self.levels = {
                        'floor' : 0.0,
                        'aboveFloor' : 5.0,
                        'lowHatches' : 31.0,
                        'midHatches' : 37.0,
                        'highHatches' : 35.0,
                        'cargoBalls' : 55.0,
                        'lowBalls' : 70.0,
                        'midBalls' : 55.0,
                        'highBalls' : 70.0,
                        'start' : 90.0
                        }


    def up(self):
        isTop = self.getPosition() >= self.upperLimit
        print('Arm ' + str(self.getPosition()))

        if isTop:
            self.setPosition(float(self.upperLimit), 'down')
            self.stop()
        else:
            robot.lights.isZero()
            self.set(0.93)

        return isTop


    def down(self):
        isZero = self.isAtZero()
        print('Arm ' + str(self.getPosition()))

        if isZero:
            print('IS ZERO ')
            self.stop()
            self.resetEncoder()
            robot.lights.isZero()


        else:
            self.set(-1)
            if isZero:
                print('IS ZERO')
                self.stop()
                self.resetEncoder()
        return isZero

    def downSS(self):
        isZero = self.isAtZero()
        print('Arm ' + str(self.getPosition()))

        if isZero:
            print('IS ZERO ')
            self.stop()
            self.resetEncoder()
            robot.lights.isZero()


        else:
            self.set(-0.7)

        return isZero

    def forceDown(self):
        print('Down ' + str(self.getPosition()))
        if self.lowerLimit.get():
            self.set(-1)
        else:
            self.stop()
            self.resetEncoder()

        return self.lowerLimit.get()


    def forceUp(self):
        isTop = self.getPosition() >= self.startPos
        if not isTop:
            self.set(1.0)
        else:
            self.stop()

        return isTop

    def stop(self):
        self.set(0.0)


    def hold(self):
        self.setPosition(self.getPosition())


    def set(self, speed):
        self.motor.set(float(speed))


    def resetEncoder(self):
        self.encoder.setPosition(0.0)


    def setPosition(self, target, upOrDown):
        position = self.getPosition()

        print('POSITION: ' + str(position))
        print('TARGET: ' + str(target))
        print('Up or down:  ' + str(upOrDown))

        if position >= self.startPos or position <= 0:
            self.stop()
            return True

        if upOrDown.lower() == 'up' and position < target:
            #target = target - position
            self.PIDController.setReference(float(target), ControlType.kPosition, 0, 0)
            return False

        elif upOrDown.lower() == 'down' and position > target:
            #target = -1 * (position - target)
            self.PIDController.setReference(float(target), ControlType.kPosition, 0, 0)
            return False

        else:
            self.stop()
            return True


    def getPosition(self):
        return self.encoder.getPosition()


    def isAtZero(self):
        return (not self.lowerLimit.get()) or (self.getPosition() <= 0.0)


    def goToLevel(self, level, upOrDown=''):
        return self.setPosition(float(self.levels[level]), upOrDown)


    def goToFloor(self):
        self.goToLevel('floor')


    def goToStartingPosition(self):
        self.goToLevel('start')
