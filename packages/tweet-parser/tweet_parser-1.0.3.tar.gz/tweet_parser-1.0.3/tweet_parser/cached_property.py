class cached_property():
    """
    Descriptor (non-data) for building an attribute on-demand on first use.
    https://stackoverflow.com/questions/4037481/caching-attributes-of-classes-in-python
    """
    def __init__(self, factory):
        """
        <factory> is called such: factory(instance) to build the attribute.
        """
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        # Build the attribute.
        attr = self._factory(instance)

        # Cache the value; hide ourselves.
        setattr(instance, self._attr_name, attr)

        return attr