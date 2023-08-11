#!/usr/bin/env python
# coding: utf-8

# # Yahtzee game

# ### Global

# In[1]:


import random
from IPython.display import clear_output


# In[2]:


# Define constants

num_dice = 5
num_sides = 6
num_rounds = 13


# ### Scoring functions

# In[3]:


def calculate_ones(dice):
    return dice.count(1)


# In[4]:


def calculate_twos(dice):
    return dice.count(2) * 2


# In[5]:


def calculate_threes(dice):
    return dice.count(3) * 3


# In[6]:


def calculate_fours(dice):
    return dice.count(4) * 4


# In[7]:


def calculate_fives(dice):
    return dice.count(5) * 5


# In[8]:


def calculate_sixes(dice):
    return dice.count(6) * 6


# In[9]:


def calculate_three_of_a_kind(dice):
    for value in set(dice):
        if dice.count(value) >= 3:
            return value * 3
    return 0


# In[10]:


def calculate_four_of_a_kind(dice):
    for value in set(dice):
        if dice.count(value) >= 4:
            return value * 4
    return 0


# In[11]:


def calculate_full_house(dice): 
    dice_set = set(dice)
    if len(dice_set) == 2 and dice.count(dice[0]) == 2 or  dice.count(dice[0]) == 3:
        return 25
    return 0


# In[12]:


def calculate_small_straight(dice):
    sorted_dice = sorted(dice)
    consecutive_count = 0
    for i in range(len(sorted_dice) - 1):
        if sorted_dice[i] + 1 == sorted_dice[i + 1]:
            consecutive_count += 1
            if consecutive_count == 3:
                return 30
        elif sorted_dice[i] != sorted_dice[i + 1]:
            consecutive_count = 0
    return 0


# In[13]:


def calculate_large_straight(dice):
    set_dice = list(set(dice))
    if len(set_dice) == 5:
        return 40
    return 0


# In[14]:


def calculate_yahtzee(dice):
    set_dice = list(set(dice))
    if len(set_dice) == 1:
        return 50
    return 0


# In[15]:


def calculate_chance(dice):
    return sum(dice)


# ### Combinations

# In[16]:


# Define scoring combinations and their scoring functions
available_combinations = {
    "Ones": calculate_ones,
    "Twos": calculate_twos,
    "Threes": calculate_threes,
    "Fours": calculate_fours,
    "Fives": calculate_fives,
    "Sixes": calculate_sixes,
    "Three Of A Kind": calculate_three_of_a_kind,
    "Four Of A Kind": calculate_four_of_a_kind,
    "Full House": calculate_full_house,
    "Small Straight": calculate_small_straight,
    "Large Straight": calculate_large_straight,
    "Yahtzee": calculate_yahtzee,
    "Chance": calculate_chance
}


# In[17]:


def display_available_combinations(player_name, scoreboard):
    print(f"\n{player_name}, available combinations:\n------------------------------")
    for combination in available_combinations.keys():
        if scoreboard[player_name][combination] is None:
            print(combination)


# In[18]:


def choose_combination(player_name, scoreboard):
    display_available_combinations(player_name, scoreboard)
    while True:
        choice = input("\nChoose a combination: ").title()
        if choice in available_combinations and scoreboard[player_name][choice] is None:
            return choice
        else:
            print("Invalid choice or combination already used. Please choose a valid combination.")


# In[19]:


def calculate_score(dice, combination):
    scoring_function = available_combinations[combination]
    if combination in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
        return scoring_function(dice)
    else:
        return scoring_function(dice)


# ### Scoreboard

# In[20]:


def initialize_scoreboard(players):
    scoreboard = {}
    
    for player_name in players:
        scoreboard[player_name] = {"Bonus": None}
        for combination in available_combinations.keys():
            scoreboard[player_name][combination] = None
            
    return scoreboard


# In[21]:


def update_scoreboard(player_name, combination, score, scoreboard):
    scoreboard[player_name][combination] = score


# In[22]:


def display_scoreboard(player_name, scoreboard, upper_section_combinations):
    print(f"\n{player_name}'s Scoreboard:\n-------------------")
    upper_section_scores = [score for combination, score in scoreboard[player_name].items() if combination in upper_section_combinations and score is not None]
    
    for combination, score in scoreboard[player_name].items():
        if combination != "Bonus":
            if score is not None:
                print(f"{combination}: {score}")
            else:
                print(f"{combination}: 0")
    
    bonus = calculate_bonus(scoreboard[player_name])  # Calculate bonus progress
    total_upper_section_score = sum(upper_section_scores)


# In[23]:


def calculate_total_scores(scoreboard):
    total_scores = {}
    for player, scores in scoreboard.items():
        bonus = calculate_bonus(scores)
        total_scores[player] = bonus + sum(score for combination, score in scores.items() if combination != 'Bonus' and score is not None)
    return total_scores


# In[24]:


def determine_winner(total_scores):
    max_score = max(total_scores.values())
    winners = [player for player, score in total_scores.items() if score == max_score]
    return winners, max_score


# In[25]:


def clear_scoreboard():
    cont = input("Press enter for next turn: ")
    clear_output()



# In[26]:


def calculate_bonus(player_scores):
    upper_section_combinations = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    upper_section_score = sum(player_scores[combination] for combination in upper_section_combinations if player_scores[combination] is not None)
    
    if upper_section_score >= 63:
        return 50
    else:
        return 0


# ## Main

# In[27]:


def roll_dice(num_dice, dice_to_keep=[]):
    rolled_dice = [random.randint(1, num_sides) for i in range(num_dice - len(dice_to_keep))]
    return dice_to_keep + rolled_dice


# In[28]:


def player_turn(player_name, scoreboard):
    print("\nPlayer Turn:", player_name)
    input(f"\n{player_name}, press Enter to roll the dice...")
    dice = roll_dice(num_dice)
    print(f"{player_name} rolled: {dice}")

    re_roll_count = 0
    new_dice = dice
    while re_roll_count < 2:
        re_roll_choice = input("\nEnter indices of dice to re-roll, or press Enter to keep all (Re-roll {}/2): ".format(re_roll_count + 1))
        if re_roll_choice.strip() == "":
            break  # If no input, exit the loop

        indices_to_reroll = [int(idx) - 1 for idx in re_roll_choice.split() if idx.isdigit()]
        if all(0 <= idx < num_dice for idx in indices_to_reroll) and len(indices_to_reroll) > 0:
            new_dice = roll_dice(num_dice, dice_to_keep=[new_dice[i] for i in range(num_dice) if i not in indices_to_reroll])
            new_dice.sort()
            print(f"{player_name} re-rolled: {new_dice}")
            re_roll_count += 1
        else:
            print("\nInvalid input. Please enter valid integer indices separated by spaces and within the range 1 to {}.".format(num_dice))

    chosen_combination = choose_combination(player_name, scoreboard)
    score = calculate_score(new_dice, chosen_combination)
    update_scoreboard(player_name, chosen_combination, score, scoreboard)
    bonus = calculate_bonus(scoreboard[player_name])
    
    upper_section_combinations = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    upper_section_score = sum(scoreboard[player_name][combination] for combination in upper_section_combinations if scoreboard[player_name][combination] is not None)

    print(f"{player_name} scored {score} points for {chosen_combination}")
    
    if scoreboard[player_name]['Bonus'] is None:
        scoreboard[player_name]['Bonus'] = bonus
        print(f"\nBonus: 50 points (Progress towards Bonus: {upper_section_score} / 63)")
    else:
        print(f"\nBonus: 50 points (Progress towards Bonus: {upper_section_score} / 63)")
    


# In[29]:


def main():
    print("Welcome to a game of Python Yahtzee!\n------------------------------------")
    num_players = int(input("\nEnter the number of players: "))
    players = [input(f"\nEnter name for Player {i+1}: ") for i in range(num_players)]
    scoreboard = initialize_scoreboard(players)

    total_combinations = len(available_combinations)
    
    upper_section_combinations = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    
    while any(score is None for player_scores in scoreboard.values() for score in player_scores.values()):
        print("\nNew round:\n----------")
        for player_name in players:
            if any(score is None for score in scoreboard[player_name].values()):
                player_turn(player_name, scoreboard)
                display_scoreboard(player_name, scoreboard, upper_section_combinations)
                clear_scoreboard()
               
                
    print("\nAll players have used all combinations. Game over!")
    
    total_scores = calculate_total_scores(scoreboard)
    winners, max_score = determine_winner(total_scores)

    print("\nFinal Scores:")
    for player, score in total_scores.items():
        print(f"{player}: {score}")
    
    print("\nWinner(s):")
    for winner in winners:
        print(f"{winner} wins with a score of {max_score}!")


# In[ ]:


main()


# In[ ]:




