from django.core.validators import URLValidator
from django.core.exceptions import ValidationError



def urlvalidator(urladdress):
    validate = URLValidator()
    
    try:
        validate(urladdress)
        return True
    except ValidationError as exception:
        return False
