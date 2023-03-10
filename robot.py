#!/usr/bin/env python3

from commandbased import CommandBasedRobot
from wpilib._impl.main import run
from wpilib import RobotBase

from custom import driverhud
import controller.layout
import subsystems
import shutil, sys
#itsahashtag
from wpilib.command import Subsystem

from subsystems.monitor import Monitor as monitor
from subsystems.drivetrain import DriveTrain as drivetrain
from subsystems.lights import Lights as lights
from subsystems.elevator import Elevator as elevator
from subsystems.intake import Intake as intake
from subsystems.arm import Arm as arm
from subsystems.climber import Climber as climber
from subsystems.hatch import Hatch as hatch
from subsystems.limelighttests import LimelightTests as limelighttests

class KryptonBot(CommandBasedRobot):
    '''Implements a Command Based robot design'''

    def robotInit(self):
        '''Set up everything we need for a working robot.'''

        if RobotBase.isSimulation():
            import mockdata

        self.subsystems()
        controller.layout.Layout.init(self)
        driverhud.init()

        from commands.startupcommandgroup import StartUpCommandGroup
        StartUpCommandGroup().start()


    def autonomousInit(self):
        '''This function is called each time autonomous mode starts.'''

        # Send field data to the dashboard
        driverhud.showField()

        # Schedule the autonomous command
        auton = driverhud.getAutonomousProgram()
        auton.start()
        driverhud.showInfo("Starting %s" % auton)


    def teleopInit(self):
        from commands.drivetrain.setpipelinecommand import SetPipelineCommand
        SetPipelineCommand(0).start()

    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert('Fatal Error: %s' % error)


    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules['robot']
        for key, var in vars.items():
            try:
                if issubclass(var, Subsystem) and var is not Subsystem:
                    setattr(module, key, var())
            except TypeError:
                pass


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        shutil.rmtree('opkg_cache', ignore_errors=True)
        shutil.rmtree('pip_cache', ignore_errors=True)

    run(KryptonBot)
