from opentrons import protocol_api

metadata = {'apiLevel': '2.11',
            'protocolName': 'Your Protocol Name',
            'author': 'Your Name',
            'description': 'Your protocol description'}


number_of_rows=3
tot_dilplates=1
tot_agarplates=1
number_dilutions=1
spot_range=[1]
open_positions=[7,8,4,5,1,2,3]
rows_plate_temp=['A1', 'A2', 'A3','A4','A5','A6','A7', 'A8', 'A9','A10','A11','A12']




Dilplates={}
for i in range(tot_dilplates):
    Dilplates["Plate"+str(i+1)]=i

Agar_plates={}
for i in range(tot_agarplates):
    Agar_plates["PlateAgar"+str(i+1)]=i

source_rows=[]
for i in range(number_of_rows):
    source_rows.append(rows_plate_temp[i])

rows_dplate_temp_all=[]
for plate in range(tot_dilplates):
    for row in rows_plate_temp:
        rows_dplate_temp_all.append((plate,row))

order_dplate=[]
j=0
for source_row in source_rows:
    dill_wells=[]
    for i in range(number_dilutions):
        plate_nr=rows_dplate_temp_all[j][0]
        dill_wells.append(rows_dplate_temp_all[j][1])
        j += 1

    order_dplate.append((source_row,plate_nr,dill_wells))

rows_spot_plate_temp_all=[]
for plate in range(tot_agarplates):
    for row in rows_plate_temp:
        rows_spot_plate_temp_all.append((plate,row))

j=0
for row_nr in range(len(order_dplate)):

    if spot_range[0]==0:
        spot_undiluted='yes'
    else:
        spot_undiluted='no'

    to_spot=[]
    for i in range(len(spot_range)):
        plate_nr=rows_spot_plate_temp_all[j][0]
        to_spot.append(rows_spot_plate_temp_all[j][1])
        j += 1

    order_dplate[row_nr]+=((spot_undiluted,plate_nr,to_spot))


def run(protocol: protocol_api.ProtocolContext):
    plateCulture = protocol.load_labware('greiner_96_wellplate_382ul', 10)

    plateBuffer = protocol.load_labware('nest_12_reservoir_15ml', 11)

    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    tiprack_p10 = protocol.load_labware('opentrons_96_filtertiprack_10ul', 6)

    positions_dil_plate=[]
    dil_plates=[]
    for d_plate,pos in zip(Dilplates,open_positions):
        dil_plates.append(protocol.load_labware('greiner_96_wellplate_382ul', pos))
        positions_dil_plate.append(pos)

    positions_agar_plate=[item for item in open_positions if item not in positions_dil_plate]

    positions_dil_plate=[]
    agar_plates = []
    for d_plate,pos in zip(Agar_plates,positions_agar_plate):
        agar_plates.append(protocol.load_labware('agar_96_wellplate_10ul', pos))
        positions_dil_plate.append(pos)


    pipette = protocol.load_instrument('p300_multi_gen2', 'right',
                                       tip_racks=[tiprack1])

    pipetteP10 = protocol.load_instrument('p10_multi', 'left',
                                       tip_racks=[tiprack_p10])

    pipette.well_bottom_clearance.aspirate = 1

    ##Fill plates with 180ul
    pipette.pick_up_tip()
    for d_plate in dil_plates:

        pipette.transfer(180, plateBuffer.rows_by_name()['A'], d_plate.rows_by_name()['A'],
                         blow_out=True,
                         blowout_location='destination well',
                         new_tip='never',
        )

    ##Dilution
    for source_row in order_dplate:
        pipette.transfer(20, plateCulture.wells_by_name()[source_row[0]], dil_plates[source_row[1]].wells_by_name()[source_row[2][0]],
                         mix_before=(4, 50),  # mix 4 times with 50uL before aspirating
                         mix_after=(3, 50),
                         blow_out=True,
                         blowout_location='destination well',
                         touch_tip='True',
                         new_tip='never'
                         )
        if number_dilutions==1:
            pass
        else:
            pipette.transfer(
                20,
                [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][:-1]],
                [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][1:]],
                mix_after=(3, 100),
                blow_out=True,
                blowout_location='destination well',
                new_tip='never')

        pipette.drop_tip()
        if order_dplate.index(source_row) != len(order_dplate)-1:
            pipette.pick_up_tip()

        ##to agar plate

    for source_row in order_dplate:
        pipetteP10.pick_up_tip()

        if source_row[3]=='no':
            pipetteP10.transfer(
                5,
                [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][spot_range[0]-1:spot_range[-1]][::-1]],
                [agar_plates[source_row[4]].wells_by_name()[well_name] for well_name in source_row[5][::-1]],
                blow_out=False,
                blowout_location='destination well',
                new_tip='never')
            pipetteP10.drop_tip()

        else:
            pipetteP10.transfer(
                5,
                [dil_plates[source_row[1]].wells_by_name()[well_name] for well_name in source_row[2][spot_range[1]-1:spot_range[-1]][::-1]],
                [agar_plates[source_row[4]].wells_by_name()[well_name] for well_name in source_row[5][1:][::-1]],
                blow_out=False,
                blowout_location='destination well',
                new_tip='never')

            pipetteP10.transfer(
                5,
                [plateCulture.wells_by_name()[well_name] for well_name in [source_row[0]]],
                [agar_plates[source_row[4]].wells_by_name()[well_name] for well_name in [source_row[5][0]]],
                blow_out=False,
                blowout_location='destination well',
                new_tip='never')
            pipetteP10.drop_tip()


