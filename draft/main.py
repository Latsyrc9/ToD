#!/usr/bin/env python
'''
This is a simple console base Truth or Dare game draft.
Using this components will be built out.

** This game will not handle errors gracefully **
'''
import os
import pandas as pd
import random

dir_path = os.path.dirname(os.path.realpath(__file__))

data_file = dir_path + '/data/challenge_data.csv'
data = pd.read_csv(data_file)

# TODO: Convert player data to a file called /data/player_data.csv
player_data = pd.DataFrame(
    [['OMale', 'Male', 'Heterosexual'],
    ['OFelmale', 'Female', 'Heterosexual'],
    ['AFemale', 'Female', 'Bisexual'],
    ['SFemale', 'Female', 'Homosexual'],
    ['SMale', 'Female', 'Homosexual']], # Break code?
    columns=['Name', 'Gender', 'Orientation']
)

# TODO: Convert setting data to a file called /data/setting_data.json
game_settings = {
    'Starting Lvl': 99,
    'Category': 'All',
    'Objects': 'All'
}

# There has to be a better way to print the menu and keep tarck of the options but this is my solution for now
def print_menu():
    '''Prints out on the console the menu options'''
    print('MENU')
    print('1 - PLAY (New Game)')
    print('2 - Players')
    print('3 - Settings')
    print('4 - Exit')

def menu(game):
    '''Main Menu'''
    menu = True
    while menu:
        print_menu()
        choice = input('Enter your choice [1-4]: ')

        if choice == '1':
            print('Time to play the game')
            menu = False
        elif choice == '2':
            print('Using Default Playes')
        elif choice == '3':
            print('Using Default Settings')
        elif choice == '4':
            print('Exiting the Game. Goodbye, play again soon!')
            menu = False
            game = False
        else:
            input('Wrong option selection. Enter any key to try again..')
    return game

def play(game):
    '''Main Game Play'''
    current_player = []
    first_round = True
    lvl = game_settings['Starting Lvl']

    while game:
        current_turn = True
        current_player, first_round = players_turn(first_round, current_player)
        choice = usr_input(current_player)

        if choice == 'Q':
            break
        elif choice == 'S':
            continue
        elif choice == 'M':
            game = menu(game)
            # TODO: Reset game or continue game
        else:
            current_turn_failsafe = 0
            valid_data = validate_challenge(data, choice, current_player, player_data, lvl)
            while current_turn:
                valid_partner_data = valid_partners(current_player, player_data)
                # TODO: Setting any partners
                if valid_partner_data.empty:
                    current_turn = False
                    game = False
                    print(current_player + ' has no valid partner')
                else:
                    generate_challenge(valid_data, current_player, valid_partner_data)
                    choice = input('Completed (C), Fail (F), Re-Draw (R), Skip (S)').capitalize()
                    if choice == 'R':
                        print('Generating new challenge')
                    elif choice == 'C':
                        # TODO: Add points
                        current_turn = False
                    elif choice == 'F':
                        # TODO: Loose Points
                        current_turn = False
                    elif choice == 'S':
                        current_turn = False
                    elif choice == 'M':
                        game = menu(game)
                        # TODO: Reset game or continue game
                    elif choice == 'Q':
                        print('Goodbye, play again soon!')
                        current_turn = False
                        game = False
                    else:
                        print('"' + str(choice) + '" is an invalid input')

                if current_turn_failsafe > 25:
                    print('Current turn loop failsafe triggered. The current turn has lasted too lond. Ending game now.')
                    current_turn = False
                    game = False
                else:
                    current_turn_failsafe += 1

def players_turn(first_round, current_player):
    '''Current Player'''
    list_of_players = player_data['Name'].values.tolist()

    if first_round:
        current_player = random.choice(list_of_players)
        first_round = False
    else:
        next_player_position = 0
        length = len(list_of_players)
        for i in range(length):
            if list_of_players[i] == current_player:
                next_player_position = i + 1
        if next_player_position >= length:
            next_player_position = 0
        current_player = list_of_players[next_player_position]
    return current_player, first_round

def usr_input(current_player):
    '''Ask user Truth or Dare or other options'''
    print('Quit (Q), Menu (M), Skip Trun (S)')
    usr_choice = input(str(current_player) + ': Truth (T) or Dare (D)?').capitalize()
    if usr_choice == 'T' or usr_choice == 'D':
        print('You chose ' + usr_choice)
    elif usr_choice == 'S':
        print(str(current_player) + ' will be skipped')
    elif usr_choice == 'M':
        print('Opening Menu')
    else:
        if usr_choice != 'Q':
            print('Any invalid input here will stop the game') # Makes my life EZer
            print('"' + str(usr_choice) + '" is an invalid choice. Goodbye, play again soon!')
        else:
            print('Goodbye, play again soon!')
        usr_choice = 'Q'

    return usr_choice

def validate_challenge(data, choice, current_player, player_data, lvl):
    '''Filter data to valid challenges for the current player'''
    current_player_position = 0
    list_of_players = player_data['Name'].values.tolist()

    length = len(list_of_players)
    for i in range(length):
        if list_of_players[i] == current_player:
            current_player_position = i
    current_player_data = player_data.loc[[current_player_position]]

    if choice == 'T':
        data = data[data['type'] == 'Truth']
    elif choice == 'D':
        data = data[data['type'] == 'Dare']
    else:
        print('"' + str(choice) + '" This type is not being filtered')
    
    # There has to be a better logic
    if current_player_data['Gender'].iloc[0] == 'Male' and current_player_data['Orientation'].iloc[0] == 'Heterosexual':
        data = data[data['who'] != 'Female']
        data = data[data['who'] != 'Homosexual']
        data = data[data['who'] != 'Bisexual']
    elif current_player_data['Gender'].iloc[0] == 'Female' and current_player_data['Orientation'].iloc[0] == 'Heterosexual':
        data = data[data['who'] != 'Male']
        data = data[data['who'] != 'Homosexual']
        data = data[data['who'] != 'Bisexual']
    elif current_player_data['Gender'].iloc[0] == 'Male' and current_player_data['Orientation'].iloc[0] == 'Bisexual':
        data = data[data['who'] != 'Female']
        data = data[data['who'] != 'Homosexual']
        data = data[data['who'] != 'Heterosexual']
    elif current_player_data['Gender'].iloc[0] == 'Female' and current_player_data['Orientation'].iloc[0] == 'Bisexual':
        data = data[data['who'] != 'Male']
        data = data[data['who'] != 'Homosexual']
        data = data[data['who'] != 'Heterosexual']
    elif current_player_data['Gender'].iloc[0] == 'Male' and current_player_data['Orientation'].iloc[0] == 'Homosexual':
        data = data[data['who'] != 'Female']
        data = data[data['who'] != 'Heterosexual']
        data = data[data['who'] != 'Bisexual']
    elif current_player_data['Gender'].iloc[0] == 'Female' and current_player_data['Orientation'].iloc[0] == 'Homosexual':
        data = data[data['who'] != 'Male']
        data = data[data['who'] != 'Heterosexual']
        data = data[data['who'] != 'Bisexual']

    data = data[data['lvl'] == lvl]

    return data

def valid_partners(current_player, player_data):
    '''Filter valid partners for the current player'''
    valid_partner_data = player_data[player_data['Name'] != str(current_player)]
    # list_of_players = player_data['Name'].values.tolist()
    current_player_data = player_data.loc[player_data['Name'] == str(current_player)]
    if current_player_data['Orientation'].iloc[0] == 'Bisexual' and current_player_data['Gender'].iloc[0] == 'Female':
        valid_partner_data = valid_partner_data[
            (valid_partner_data['Orientation'] == 'Bisexual') |
            ((valid_partner_data['Gender'] == 'Female') & (valid_partner_data['Orientation'] == 'Homosexual')) |
            ((valid_partner_data['Gender'] == 'Male') & (valid_partner_data['Orientation'] == 'Heterosexual')) ]
    elif current_player_data['Orientation'].iloc[0] == 'Homosexual' and current_player_data['Gender'].iloc[0] == 'Female':
        valid_partner_data = valid_partner_data[
            ((valid_partner_data['Gender'] == 'Female') & (valid_partner_data['Orientation'] == 'Homosexual')) |
            ((valid_partner_data['Gender'] == 'Female') & (valid_partner_data['Orientation'] == 'Bisexual')) ]
    elif current_player_data['Orientation'].iloc[0] == 'Heterosexual' and current_player_data['Gender'].iloc[0] == 'Female':
        valid_partner_data = valid_partner_data[
            ((valid_partner_data['Gender'] == 'Male') & (valid_partner_data['Orientation'] == 'Heterosexual')) |
            ((valid_partner_data['Gender'] == 'Male') & (valid_partner_data['Orientation'] == 'Bisexual')) ]
    elif current_player_data['Orientation'].iloc[0] == 'Bisexual' and current_player_data['Gender'].iloc[0] == 'Male':
        valid_partner_data = valid_partner_data[
            (valid_partner_data['Orientation'] == 'Bisexual') |
            ((valid_partner_data['Gender'] == 'Male') & (valid_partner_data['Orientation'] == 'Homosexual')) |
            ((valid_partner_data['Gender'] == 'Female') & (valid_partner_data['Orientation'] == 'Heterosexual')) ]
    elif current_player_data['Orientation'].iloc[0] == 'Homosexual' and current_player_data['Gender'].iloc[0] == 'Male':
        valid_partner_data = valid_partner_data[
            ((valid_partner_data['Gender'] == 'Male') & (valid_partner_data['Orientation'] == 'Homosexual')) |
            ((valid_partner_data['Gender'] == 'Male') & (valid_partner_data['Orientation'] == 'Bisexual')) ]
    elif current_player_data['Orientation'].iloc[0] == 'Heterosexual' and current_player_data['Gender'].iloc[0] == 'Male':
        valid_partner_data = valid_partner_data[
            ((valid_partner_data['Gender'] == 'Female') & (valid_partner_data['Orientation'] == 'Heterosexual')) |
            ((valid_partner_data['Gender'] == 'Female') & (valid_partner_data['Orientation'] == 'Bisexual'))]
    else:
        print('OH NO SOMETHING WENT REALLY WRONG!')
    
    return valid_partner_data
    

def generate_challenge(valid_data, current_player, valid_partner_data):
    '''Selects the challenge from given data and fills in the variables'''
    list_of_players = valid_partner_data['Name'].values.tolist()
    partner = random.choice([x for x in list_of_players if x != current_player])
    challenge = valid_data.sample()
    challenge = challenge.replace({'--player--': partner}, regex=True)
    print(str(current_player) + ': ' + str(challenge['challenge'].values[0]))
    if str(challenge['info'].values[0]) != 'nan':
        print(str(challenge['info'].values[0]))
    print("")

def main(data):
    game = True

    game = menu(game) # Starting Menu

    play(game) # Play Game Loop
    
if __name__ == '__main__':
    main(data) # This might not be the best way to handle the data but it will do for now