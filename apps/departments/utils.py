def get_absolute_parent(obj):
    """
    recursive function to get absolute parent for given object
    """
    if obj.parent is None:
        return obj
    return get_absolute_parent(obj.parent)

