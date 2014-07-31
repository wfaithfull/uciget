# Python 2.7 script to download datasets from UCI machine learning repo.
# Author: Will Faithfull
#
# http://faithfull.io/
import sys, urllib, urllib2, os, argparse, pickle, re
from bs4 import BeautifulSoup

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases'
meta = 'http://archive.ics.uci.edu/ml/datasets.html'
data_suffix = '.data'
names_suffix = '.names'
args_def = 'd:bc'

parser = argparse.ArgumentParser(description='Get datasets from UCI repository.')
parser.add_argument('-n', dest='name', type=str, nargs="+",
                    help='the name of the dataset [REGEX]')
parser.add_argument('-d', dest='savedir', type=str,
                    help='directory to save downloaded files')
parser.add_argument('-c', dest='category', type=str,
                    help='category (default task) [REGEX]')


def get_data(name, savedir):
    directory = savedir + name + '\\'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = '%s/%s/%s' %(url,name,name)
    save_target = directory + name
    print file_name + data_suffix + " -> " + save_target + data_suffix
    data = urllib.urlretrieve(file_name + data_suffix, save_target + data_suffix)
    print file_name + names_suffix + " -> " + save_target + names_suffix
    names = urllib.urlretrieve(file_name + names_suffix, save_target + names_suffix)

def get_cell_str(cell):
    return cell.text.encode('ascii','ignore')#.replace(u'\xa0',u' ').encode('utf-8')

def print_dict(d):
    for x in d:
        print x
        for y in d[x]:
            print y + ':' + d[x][y]

def get_meta():
    print "Retrieving metadata...",
    html = urllib2.urlopen(meta).read()
    
    bs = BeautifulSoup(html)

    table = bs.findAll(
        lambda tag: tag.name=='table' and
        tag.has_attr('border') and
        tag.has_attr('cellpadding'))[1]

    rows = table.findAll(lambda tag: tag.name=='tr')
    categories = rows[0].findChildren('td')

    cats = []
    for cell in categories:
        cats.append(get_cell_str(cell))

    data = []
    
    for row in rows[1:]:
        cells = row.findChildren('td')
        dataset = dict()
        for idx, cell in enumerate(cells[2:], start=0):
            dataset[cats[idx]] = cell.text.encode('ascii','ignore') #.replace(u'\xa0', u' ')
        if dataset != {}:
            data.append(dataset)
    pickle.dump(data, open('sets.p','wb'))
    print " Done."
    return data
    

def main(argv):
    args = parser.parse_args()
    savedir = args.savedir
    names = args.name
    category = args.category

    if names is None:
        names = [''];

    if savedir is None:
        savedir = os.getcwd()
    if not savedir.endswith('/') or not savedir.endswith('\\'):
        savedir += '\\'

    if category is None:
        category = '';

    metadata = []
    if os.path.isfile('sets.p'):
        metadata = pickle.load(open("sets.p","rb"))
    else:
        metadata = get_meta()
    
    p = re.compile(names[0])
    cp = re.compile(category)
    sets = []
    for ds in metadata:
        if p.match(ds['Name']) and cp.match(ds['Default Task']):
            sets.append(ds['Name'])

    if len(sets) > 0:
        print "found: " + str(sets)
    else:
        print "no matches found."
    
    for n in sets:
        get_data(n, savedir)

if __name__ == '__main__':
    main(sys.argv[1:])
    
