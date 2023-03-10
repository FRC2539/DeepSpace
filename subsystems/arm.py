from .debuggablesubsystem import DebuggableSubsystem
from rev import CANSparkMax, MotorType, ControlType
import ports
from wpilib import DigitalInput
from custom.config import Config

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

        self.FFk = Config('/Arm/FFk', 0)
        self.Pk = Config('/Arm/Pk', .00001)
        self.Ik = Config('/Arm/Ik', 0)
        self.Dk = Config('/Arm/Dk', 1)
        self.IZk = Config('/Arm/IZk', 0)

        self.PIDController.setFF(0.00019, 0)
        self.PIDController.setP(0.0001, 0)
        self.PIDController.setI(0, 0)
        self.PIDController.setD(0.001, 0)
        self.PIDController.setIZone(0, 0)

        self.motor.setOpenLoopRampRate(0.25)
        self.motor.setClosedLoopRampRate(0.25)

        self.motorspeed = 0.8

        self.lowerLimit = DigitalInput(ports.arm.lowerLimit)

        self.upperLimit = 70.0
        self.startPos = 105.0

        self.armTable = NetworkTables.getTable('Arm')

        self.armTable.putNumber('Position', self.getPosition())

        self.encoder.setPositionConversionFactor(1)
        self.encoder.setPosition(self.startPos)

        #self.zeroPosition = self.encoder.getPosition()

        #These are temporary and need to be finalized for competition.
        self.levels = {
                        'floor' : 0.0,
                        'aboveFloor' : 1.0,
                        'lowHatches' : 11.0,
                        'midHatches' : 37.0,
                        'highHatches' : 35.0,
                        'cargoBalls' : 55.0,
                        'lowBalls' : 70.0,
                        'midBalls' : 55.0,
                        'highBalls' : 70.0,
                        'start' : 90.0
                        }


    def up(self):
        speed = self.motorspeed

        isTop = self.getPosition() >= self.upperLimit

        if isTop:
            self.setPosition(float(self.upperLimit), 'down')
            self.stop()
        else:
            self.set(speed)

        finalPos = self.getPosition()
        self.armTable.putNumber('Position', int(finalPos))

        return isTop


    def down(self):
        speed = self.motorspeed * -1
        isZero = self.isAtZero()

        if isZero:
            print("arm zero")
            self.stop()
            self.resetEncoder()
            print("after encoder")

        else:
            self.set(speed)

        finalPos = self.getPosition()
        self.armTable.putNumber('Position', int(finalPos))

        return isZero


    def downSS(self):
        speed = self.motorspeed * -1
        return self.down(speed)

    def degreesToRotations(self, degrees):
        self.rotations = degrees*1.4
        return self.rotations


    def forceDown(self):
        print('Force Down ' + str(self.getPosition()))

    def shoot(self, speed):
        #self.motor.set(-0.82)
        self.PIDController.setReference(float(speed), ControlType.kVelocity, 0, 0)
        #self.set(-.8)


    def downNoZero(self, speed=-1.0):
        #speed = self.motor.speed * -1
        isZero = self.isAtZero()

        if isZero:
            self.stop()

        else:
            self.set(speed)

        return

        finalPos = self.getPosition()
        self.armTable.putNumber('Position', int(finalPos))


    def forceDown(self):

        if self.lowerLimit.get():
            self.set(-1)
        else:
            self.stop()
            self.resetEncoder()

        return self.lowerLimit.get()


    def forceUp(self):
        speed = self.motorspeed
        isTop = self.getPosition() >= self.startPos
        if not isTop:
            self.set(speed)
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
        #print("before reset: "+str(self.encoder.getPosition()))
        self.encoder.setPositionConversionFactor(1)
        self.encoder.setPosition(0.0)
        self.motor.setEncPosition(0.0)
        #print("after reset: "+str(self.encoder.getPosition()))
        #self.zeroPosition = self.encoder.getPosition()


    def setPosition(self, target, upOrDown):
        position = self.getPosition()


        if target > self.upperLimit or target < -3.5:
            self.stop()
            print('Illegal arm target position')
            return True

        elif upOrDown == 'up' and position < target:
            return self.up()

        elif upOrDown == 'down' and position > target:
            return self.down()

        else:
            self.stop()
            return True


    def getPosition(self):
        return self.encoder.getPosition()

    def positionPID(self, target):
        if target < 51 and target  > 0:
            self.target = self.degreesToRotations(target)
            self.PIDController.setReference(float(self.target), ControlType.kPosition, 0, 0)
        else:
            print("target was invalid")


    def isAtZero(self):
        return (not self.lowerLimit.get()) or (self.getPosition() <= 0.0)


    def goToLevel(self, level, upOrDown=''):
        return self.setPosition(float(self.levels[level]), upOrDown)


    def goToFloor(self):
        self.goToLevel('floor')


    def goToStartingPosition(self):
        self.goToLevel('start')
