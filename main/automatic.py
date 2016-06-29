# automatic distinguish fileds type.
# writed by sunhuachuang #

# descs
# name     => str
# key      => str (pri or other)
# type     => tuple (typename, params) int str float datetime date bool text enum
# default  => str
# nullable => bool (True or False)
# extra    => str

#results
# name        => str
# type        => str
# min         => int
# max         => int
# default     => str
# nullable    => bool
# unique      => bool
# foreign_key => str (table_name)
# language    => str

# @param descs([{}, {}])
# @return [{},]
def analyze(descs):
    results = []
    for desc in descs:
        result = {}
        result['name']        = desc['name']
        result['type']        = 'email'
        result['min']         = 23
        result['max']         = 44
        result['default']     = 'some'
        result['nullable']    = True
        result['unique']      = False
        result['foreign_key'] = ''
        result['language']    = 'zh_cn'

        results.append(result)
    return results
