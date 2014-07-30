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
parser.add_argument('name', metavar='D', type=str, nargs="+",
                    help='the name of the dataset [REGEX]')
parser.add_argument('-d', dest='savedir', 
                    help='directory to save downloaded files')


def get_data(name, savedir):
    directory = savedir + name + '\\'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = '%s/%s/%s' %(url,name,name)
    save_target = directory + name
    print name + data_suffix + " -> " + save_target + data_suffix
    data = urllib.urlretrieve(file_name + data_suffix, save_target + data_suffix)
    print name + names_suffix + " -> " + save_target + names_suffix
    names = urllib.urlretrieve(file_name + names_suffix, save_target + names_suffix)

def get_cell_str(cell):
    return cell.text.encode('ascii','ignore')#.replace(u'\xa0',u' ').encode('utf-8')

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
            dataset[cats[idx]] = cell.text.encode('ascii','ignore')
        if dataset != {}:
            data.append(dataset)
            
    outf = open('sets.p','wb')
    pickle.dump(data, outf)
    outf.close()
    print " Done."
    return data
    

def main(argv):
    args = parser.parse_args()
    savedir = args.savedir
    names = args.name

    if savedir is None:
        savedir = os.getcwd()
    if not savedir.endswith('/') or not savedir.endswith('\\'):
        savedir += '\\'

    metadata = []
    if os.path.isfile('sets.p'):
        pckl = open("sets.p","rb")
        metadata = pickle.load(pckl)
        pckl.close()
    else:
        metadata = get_meta()
    
    p = re.compile(names[0])
    sets = []
    for ds in metadata:
        if p.match(ds['Name']):
            sets.append(ds['Name'])

    if len(sets) > 0:
        length = len(sets)
        print "Fetching " + str(length) + " matching dataset" + ('s.' if length > 1 else '.');
    else:
        print "no matches found for " + names[0]
    
    for n in sets:
        get_data(n, savedir)

if __name__ == '__main__':
    main(sys.argv[1:])
    
