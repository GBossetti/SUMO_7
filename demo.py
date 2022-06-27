#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    #Time Step
    step = 0 #Keeping track of our time step, instead of query via track i (is simple tacking control from here)

    # Main control loop with exit condition                       
        # traci -> Traffic Control Interface
    while traci.simulation.getMinExpectedNumber() > 0: # -> return 0 when all reoute files have been exhausted and there's no more vehicles left in the simulation
        traci.simulationStep() # by default advance the simulation in one time step
        print(step)

        #det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        #for veh in det_vehs:
        #    print(veh)
        #    traci.vehicle.changeLane(veh, 2, 25)

        #if step == 350:
        #    """ traci.vehicle.changeTarget("0", "-E0")
        #    traci.vehicle.changeTarget("2", "-E0") """
        #    traci.vehicle.changeTarget("carflow", "-E0")
        
        step += 1

    traci.close()
    sys.stdout.flush()

# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "demo.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
