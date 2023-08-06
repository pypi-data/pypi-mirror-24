import sys

# pycube90 v0.1.1

class Cube:
    def __init__(self, key):
        self.key_list = []
        self.key = ""
        self.master_list = []
        self.alphabet_dict = {}
        self.alphabet_dict_rev = {}
        self.start_char = 32
        self.end_char = 91
        self.size_factor = 26
        for x in range(0,self.end_char):
            self.alphabet_dict[chr(x + self.start_char)] = x
            self.alphabet_dict_rev[x] = chr(x + self.start_char)

        def gen_cube(depth, width, length):
            for z in range(0,depth):
                section_list = []
                for y in range(0,width):
                    alphabet = []
                    for x in range(0,length):
                        alphabet.append(chr(x + self.start_char))
                    for mod in range(0,y):
                        shift = alphabet.pop(0)
                        alphabet.append(shift)
                        shift = alphabet.pop(2)
                        alphabet.insert(45,shift)
                    section_list.append(alphabet)
                self.master_list.append(section_list)

        gen_cube(26, 26, 90)
        self.init(key)

    def key_cube(self, key):
        for section in self.master_list:
            for char in key:
                char_value = self.alphabet_dict[char]
                sized_pos = char_value % self.size_factor
                for alphabet in section:
                    pos = alphabet.index(char)
                    key_sub = alphabet.pop(sized_pos)
                    alphabet.append(key_sub)
                    for y in range(0,char_value):
                        if y % 2 == 0:
                            shuffle = alphabet.pop(0)
                            alphabet.append(shuffle)
                            shuffle = alphabet.pop(2)
                            alphabet.insert(12,shuffle)
                for x in range(char_value):
                    section = self.master_list.pop(sized_pos)
                    newpos = (sized_pos + (x * 128)) % self.size_factor
                    self.master_list.insert(newpos,section)

    def load_key(self, skey):
        self.key = skey
        for element in self.key:
            self.key_list.append(element)

    def key_scheduler(self, key):
        sub_key = ""
        for element in key:
            pos = self.alphabet_dict[element]
            sized_pos = pos % self.size_factor
            section = self.master_list.pop(sized_pos)
            sub_alpha = section.pop(sized_pos)
            shift = sub_alpha.pop(1)
            sub_alpha.append(shift)
            section.insert(pos,sub_alpha)
            self.master_list.insert(sized_pos,section)
            sub = sub_alpha.pop(pos)
            sub_alpha.insert(pos,sub)
            sub_key += sub
        self.load_key(sub_key)
        return sub_key
    
    def init(self, key):
        self.load_key(key)
        self.key_cube(key)

    def morph_cube(self, counter, sub_key):
        mod_value = counter % self.size_factor
        for key_element in sub_key:
            key_value = self.alphabet_dict[key_element]
            shift_value = (mod_value + key_value) % self.size_factor
            for section in self.master_list:
                for alphabet in section:
                    shift = alphabet.pop(mod_value)
                    alphabet.insert(shift_value,shift)
            section_shift = self.master_list.pop(key_value % self.size_factor)
            self.master_list.append(section_shift)

    def encrypt(self, words):
        cipher_text = ""
        sub_key = self.key
        for word in words:
            for counter, letter in enumerate(word):
                for section in self.master_list:
                    for alphabet in section:
                        sub_pos = self.alphabet_dict[letter]
                        sub = alphabet.pop(sub_pos)
                        alphabet.insert(sub_pos,sub)
                        shift = alphabet.pop(0)
                        alphabet.append(shift)
                self.morph_cube(counter, sub_key)
                sub_key = self.key_scheduler(sub_key)
                cipher_text += sub
        return cipher_text

    def decrypt(self, words):
        plain_text = ""
        sub_key = self.key
        for word in words:
            for counter, letter in enumerate(word):
                for section in self.master_list:
                    for alphabet in section:
                        sub_pos = alphabet.index(letter)
                        sub = self.alphabet_dict_rev[sub_pos]
                        shift = alphabet.pop(0)
                        alphabet.append(shift)
                self.morph_cube(counter, sub_key)
                sub_key = self.key_scheduler(sub_key)
                plain_text += sub
        return plain_text
