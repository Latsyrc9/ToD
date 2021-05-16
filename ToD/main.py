#!/usr/bin/env python
'''
This is a simple console base Truth or Dare game.

** This game will not handle errors gracefully **
'''
import os
import pandas as pd
import random

dir_path = os.path.dirname(os.path.realpath(__file__))

class Game():

    def __init__(self):
        self.game_running = True
        self.first_round = True
        self.random_player = True # can be turn Flase only after self.current_player is set
        self.turn_active = True
        self.current_lvl = [3,4,5] # lvl 8378 is test data
        self.list_of_players = []
        self.current_player = ''
        self.usr_input_choice = ''
        self.challenge_data_file_name = 'local_challenge_data.csv' # TODO: change based on ENV
        self.player_data_file_name = 'local_player_data.csv' # TODO: change based on ENV

        self.get_challenge_data()
        self.get_player_data()

        # TODO: create /data/setting_data.json
    
    def run(self):
        self.main_menu()
        while self.game_running:
            self.turn_active = True # Reset
            self.set_current_players()
            self.ask_truth_or_dare()
            if self.usr_input_choice != 'Q':
                self.current_challenge()

    def main_menu(self):
        '''Main Menu'''
        menu = True
        while menu:
            self.print_main_menu()
            choice = input('Enter your choice [1-4]: ')

            if choice == '1':
                print('Time to play the game')
                menu = False
            elif choice == '2':
                print('Using Default Playes')
            elif choice == '3':
                print('Cant Save Yet')
            elif choice == '4':
                print('Using Default Settings')
            elif choice == '5':
                print('Exiting the Game. Goodbye, play again soon!')
                menu = False
                self.quit()
            else:
                input('Wrong option selection. Enter any key to try again..')

    def print_main_menu(self):
        '''Prints out on the console the menu options'''
        print('MENU')
        print('1 - PLAY (New Game)')
        print('2 - Players')
        print('3 - Save')
        print('4 - Settings')
        print('5 - Exit')

    def set_current_players(self):
        '''Current Player'''
        self.list_of_players = self.player_data['Name'].values.tolist()

        if self.random_player:
            self.current_player = random.choice(self.list_of_players)
            self.random_player = False
        else:
            next_player_position = 0
            length = len(self.list_of_players)
            for i in range(length):
                if self.list_of_players[i] == self.current_player:
                    next_player_position = i + 1
            if next_player_position >= length:
                next_player_position = 0
            self.current_player = self.list_of_players[next_player_position]
        
    def ask_truth_or_dare(self):
        '''Ask user Truth or Dare or other options'''
        print('Quit (Q), Menu (M), Skip Trun (S)')
        self.usr_input_choice = input(str(self.current_player) + ': Truth (T) or Dare (D)?').capitalize()
        if self.usr_input_choice == 'T' or self.usr_input_choice == 'D':
            print('You chose ' + self.usr_input_choice)
        elif self.usr_input_choice == 'S':
            print(str(self.current_player) + ' will be skipped')
        elif self.usr_input_choice == 'M':
            print('Opening Menu')
        else:
            if self.usr_input_choice != 'Q':
                print('Any invalid input here will stop the game') # Makes my life EZer
                print('"' + str(self.usr_input_choice) + '" is an invalid choice. Goodbye, play again soon!')
            else:
                print('Goodbye, play again soon!')
            self.quit()

    def current_challenge(self):
        self.set_valid_challenge()
        self.set_valid_partners()
        while self.turn_active:
            # TODO: Setting any partners
            if self.valid_partners.empty:
                self.turn_active = False
                self.game_running = False
                print(self.current_player + ' has no valid partner')
            else:
                self.generate_challenge()
                choice = input('Completed (C), Fail (F), Re-Draw (R), Skip (S)').capitalize()
                if choice == 'R':
                    print('Generating new challenge')
                elif choice == 'C':
                    # TODO: Add points
                    self.turn_active = False
                elif choice == 'F':
                    # TODO: Loose Points
                    self.turn_active = False
                elif choice == 'S':
                    self.turn_active = False
                elif choice == 'M':
                    self.main_menu()
                    # TODO: Reset game or continue game
                elif choice == 'Q':
                    print('Goodbye, play again soon!')
                    self.quit()
                else:
                    print('"' + str(choice) + '" is an invalid input')

    def generate_challenge(self):
        '''Selects the challenge from given data and fills in the variables'''
        list_of_players = self.valid_partners['Name'].values.tolist()
        partner = random.choice([x for x in list_of_players if x != self.current_player])
        challenge = self.valid_challenges.sample()
        challenge = challenge.replace({'--player--': partner}, regex=True)
        print(str(self.current_player) + ': ' + str(challenge['challenge'].values[0]))
        if str(challenge['info'].values[0]) != 'nan':
            print(str(challenge['info'].values[0]))
        print("")

    def set_valid_challenge(self):
        '''Filter data to valid challenges for the current player'''
        current_player_position = 0
        data = self.challenge_data

        length = len(self.list_of_players)
        for i in range(length):
            if self.list_of_players[i] == self.current_player:
                current_player_position = i
        current_player_data = self.player_data.loc[[current_player_position]]

        # Simple filter for Truth or Dare
        if self.usr_input_choice == 'T':
            data = data[data['type'] == 'Truth']
        elif self.usr_input_choice == 'D':
            data = data[data['type'] == 'Dare']
        else:
            print('"' + str(self.usr_input_choice) + '" This type is not being filtered')
        
        # Filter data for Orientaion compatabilty
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

        # Filter data for valid levels
        data = data[data.lvl.isin(self.current_lvl)]

        self.valid_challenges = data

    def set_valid_partners(self):
        '''Filter valid partners for the current player'''
        player_data = self.player_data
        valid_partner_data = player_data[player_data['Name'] != str(self.current_player)]
        current_player_data = player_data.loc[player_data['Name'] == str(self.current_player)]
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
            print('OH NO SOMETHING WENT REALLY WRONG!') # Will be replced with error message
        
        self.valid_partners = valid_partner_data
        

    def get_challenge_data(self):
        data_file = dir_path + '/data/' + self.challenge_data_file_name
        self.challenge_data = pd.read_csv(data_file)

    def get_player_data(self):
        data_file = dir_path + '/data/' + self.player_data_file_name 
        self.player_data = pd.read_csv(data_file)

    def quit(self):
        self.usr_input_choice = 'Q'
        self.turn_active = False
        self.game_running = False

def main():
    # Init Game
    game = Game()

    # Run Game
    game.run()

    # TODO: Save & Exit Game
    # game.save()

if __name__ == '__main__':
    main()