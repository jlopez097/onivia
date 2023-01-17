def remove_none_values(d):
    for key in list(d.keys()):
        if d[key] is None or d[key]==[]:
            d.pop(key)
        elif isinstance(d[key], dict):
            remove_none_values(d[key])
        elif isinstance(d[key], list):
            for x in d[key]:
                remove_none_values(x)
    return d