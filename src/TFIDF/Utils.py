from DatabaseOperations import getTagname


def dateWeightGenerator(date):
    """Assuming the dates range from 2006-2009"""
    date_arr = date.split(' ')[0].split('-')
    year_ratio = {'2006': 0.1, '2007': 0.2, '2008': 0.3, '2009': 0.4}
    month_ratio = {'01': 1.0/12, '02': 2.0/12, '03': 3.0/12, '04': 4.0/12,
                   '05': 5.0/12, '06': 6.0/12, '07': 7.0/12, '08': 8.0/12,
                   '09': 9.0/12, '10': 10.0/12, '11': 11.0/12,'12': 12/12}
    return (month_ratio[date_arr[1]]*0.1) + float(year_ratio[date_arr[2]])

def sortedDict(dictToSort, cursor):
    for key, value in sorted(dictToSort.iteritems(), key=lambda (k,v): (v, k), reverse=True):
            print "%s: %s" % (getTagname(key,cursor), value)
