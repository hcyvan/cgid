from config import const


def create_value(values, ftypes):
    if len(values) != len(ftypes):
        raise Exception('csv2sql config: values and ftypes have different length!')
    value_insert = []
    for i, value in enumerate(values):
        if ftypes[i] == 'string':
            value_format = "'{}'".format(value)
        elif ftypes[i] == 'geometry:point':
            value_format = "ST_GeomFromText('POINT({})', {})".format(
                value, const.get('SRID'))
        elif ftypes[i] == 'geometry:polygon':
            value_format = "ST_GeomFromText('POLYGON{}', {})".format(
                value[1:-1], const.get('SRID'))
        else:
            value_format = value
        value_insert.append(value_format)
    return '({})'.format(', '.join(value_insert))
