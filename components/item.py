class Item:
    """
    Stores function and its kwargs associated with an item.
    """
    def __init__(self, use_function=None, equip=False, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.equip = equip
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
