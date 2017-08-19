class Item:
    """
    Item component for entities.
    Stores function and its kwargs associated with an item.
    """
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs

    def __repr__(self):
        return """{self.__class__.__name__}(use_function={self.use_function},\
            equip={self.equip}, targeting={self.targeting}, targeting_message={self.targeting_message},\
            kwargs={self.function_kwargs})""".format(self=self)
