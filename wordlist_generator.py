import itertools

class WordlistGenerator:
    def __init__(self, user_inputs):
        self.user_inputs = user_inputs
        self.leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$']
        }
    
    def _apply_leet(self, word):
        """Generate leetspeak variations of a word"""
        variations = [word]
        for char in word:
            if char.lower() in self.leet_map:
                new_vars = []
                for variant in variations:
                    for leet_char in self.leet_map[char.lower()]:
                        new_vars.append(variant.replace(char, leet_char))
                variations += new_vars
        return set(variations)
    
    def _add_suffixes(self, word):
        """Append numbers and years to words"""
        suffixes = [str(i) for i in range(0, 100)] + \
                   [str(year) for year in range(2020, 2026)]
        return [word + suffix for suffix in suffixes]
    
    def generate(self):
        """Generate all word combinations"""
        words = set()
        
        # Base words + leetspeak
        for word in self.user_inputs:
            words.add(word)
            words.update(self._apply_leet(word))
            words.add(word[::-1])  # Reversed
        
        # Add number suffixes
        expanded_words = []
        for word in words:
            expanded_words.append(word)
            expanded_words.extend(self._add_suffixes(word))
        
        # Combine words (e.g., "john" + "doe" = "johndoe")
        for combo in itertools.product(expanded_words, repeat=2):
            combined = ''.join(combo)
            expanded_words.append(combined)
        
        return set(expanded_words)
