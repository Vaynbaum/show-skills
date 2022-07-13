import random
import string


class GeneratorHandler:
    def generate_random_combination(self, length: int) -> str:
        """Generating a random string with a given length

        Args:
            length (int): String length

        Returns:
            str: Random string
        """        
        letters = string.ascii_lowercase
        rand_string = "".join(random.choice(letters) for i in range(length))
        return rand_string
