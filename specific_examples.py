import LTL2DFA as ltlf2dfa


# construct a dfa that implements alternating bit protocol
class Alternating_Bit_Protocol:
    def __init__(self):
        self.dfa=ltlf2dfa.DFA()
        self.target_formula="alternating bit protocol"
        self.construct_dfa()

    def construct_dfa(self):
        # alphabet
        alphabet="abcd" 
        """ 
        a = bit 0 
        b = bit 1
        c = bit 0 acknowledge
        d = bit 1 acknowledge
        """
        self.dfa.alphabet = [character for character in alphabet]
        self.dfa.Q = [0,1,2,3,4] # state 4 denotes rejecting state for all unalowed move
        self.dfa.q0 = 0
        self.dfa.F= [0,2] 
        self.dfa.delta = {
            0: {
                '0001': 0,
                '0010': 4,
                '0100': 4,
                '1000': 1,
                '0000': 0 # implements empty input
            },
            1: {
                '0001': 4,
                '0010': 2,
                '0100': 4,
                '1000': 1,
                '0000': 1 # implements empty input
            },
            2: {
                '0001': 4,
                '0010': 2,
                '0100': 3,
                '1000': 4,
                '0000': 2 # implements empty input
            },
            3: {
                '0001': 0,
                '0010': 4,
                '0100': 3,
                '1000': 4,
                '0000': 3 # implements empty input
            },
            4: {
                '0001': 4,
                '0010': 4,
                '0100': 4,
                '1000': 4,
                '0000': 4 # implements empty input
            }
        }
        