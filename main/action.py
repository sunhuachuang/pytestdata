# create insert data.
# writed by sunhuachuang #

# @params fields [{}, {}]
# @return ([field_names], [[value1, value2],[]...])
def create_data(fields, number):
    field_names = []
    field_values = []

    # test
    field_names = ['name', 'age']
    field_values = [['zhangsan', 24], ['lisi', 56], ['wang', 74]]

    return field_names, field_values
