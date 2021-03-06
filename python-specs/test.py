import os
import time

USER = 'specs'
LANG = 'python'
NOTES = 'ugly. needs cleanup.'
PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'data',
    'all.csv'
)


def load_data():
    with open(PATH) as f:
        temp = [
            l for l in f.readlines()
            if not l.startswith('StnID')
            and ',' in l
            and float(l[12:19]) > 45.0000
        ]

    return temp


def transform_data(temp):
    data = {}
    for row in temp[1:]:
        x = row.split(',')
        if x[1] == 'Lat' or float(x[1]) > 45.0:
            if x[0] not in data:
                data[x[0]] = 0
            data[x[0]] += sum(1 for t in x[6::5] if float(t) > 0.0)

    return data


def print_results(result, runtime):
    print('{}, {}, {}, {} ms, {}'.format(USER, LANG, result, runtime, NOTES))


start = int(round(time.time() * 1000))
temp = load_data()
data = transform_data(temp)
data = sorted(
    [
        {
            'station': k,
            'total': v
        }
        for k, v in data.items()
    ],
    key=lambda k: k['total'],
    reverse=True
)
end = int(round(time.time() * 1000)) - start
print_results(data[0]['station'][3:], end)
