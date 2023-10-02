from Groups import *
from Animals import *
import random

def merge_herds(cell):
    herds_in_cell = list(cell.herds)

    if len(herds_in_cell) <= 1:
        return
    
    min_threshold_herd = min(herds_in_cell, key=lambda herd: herd.threshold)

    for herd in herds_in_cell:
        if herd is not min_threshold_herd:
            for erbast in list(herd.members):
                erbast.join_group(min_threshold_herd)
            if not herd.members and herd in cell.herds:
                cell.herds.remove(herd)

def merge_prides(pride1, pride2):
    # print(f"Merging Pride {pride1.id} and Pride {pride2.id}")
    # print(f"Pride {pride1.id} threshold: {pride1.threshold}")
    # print(f"Pride {pride2.id} threshold: {pride2.threshold}")

    if pride1.threshold < pride2.threshold:
        keep_pride, remove_pride = pride1, pride2
    else:
        keep_pride, remove_pride = pride2, pride1

    if keep_pride is remove_pride:
        return

    # print(f"Keeping Pride {keep_pride.id}, removing Pride {remove_pride.id}")

    remove_members = remove_pride.members.copy()  # Create a copy of remove_pride.members
    for member in remove_members:
        member.join_group(keep_pride)

    # print(f"Pride {keep_pride.id} members after merge: {[member.id for member in keep_pride.members]}")

    keep_pride.cell.prides.remove(remove_pride)

def fight_prides(pride1, pride2):
    # print(f"Pride 1 members before fight: {[member.id for member in pride1.members]}")
    # print(f"Pride 2 members before fight: {[member.id for member in pride2.members]}")

    total_energy_pride1 = sum(member.energy for member in pride1.members)
    total_energy_pride2 = sum(member.energy for member in pride2.members)

    # print(f"Total energy of Pride 1: {total_energy_pride1}")
    # print(f"Total energy of Pride 2: {total_energy_pride2}")

    winning_probability_pride1 = total_energy_pride1 / (total_energy_pride1 + total_energy_pride2)

    # print(f"Winning probability of Pride 1: {winning_probability_pride1}")

    if random.random() < winning_probability_pride1:
        winner, loser = pride1, pride2
    else:
        winner, loser = pride2, pride1

    # social_attitude_increment = sum(member.energy for member in loser.members) / 100
    # print(f"Winner: {winner.id}")
    # print(f"Loser: {loser.id}")
    scaling_factor = 0.5
    energy_expenditure = (loser.getSize / winner.getSize) * scaling_factor

    for member in loser.members:
        loser.cell.inhabitants.remove(member)

    for member in winner.members:
        member.expend_energy(energy_expenditure)

    winner.cell.prides.remove(loser)

    # print(f"Prides in cell after fight: {[pride.id for pride in winner.cell.prides]}")

    # print(f"Pride 1 members after fight: {[member.id for member in pride1.members]}")
    # print(f"Pride 2 members after fight: {[member.id for member in pride2.members]}")

    

def evaluate_and_fight_prides(cell):
    prides_in_cell = cell.prides

    if len(prides_in_cell) <= 1:
        return

    # print(f"Initial prides in cell: {[pride.id for pride in prides_in_cell]}")

    for pride in prides_in_cell:
    
        # print(f"Pride ID: {pride.id}")
        # print(f"Pride members: {[member.id for member in pride.members]}")
        # print(f"Members' social attitudes: {[member.social_attitude for member in pride.members]}")
        
        pass

    while len(cell.prides) > 1:
        pride1 = cell.prides[0]
        pride2 = cell.prides[1]

        # print(f"Evaluating Pride {pride1.id} and Pride {pride2.id}")

        if pride1.should_join(pride2):
            # print(f"Pride {pride1.id} and Pride {pride2.id} should join")
            merge_prides(pride1, pride2)
        else:
            # print(f"Pride {pride1.id} and Pride {pride2.id} should fight")
            fight_prides(pride1, pride2)

    # print(f"Final prides in cell: {[pride.id for pride in prides_in_cell]}")

        

    

    

            

    