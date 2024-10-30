from django.db.models import F, Value
from django.db.models.functions import Concat


def join_db(*args: tuple[str], separator: str = ' ') -> Concat:
    """
    concatenate given arguments with a default separator in database level
    """
    concat_args = []

    for idx, arg in enumerate(args, 1):
        
        concat_args.append(F(arg))

        is_last = idx == len(args)
        
        if not is_last:
            concat_args.append(Value(separator))
    
    return Concat(*concat_args)