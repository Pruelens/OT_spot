
import streamlit as st

from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="", page_title="Opentrons Spotting Protocol Generator")
st.title("Opentrons Protocol Generator")

input_name=st.text_input('Name of protocol')

number_row=st.slider('Number of rows with samples in input plate:', 1,12,3)
number_samples=number_row*8
values = [str(0),str(1),str(2),str(3),str(4),str(6)]
default_ix = values.index(str(1))
number_dilutions=int(st.selectbox('Number of 10-fold Dilutions to prepare',values,index=default_ix))

values=[]
for i in range(number_dilutions):
    values.append(str(i+1))
values.append(str(i+2))
default_ix = values.index(str(1))

range_tospot=st.slider('Select a range of 10-fold dilutions to spot:', 1, number_dilutions, (0, number_dilutions))

range_tospot_o=list(range(range_tospot[0], range_tospot[1]+1))


col1, col2 = st.columns(2)
with col1:
    st.write("Range that will be spotted:")
with col2:
    st.latex(r'''[10^{-'''+str(range_tospot[0])+'''}, 10^{-'''+str(range_tospot[1])+'''}]''')

tot_spot=number_samples*(range_tospot[1]-range_tospot[0]+1)
tot_dilwells=number_samples*number_dilutions
tot_spot_pl=int(tot_spot/96.0001)+1
tot_dilwells_pl=int(tot_dilwells/96.0001)+1
st.write(tot_dilwells_pl)
if tot_spot_pl+tot_dilwells_pl>5:
    st.write("Too few positions, consider splitting up experiment.")

else:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Total spots:")
    with col2:
        st.latex(str(number_samples*(range_tospot[1]-range_tospot[0]+1)))




lines = ['from opentrons import protocol_api\n',
 '\n',
 "metadata = {'apiLevel': '2.11',\n",
 "            'protocolName': 'Your Protocol Name',\n",
 "            'author': 'Your Name',\n",
 "            'description': 'Your protocol description'}\n",
 '\n',
 '\n',
 '\n',
 'open_positions=[7,8,4,5,1,2,3]\n',
 "rows_plate_temp=['A1', 'A2', 'A3','A4','A5','A6','A7', 'A8', 'A9','A10','A11','A12']\n",
 '\n',
 '\n',
 '\n',
 '\n',
 'Dilplates={}\n',
 'for i in range(tot_dilplates):\n',
 '    Dilplates["Plate"+str(i+1)]=i\n',
 '\n',
 'Agar_plates={}\n',
 'for i in range(tot_agarplates):\n',
 '    Agar_plates["PlateAgar"+str(i+1)]=i\n',
 '\n',
 'source_rows=[]\n',
 'for i in range(number_of_rows):\n',
 '    source_rows.append(rows_plate_temp[i])\n',
 '\n',
 'rows_dplate_temp_all=[]\n',
 'for plate in range(tot_dilplates):\n',
 '    for row in rows_plate_temp:\n',
 '        rows_dplate_temp_all.append((plate,row))\n',
 '\n',
 'order_dplate=[]\n',
 'j=0\n',
 'for source_row in source_rows:\n',
 '    dill_wells=[]\n',
 '    for i in range(number_dilutions):\n',
 '        plate_nr=rows_dplate_temp_all[j][0]\n',
 '        dill_wells.append(rows_dplate_temp_all[j][1])\n',
 '        j += 1\n',
 '\n',
 '    order_dplate.append((source_row,plate_nr,dill_wells))\n',
 '\n',
 'rows_spot_plate_temp_all=[]\n',
 'for plate in range(tot_agarplates):\n',
 '    for row in rows_plate_temp:\n',
 '        rows_spot_plate_temp_all.append((plate,row))\n',
 '\n',
 'j=0\n',
 'for row_nr in range(len(order_dplate)):\n',
 '\n',
 '    if spot_range[0]==0:\n',
 "        spot_undiluted='yes'\n",
 '    else:\n',
 "        spot_undiluted='no'\n",
 '\n',
 '    to_spot=[]\n',
 '    for i in range(len(spot_range)):\n',
 '        plate_nr=rows_spot_plate_temp_all[j][0]\n',
 '        to_spot.append(rows_spot_plate_temp_all[j][1])\n',
 '        j += 1\n',
 '\n',
 '    order_dplate[row_nr]+=((spot_undiluted,plate_nr,to_spot))\n',
 '\n',
 '\n',
 'def run(protocol: protocol_api.ProtocolContext):\n',
 "    plateCulture = protocol.load_labware('greiner_96_wellplate_382ul', 10)\n",
 '\n',
 "    plateBuffer = protocol.load_labware('nest_12_reservoir_15ml', 11)\n",
 '\n',
 "    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)\n",
 "    tiprack_p10 = protocol.load_labware('opentrons_96_filtertiprack_10ul', 6)\n",
 '\n',
 '    positions_dil_plate=[]\n',
 '    dil_plates=[]\n',
 '    for d_plate,pos in zip(Dilplates,open_positions):\n',
 "        dil_plates.append(protocol.load_labware('greiner_96_wellplate_382ul', pos))\n",
 '        positions_dil_plate.append(pos)\n',
 '\n',
 '    positions_agar_plate=[item for item in open_positions if item not in positions_dil_plate]\n',
 '\n',
 '    positions_dil_plate=[]\n',
 '    agar_plates = []\n',
 '    for d_plate,pos in zip(Agar_plates,positions_agar_plate):\n',
 "        agar_plates.append(protocol.load_labware('agar_96_wellplate_10ul', pos))\n",
 '        positions_dil_plate.append(pos)\n',
 '\n',
 '\n',
 "    pipette = protocol.load_instrument('p300_multi_gen2', 'right',\n",
 '                                       tip_racks=[tiprack1])\n',
 '\n',
 "    pipetteP10 = protocol.load_instrument('p10_multi', 'left',\n",
 '                                       tip_racks=[tiprack_p10])\n',
 '\n',
 '    pipette.well_bottom_clearance.aspirate = 1\n',
 '\n',
 '    ##Fill plates with 180ul\n',
 '    pipette.pick_up_tip()\n',
 '    for d_plate in dil_plates:\n',
 '\n',
 "        pipette.transfer(180, plateBuffer.rows_by_name()['A'], d_plate.rows_by_name()['A'],\n",
 '                         blow_out=True,\n',
 "                         blowout_location='destination well',\n",
 "                         new_tip='never',\n",
 '        )\n',
 '\n',
 '    ##Dilution\n',
 '    for source_row in order_dplate:\n',
 '        pipette.transfer(20, plateCulture.wells_by_name()[source_row[0]], dil_plates[source_row[1]].wells_by_name()[source_row[2][0]],\n',
 '                         mix_before=(4, 50),  # mix 4 times with 50uL before aspirating\n',
 '                         mix_after=(3, 50),\n',
 '                         blow_out=True,\n',
 "                         blowout_location='destination well',\n",
 "                         touch_tip='True',\n",
 "                         new_tip='never'\n",
 '                         )\n',
 '        pipette.transfer(\n',
 '            20,\n',
 '            [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][:-1]],\n',
 '            [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][1:]],\n',
 '            mix_after=(3, 100),\n',
 '            blow_out=True,\n',
 "            blowout_location='destination well',\n",
 "            new_tip='never')\n",
 '\n',
 '        pipette.drop_tip()\n',
 '        if order_dplate.index(source_row) != len(order_dplate)-1:\n',
 '            pipette.pick_up_tip()\n',
 '\n',
 '        ##to agar plate\n',
 '\n',
 '    for source_row in order_dplate:\n',
 '        pipetteP10.pick_up_tip()\n',
 '\n',
 "        if source_row[3]=='no':\n",
 '            pipetteP10.transfer(\n',
 '                5,\n',
 '                [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][spot_range[0]-1:spot_range[-1]][::-1]],\n',
 '                [agar_plates[source_row[4]].wells_by_name()[well_name] for well_name in source_row[5][::-1]],\n',
 '                blow_out=False,\n',
 "                blowout_location='destination well',\n",
 "                new_tip='never')\n",
 '            pipetteP10.drop_tip()\n',
 '\n',
 '        else:\n',
 '            pipetteP10.transfer(\n',
 '                5,\n',
 '                [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][spot_range[1]-1:spot_range[-1]][::-1]],\n',
 '                [agar_plates[source_row[4]].wells_by_name()[well_name] for well_name in source_row[5][1:][::-1]],\n',
 '                blow_out=False,\n',
 "                blowout_location='destination well',\n",
 "                new_tip='never')\n",
 '\n',
 '            pipetteP10.transfer(\n',
 '                5,\n',
 '                [plateCulture.wells_by_name()[well_name] for well_name in [source_row[0]]],\n',
 '                [agar_plates[source_row[4]].wells_by_name()[well_name] for well_name in [source_row[5][0]]],\n',
 '                blow_out=False,\n',
 "                blowout_location='destination well',\n",
 "                new_tip='never')\n",
 '            pipetteP10.drop_tip()\n',
 '\n',
 '\n']


lines.insert(0,'\n')
lines.insert(0,'number_of_rows='+str(number_row)+ '\n')
lines.insert(0,'tot_dilplates='+str(tot_dilwells_pl)+ '\n')
lines.insert(0,'tot_agarplates='+str(tot_spot_pl)+ '\n')
lines.insert(0,'number_dilutions='+str(number_dilutions)+ '\n')
lines.insert(0,'spot_range='+str(range_tospot_o)+ '\n')




st.download_button('Download Protocol', ''.join(lines),file_name=input_name+'.txt')



st.write(
    "Contact: philip.ruelens(at)kuleuven.be")


