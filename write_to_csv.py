import csv, os


def writeToCsv(content, heading = ['Medicine', 'Summary']):

    '''
    content needs to be in the form of [{"Medicine": "name", "Summary": "stuff"}, ...]
    '''

    i = 0
    while os.path.exists(f'Database summary{i}.csv'):
        i += 1

    file = f'Database summary{i}.csv'

    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = heading)
        writer.writeheader()
        writer.writerows(content)
    
