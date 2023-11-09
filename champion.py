class Champion:
    def __init__(self, name, tier, frontline=False, items=None):
        self.name = name
        self.tier = tier  # Tier attribute ranging from 1 to 5
        self.frontline = frontline
        self.items = items if items is not None else []

    def __str__(self):
        # This method allows us to print the champion object neatly
        return f'Champion(name={self.name}, tier={self.tier}, frontline={self.frontline}, items={self.items})'
