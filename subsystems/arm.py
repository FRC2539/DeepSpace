from .debuggablesubsystem import DebuggableSubsystem
from rev import CANSparkMax, MotorType, ControlType
import ports
from wpilib import DigitalInput


class Arm(DebuggableSubsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Arm')

        self.motor = CANSparkMax(ports.arm.motorID, MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()
        self.PIDController = self.motor.getPIDController()

        self.lowerLimit = DigitalInput(ports.arm.lowerLimit)

        self.upperLimit = 7000

        self.zero = 0

        #These are temporary and need to be finalized for competition.
        self.levels = {
                        'floor' : 0,
                        'lowHatches' : 2000,
                        'midHatches' : 4000,
                        'highHatches' : 6000,
                        'cargoBalls' : 3000,
                        'lowBalls' : 2500,
                        'midBalls' : 4500,
                        'highBalls' : 6500,
                        'start' : 7000
                        }


    def up(self):
        isTop = self.getPosition() >= self.upperLimit

        if isTop:
            self.stop()
        else:
            self.set(0.5)
            #self.PIDController.setReference(5000, ControlType.kVelocity)

        return isTop


    def down(self):
        isZero = self.isAtZero()

        if isZero:
            self.stop()
            self.zero = self.getPosition()
        else:
            self.set(-0.5)
            #self.PIDController.setReference(5000, ControlType.kVelocity)

        return isZero


    def stop(self):
        self.setPosition(self.getPosition())


    def set(self, speed):
        self.motor.set(speed)


    def setPosition(self, position):
        self.PIDController.setReference(position, ControlType.kPosition)


    def getPosition(self):
        return self.encoder.getPosition()


    def isAtZero(self):
        return not self.lowerLimit.get()


    def reZero(self):
        self.zero = self.getPosition()
        self.setPosition(self.zero)


    def goToLevel(self, level):
        self.setPosition(self.zero + self.levels[level])


    def goToFloor(self):
        self.goToLevel('floor')


    def goToStartingPosition(self):
        self.goToLevel('start')