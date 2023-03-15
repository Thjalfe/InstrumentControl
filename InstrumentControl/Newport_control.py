# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:47:29 2020.

Function for control of Newport 850 G actuator. Through the SMC control box.

@author: larsgr
edited by thjalfe March 13 2023
"""

import time
# The CLR module provide functions for interacting with the underlying
# .NET runtime
# The crl module is part of pythonnet, which needs to be installed
import clr


class actuator:
    """Control of actuator."""

    def __init__(self, file_loc, port):
        """
        Parameters.

        ----------
        file_loc : String
            File location for Newport.SMC100.CommandInterface.dll.
        port : Integer
            COM port no.
        """

        # Add reference to assembly and import names from namespace
        clr.AddReference(file_loc + 'Newport.SMC100.CommandInterface.dll')
        import CommandInterfaceSMC100 as CI

        # Instrument Initialization
        self.instrument = "COM" + str(port)
        print('Instrument Key=>', self.instrument)

        # create a device instance
        self.SMC = CI.SMC100()

    def initialize(self, PSL, NSL):
        """
        Initialize.

        Parameters
        ----------
        PSL : Float
            Possitive software limit in mm.
        NSL : Float
            Negative software limit in mm.

        Returns
        -------
        None.

        """
        self.SMC.OpenInstrument(self.instrument)

        # Do a home search
        result, errString = self.SMC.OR(1, '')
        if result == 0:
            print('Home search done')
        else:
            print('Error=>', errString)

        # Set positive software limit
        result, errString = self.SMC.SR_Set(1, PSL, '')
        if result == 0:
            print('Positive software limit set')
        else:
            print('Error=>', errString)

        # Set negative software limit
        result, errString = self.SMC.SL_Set(1, NSL, '')
        if result == 0:
            print('Negative software limit set')
        else:
            print('Error=>', errString)

    def move(self, dist):
        """
        Moves.

        Parameters
        ----------
        dist : Float
            Distance in mm.

        Returns
        -------
        Float: Actual position.

        """
        # Move
        result, errString = self.SMC.PR_Set(1, dist, '')
        if result == 0:
            print('Moving')
        else:
            print('Error=>', errString)

        resul, Errorccode, status, errString = self.SMC.TS(1, '', '', '')
        while status == '28':
            time.sleep(0.1)
            resul, Errorccode, status, errString = self.SMC.TS(1, '', '', '')

        if Errorccode == '':
            print('Moved succesfully')
        else:
            print('Error: ' + Errorccode)

        # Get current position
        result, response, errString = self.SMC.TP(1, 00, '')
        if result == 0:
            print('position=>', response)
        else:
            print('Error=>', errString)

        return response

    def home(self):
        """
        Returs the actuator to the 0 position.

        Returns
        -------
        Float: Actual position.

        """
        # Move
        result, errString = self.SMC.PA_Set(1, 0, '')
        if result == 0:
            print('Moving')
        else:
            print('Error=>', errString)

        resul, Errorccode, status, errString = self.SMC.TS(1, '', '', '')
        while status == '28':
            time.sleep(0.1)
            resul, Errorccode, status, errString = self.SMC.TS(1, '', '', '')

        if Errorccode == '':
            print('Homed succesfully')
        else:
            print('Error: ' + Errorccode)

        # Get current position
        result, response, errString = self.SMC.TP(1, 00, '')
        if result == 0:
            print('position=>', response)
        else:
            print('Error=>', errString)

        return response

    def close(self):
        """
        Close the connection.

        Returns
        -------
        None.

        """
        self.SMC.CloseInstrument()
