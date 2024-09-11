def generate_department_id(instance):
    
    if instance.department_id != '':
        return instance
    
    Klass = instance.__class__
    last_sibling = (
        Klass
        .objects
        .filter(parent=instance.parent)
        .exclude(pk=instance.pk)
        .last()
    )
    
    if last_sibling:
        instance.department_id = str(int(last_sibling.department_id) + 1)
        return instance

    if instance.parent is not None:
        instance.department_id = instance.parent.department_id + str(1)
        return instance
    
    instance.department_id = '1'
    return instance