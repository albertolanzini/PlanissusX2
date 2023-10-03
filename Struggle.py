from Groups import *
from Animals import *
import random


def merge_herds(cell):
    # We merge the herds by selecting the one with the lowest threshold and letting all the other members
    # join that herd, to ensure all the erbasts are able to join and be in the same group.
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
    # We keep the pride with the lower threshold as we are sure it will welcome all the members
    # of the other pride

    if pride1.threshold < pride2.threshold:
        keep_pride, remove_pride = pride1, pride2
    else:
        keep_pride, remove_pride = pride2, pride1

    if keep_pride is remove_pride:
        return

    remove_members = remove_pride.members.copy()
    for member in remove_members:
        member.join_group(keep_pride)

    keep_pride.cell.prides.remove(remove_pride)


def fight_prides(pride1, pride2):

    total_energy_pride1 = sum(member.energy for member in pride1.members)
    total_energy_pride2 = sum(member.energy for member in pride2.members)

    # We calculate the probability of winning with the total energy of both prides
    winning_probability_pride1 = total_energy_pride1 / (total_energy_pride1 + total_energy_pride2)

    if random.random() < winning_probability_pride1:
        winner, loser = pride1, pride2
    else:
        winner, loser = pride2, pride1

    scaling_factor = 0.5
    energy_expenditure = (loser.getSize / winner.getSize) * scaling_factor

    # The fight is a last-blood fight: that means all the members of the losing group die after the fight,
    # while all the members of the winning group lose some energy due to the fight.
    for member in loser.members:
        loser.cell.inhabitants.remove(member)

    for member in winner.members:
        member.expend_energy(energy_expenditure)

    winner.cell.prides.remove(loser)


def evaluate_and_fight_prides(cell):
    # Evaluate if the prides should join or fight.
    prides_in_cell = cell.prides

    if len(prides_in_cell) <= 1:
        return

    while len(cell.prides) > 1:
        pride1 = cell.prides[0]
        pride2 = cell.prides[1]


        if pride1.should_join(pride2):

            merge_prides(pride1, pride2)

        else:
            
            fight_prides(pride1, pride2)


        

    

    

            

    