from wpilib.command.command import Command

import robot


class SuperPidLevel3Command(Command):

    def __init__(self):
        super().__init__('Super Pid Level3')

        self.requires(robot.elevator)
        self.requires(robot.arm)


    def initialize(self):
        robot.arm.positionPID(45)
        robot.elevator.setPosition(41)


    def execute(self):
        pass


    def end(self):
        pass
