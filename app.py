# Main file
# Standard imports
import os
import sys

workingDirectory = os.getcwd()

uiPath = os.path.join(workingDirectory, 'gui')
gamePath = os.path.join(workingDirectory, 'car_dodge')

sys.path.append(uiPath)
sys.path.append(gamePath)

# My imports
from gui import GUILoad

if __name__ == '__main__':
    arg = [uiPath, gamePath]
    GUILoad(arg) 