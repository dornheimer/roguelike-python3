class Item:
    """
    Stores function and its kwargs associated with an item.
    """
    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs
