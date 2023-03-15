# InstrumentControl
Control some of the instruments in the FOD lab at DTU. <br>
To interface with GPIB, both NI-VISA and the NI-488.2 driver are required, they can be found here: https://www.ni.com/en/search.html?pg=1&ps=10&sb=%2Brelevancy&sn=catnav:sup.dwl.ndr. <br>
To control the Newport motor used in the Ti:sapph laser, the SMC100 utility installer from https://www.newport.com/f/smc100-single-axis-dc-or-stepper-motion-controller is needed. <br><br>
To just install the InstrumentControl module in a local Python environment, use: pip install git+https://github.com/thjalfe/InstrumentControl.git#egg=InstrumentControl.
