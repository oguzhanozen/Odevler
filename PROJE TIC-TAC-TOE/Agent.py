import numpy as np
import random
import pickle
class Agent:

    def __init__(self, game, player = 'X', episode = 100000, epsilon = 0.9, discount_factor = 0.6, eps_reduce_factor = 0.01):
        
        self.game = game
        self.player = player
        self.brain = dict()
        self.episode = episode
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.results = {'X' : 0, 'O': 0, 'D': 0}
        self.eps_reduce_factor = eps_reduce_factor

    def save_brain(self, player):
        with open('brain'+player, 'wb') as brain_file:
            pickle.dump(self.brain, brain_file)

    def load_brain(self, player):
        try:
            with open('brain'+player, 'rb') as brain_file:
                self.brain = pickle.load(brain_file)
        except:
            print('Halihazirda egitilmis bir ajaniniz yok. Oyun bilgisayarin rastgele hamleleriyle devam edecek.') 

    def reward(self, player, move_history, result):
        _reward = 0
        if player == 1:
            if result == 1:
                _reward = 1
                self.results['X'] += 1 
            elif result == -1:
                _reward = -1
                self.results['O'] += 1 
        elif player == -1:
            if result == 1:
                _reward = -1
                self.results['X'] += 1 
            elif result == -1:
                _reward = 1
                self.results['O'] += 1
        if result == -2:
             self.results['D'] += 1
        move_history.reverse()
        
        for state, action in move_history:
            self.brain[state, action] = self.brain.get((state, action), 0.0) + _reward
            _reward *= self.discount_factor

    def use_brain(self):
        possible_actions = self.game.get_available_positions()
        max_qvalue = -1000
        best_action = possible_actions[0]
        for action in possible_actions:
            qvalue = self.brain.get((self.game.get_current_game_tuple(), action), 0.0)
            if qvalue > max_qvalue:
                best_action = action
                max_qvalue = qvalue
            elif qvalue == max_qvalue and random.random() < 0.5:
                best_action = action
                max_qvalue = qvalue
            elif len(possible_actions) == 9:
                best_action = random.choice(possible_actions)
                break

        return best_action


    def train_brain_x_byrandom(self):
        for _ in range(self.episode):
            if _ % 1000 == 0:
                print('Egitimde Oynanan Oyun Sayisi: '+str(_))
                self.epsilon -= self.eps_reduce_factor
            move_history = []

            while True:
               
                if sum(self.game.get_current_game()==1) == 0 or random.random()<self.epsilon:
                    available_actions = self.game.get_available_positions()
                    action_x = random.choice(available_actions)
                    move_history.append([self.game.get_current_game_tuple(), action_x])
                    self.game.make_move(action_x)
                else:
                    action_x = self.use_brain()
                    move_history.append([self.game.get_current_game_tuple(), action_x])
                    self.game.make_move(action_x)
                if self.game.is_winner():
                    self.reward(1 ,move_history, self.game.winner)
                    break
                available_actions = self.game.get_available_positions()
                action_o = random.choice(available_actions)
                self.game.make_move(action_o)
                if self.game.is_winner():
                        self.reward(1 ,move_history, self.game.winner)
                        break

        self.save_brain('X')
        print('Egitim Tamamlandi!')
        print('Ajanin Elde Ettigi Sonuclar :')
        print(self.results)

    def train_brain_o_byrandom(self):
        for _ in range(self.episode):
            if _ % 1000 == 0:
                print('Egitimde Oynanan Oyun Sayisi: '+str(_))
                self.epsilon -= self.eps_reduce_factor
            move_history = []
            while True:

                available_actions = self.game.get_available_positions()
                action_x = random.choice(available_actions)
                self.game.make_move(action_x)
                if self.game.is_winner():
                    self.reward(-1 ,move_history, self.game.winner)
                    break
                if random.random()<self.epsilon:
                    available_actions = self.game.get_available_positions()
                    action_o = random.choice(available_actions)
                    move_history.append([self.game.get_current_game_tuple(), action_o])
                    self.game.make_move(action_o)
                else:
                    action_o = self.use_brain()
                    move_history.append([self.game.get_current_game_tuple(), action_o])
                    self.game.make_move(action_o)

                if self.game.is_winner():
                    self.reward(-1 ,move_history, self.game.winner)
                    break

        self.save_brain('O')
        print('Egitim Tamamlandi!')
        print('Ajanin Elde Ettigi Sonuclar :')
        print(self.results)
    
    def play_with_human(self):
        self.load_brain(self.player)
        order = 1 if self.player=='X' else -1
        while True:
            if order == 1:
                self.game.make_move(self.use_brain())
                self.game.draw_current_game()
                order *= -1
                if self.game.is_winner(isgame = True):
                    break
            else:
                action_o = int(input('Hamlenizi hangi kareye yapacaksiniz?'))
                self.game.make_move(action_o-1)
                self.game.draw_current_game()
                order *= -1
                if self.game.is_winner(isgame = True):
                    break





