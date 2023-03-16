def validate_input_numeric(new_value):
    '''Verifica que el carácter que está ingresando el usuario
    es numerico o vacio, ingresa:
    new_value = char'''
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False

