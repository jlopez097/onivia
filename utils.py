from dataclasses import asdict

def snake_to_camelcase(w):
    l = w.split("_")
    return "".join([x.capitalize() if i >= 1 else x for i, x in enumerate(l)])

def snake_to_camelcase_dict(d):
    
    if type(d) is dict:   
        return dict([(snake_to_camelcase(k),snake_to_camelcase_dict(v)) for k,v in list(d.items())])
    else:
        return d
