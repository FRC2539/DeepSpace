from wpilib.command.timedcommand import TimedCommand

import robot

class SlowEjectCommand(TimedCommand):

    def __init__(self):
        super().__init__('Slow Eject', 1.5)

        self.requires(robot.intake)


    def initialize(self):
        robot.intake.slowEject()


    def end(self):
        robot.lights.off()
        robot.intake.stop()
        robot.intake.hasCargo = False
