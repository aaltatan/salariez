
class ViewSetMixin:

    """
    utility class to implement list(table) view and its functionality.  
    
    ### required attributes:  
    - `filter_class: FilterSet`
    
    ### optional attributes:  
    - `serializer_class: Serializer`
    - `read_serializer_class: Serializer`
    - `write_serializer_class: Serializer`

    """

    def filter_queryset(self, queryset):
        return self.filter_class(
            self.request.GET or self.request.POST
        ).qs

    def get_serializer_class(self):

        if getattr(self, 'serializer_class', None) is not None:
            return self.serializer_class
        
        read_serializer_exists: bool = hasattr(
            self, 'read_serializer_class'
        )
        write_serializer_exists: bool = hasattr(
            self, 'write_serializer_class'
        )

        if not read_serializer_exists and not write_serializer_exists:
            raise NotImplementedError(
                'you must implement serializer_class or read_serializer_class and write_serializer_class'
            )

        if self.action in ('list', 'retrieve'):
            return self.read_serializer_class
            
        return self.write_serializer_class