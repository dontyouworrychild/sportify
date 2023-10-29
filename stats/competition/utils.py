import math
from game.models import Game
from .models import Participant


def next_power_of_2(length):
    if (length < 1):
        return 0
    a = math.log2(length)
    a = int(a)
    return 2**a if 2**a == length else 2**(a + 1)

def generate_tournament_bracket_logic(age_category, weight_category, competition):
    participants = list(Participant.objects.filter(competition=competition, age_category=age_category, weight_category=weight_category))
    next_power_of_two = next_power_of_2(len(participants))
    if next_power_of_two < 1:
        return "There are no participants"
    
    while len(participants) < next_power_of_two:
        participants.append(None)
    
    # normalize tut, sorting anau-mynau osynda bolu kerek
    return generate_bracket_for_category(participants, age_category, weight_category, competition)
        
        
def generate_bracket_for_category(participants, age_category, weight_category, competition):
    
    level = math.log2(len(participants))
    max_level = level
    prev_level = []
    current_level = []

    if len(participants) == 0:
        return f"No games in {age_category} - {weight_category}"

        
    if len(participants) == 1:
        g = Game(competition=competition, blue_corner=participants[0], red_corner=None, age_category=age_category, weight_category=weight_category)
        g.save()
        return "Succesfully generated tournament bracket for single participant"
        
    index = 1
        
    for i in range(int(len(participants) / 2)):
        player1_id = i
        player2_id = len(participants) - 1 - i

        if participants[player2_id] is None:
            g = Game(competition=competition,
                    blue_corner=participants[player1_id], red_corner=None,
                    age_category=age_category, weight_category=weight_category, level=level, index=index)
            g.save()
            index += 1
            prev_level.append(g)
        else:
            g = Game(competition=competition,
                    blue_corner=participants[player1_id], red_corner=participants[player2_id],
                    age_category=age_category, weight_category=weight_category, level=level, index=index)
            g.save()
            index += 1
            prev_level.append(g)
        
    level -= 1

    while level >= 1:
        for i in range(0, len(prev_level), 2):
            if level + 1 == max_level:
                if prev_level[i].red_corner is None:
                    prev_level[i].winner = prev_level[i].blue_corner
                if prev_level[i + 1].red_corner is None:
                    prev_level[i + 1].winner = prev_level[i + 1].blue_corner
                
            g = Game(competition=competition,
                        blue_corner=prev_level[i].winner, red_corner=prev_level[i+1].winner,
                        age_category=age_category, weight_category=weight_category, level=level, index=index)
            index += 1

            g.save()
                
            prev_level[i].parent = g
            prev_level[i].save()
            prev_level[i+1].parent = g
            prev_level[i+1].save()
            current_level.append(g)
            
        prev_level = current_level
        current_level = []
            
        level -= 1

    return "Successfully generated tournament bracket"