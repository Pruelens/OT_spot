from opentrons.simulate import simulate, format_runlog
# read the file
protocol_file = open('C:/Users/u0072317/OneDrive - KU Leuven/PycharmProjects/OpentronDash/OT_script.py')
# simulate() the protocol, keeping the runlog
runlog, _bundle = simulate(protocol_file,custom_labware_paths=['C:/Users/u0072317/OneDrive - KU Leuven/PycharmProjects/OpentronDash/labware/'])
# print the runlog
print(format_runlog(runlog))