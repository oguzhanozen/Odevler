import numpy as np

class TicTacToe:
    
    def __init__(self):
        self.current_state = np.zeros(9, dtype = np.int8)
        self.winner = None
        self.player = 1
    
    def draw_current_game(self):
        current_state = ['X' if x == 1 else 'O' if x == -1 else '--' for x in self.current_state]
        print(f'{current_state[0]:^5} {current_state[1]:^5} {current_state[2]:^5}')
        print(f'{current_state[3]:^5} {current_state[4]:^5} {current_state[5]:^5}')
        print(f'{current_state[6]:^5} {current_state[7]:^5} {current_state[8]:^5}')
        print('_'*15)
       
    """ Mevcut oyun durumunu numpy dizisi olarak döner."""
    def get_current_game(self):  
        return self.current_state
    
    """Mevcut oyun durumunu demet (tuple) olarak döner."""
    def get_current_game_tuple(self):
        return tuple(self.current_state)
    
    """Mevcut boş (0 olan) pozisyonların dizinlerini döner."""
    def get_available_positions(self):
        return(np.argwhere(self.current_state==0).ravel()) 

    """Oyun durumunu sıfırlar ve oyuncuyu X olarak ayarlar."""
    def reset_game(self): 
        self.current_state = np.zeros(9, dtype = np.int8)
        self.player = 1
    
    """Sıradaki oyuncuyu döner."""
    def get_player(self):
        return self.player

    """
   Hamleyi gerçekleştirir.
    """
    def make_move(self, action): 
        if action in self.get_available_positions():
            self.current_state[action] = self.player
            self.player *= -1
        else:
            print('Bu pozizyon mevcut degil..')

    """
    Eylem gerçekleştirilirse oluşacak durumu döndürür. Simulasyon icindir.
    """
    def _make_move(self, _current_state, action):
        _current_state[action] = self.player
        return _current_state

    """
   Olası eylemlerin gerçekleştirilmesi durumunda oluşacak durumları döndürür
    """
    def get_next_states(self):
        states = []
        _current_state = self.current_state
        _available_moves = self.get_available_positions()
        for move in _available_moves:
            states.append(self._make_move(_current_state = _current_state, action=move))
        return states
        
    """Kazananı Kontrol Eder"""
    def is_winner(self, isgame = False):
        winner_coordinates = np.array([[0,1,2], [3, 4, 5], [6, 7, 8],
                                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                                [0, 4, 8], [2, 4, 6]])
        for coordinate in winner_coordinates:
            total = sum(self.current_state[coordinate])
            if total == 3: 
                if isgame:
                    print('X Kazandi!')
                self.winner = 1
                self.reset_game()
                return 1
            elif total == -3: 
                if isgame:
                    print('O Kazandi!')
                self.winner = -1
                self.reset_game()
                return -1
            elif sum(self.current_state == 1) == 5:
                if isgame:
                    print('Berabere')
                self.winner = -2
                self.reset_game()
                return -2
        return False