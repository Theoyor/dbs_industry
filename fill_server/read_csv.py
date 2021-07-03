import csv
import decimal
from os import read, remove
def read_file(filename):
    
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        ret = []
        for row in csv_reader:
            ret.append(row) 
#            print(f'{", ".join(row)}')
            line_count += 1

        print(f'Processed {line_count} lines.')
    return ret


def read_file_to_dict(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        ret = {}
        line_count = 0
        for row in csv_reader:
#            print(f'\t{row["country"]},{row["code"]}')
            ret[row["code"]] = row["country"]
            line_count += 1
#        print(ret)
        print(f'Processed {line_count} lines.')
    return ret

def to_int(list, col):
    for row in list:
        if row[col] != '':
            row[col] = int(row[col])
        else:
            row[col] = int('nan')

def to_float(list, col):
    for row in list:
        if row[col] != '':
            row[col] = decimal.Decimal(row[col])
        else:
            row[col] = decimal.Decimal('nan')

def elongate(list, years):
    ret = []
    for country in list:
        for i in range(1, len(country)-1):
            tmp = []
            tmp.append(country[0])
            tmp.append(years[i])
            tmp.append(country[i])
            ret.append(tmp)
    return ret


# uses country code 
def remove_non_countries(list, col_of_code, countries):
    ret = []
    for row in list:
        if row[col_of_code] in countries:
            ret.append(row)  
    return ret

def to_code(list, countries, col ):
    rev_countries =  dict((v,k) for k,v in countries.items())
    ret = []
    for row in list:
        if row[col] in rev_countries:
            row[col] = rev_countries[row[col]]
            ret.append(row)
#        else:
#            print(row[col])
    return ret
            

def read_countries():
    return read_file_to_dict("./data/countries.csv")


def read_emission(countries):
    values = read_file("./data/co2_emission.csv")
    values = remove_non_countries(values, 1,countries)
    ret = {}
    for i in range(len(values)):
        del values[i][0]
    to_int(values, 1)
    to_float(values, 2)
    for row in values:
        if row[0] not in ret:
            ret[row[0]] = {}
        ret[row[0]][row[1]] = row[2]
#        print(row)
#        print(ret[row[0]])
    return values


def read_gdp(countries):
    values = read_file("./data/gdp.csv")
    ret = {}
    for i in range(len(values)):
       del values[i][0]
       del values[i][1]
       del values[i][1]
    head = values[0]
    values = remove_non_countries(values, 0,countries)
    values = elongate(values, head)
    to_int(values, 1)
    to_float(values, 2)
    for row in values:
        if row[0] not in ret:
            ret[row[0]] = {}
        ret[row[0]][row[1]] = row[2]
#        print(row)
#        print(ret[row[0]])
    return ret


def read_industry(countries):
    values = read_file("./data/industry.csv")
    ret = {}
    for i in range(len(values)):
       del values[i][0]
       del values[i][1]
       del values[i][1]
    head = values[0]
    values = remove_non_countries(values, 0,countries)
    values = elongate(values, head)
    to_int(values, 1)
    to_float(values, 2)
    for row in values:
        if row[0] not in ret:
            ret[row[0]] = {}
        ret[row[0]][row[1]] = row[2]
#        print(row)
#        print(ret[row[0]])
    return ret


def read_country_data(countries):
    values = read_file("./data/country_data.csv")
    values = remove_non_countries(values, 0,countries)
    ret = {}
    for i in range(len(values)):
        del values[i][3]
        del values[i][3]
        del values[i][3]
    for row in values:
        if row[0] not in ret:
            ret[row[0]] = {}
        ret[row[0]]["reg"] = row[1]
        ret[row[0]]["inc"] = row[2]
#        print(row)
#        print(ret[row[0]])
    return ret

def read_population_total(countries):
    values = read_file("./data/population_total.csv")
    values = to_code(values[1:], countries, 0)
    ret = {}
    to_int(values, 1)
    to_int(values, 2)
    for row in values:
        if row[0] not in ret:
            ret[row[0]] = {}
        ret[row[0]][row[1]] = row[2]
#        print(row)
#        print(ret[row[0]])
    return ret

def read_sectors(countries):
    values = read_file("./data/sectors.csv")
    values = to_code(values, countries, 0)
    ret = {}
    for i in range(len(values)):
        del values[i][1]
        del values[i][4]
        del values[i][4]
        del values[i][4]
    to_float(values, 1)
    to_float(values, 2)
    to_float(values, 3)
    for row in values:
        if row[0] not in ret:
            ret[row[0]] = {}
        ret[row[0]]["agr"] = row[1]
        ret[row[0]]["ind"] = row[2]
        ret[row[0]]["ser"] = row[3]
#        print(row)
#        print(ret[row[0]])
    return ret
