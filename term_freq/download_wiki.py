import httplib2
import re


def download(min, max):
    url = "http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/TV/2006/{}-{}".format(min, max)
    res = []
    h = httplib2.Http()
    rsp, content = h.request(url)
    prog = re.compile(r'<tr>\s+<td>(?P<id>\d+)[^<]*</td>\s+<td><a[^>]+>(?P<word>.+?)</a></td>\s+<td>(?P<freq>\d+)</td>')
    for m in prog.finditer(content):
        if min + len(res) != int(m.group('id')):
            print(m.groupdict(), len(res), min)
            return []
        else:
            res.append(m.groups())
    if len(res) != (max - min + 1):
        print("error {}-{}, got {}".format(min, max, len(res)))
        return []
    else:
        print("ok {}-{}, got {}".format(min, max, len(res)))
        return res

pages = [(1, 1000), (1001, 2000), (2001, 3000), (3001, 4000), (4001, 5000), (5001, 6000), (6001, 7000), (7001, 8000), (8001, 9000), (9001, 10000), (10001, 12000), (12001, 14000), (14001, 16000), (16001, 18000), (18001, 20000), (20001, 22000), (22001, 24000), (24001, 26000), (26001, 28000), (28001, 30000), (30001, 32000), (32001, 34000), (34001, 36000), (36001, 38000), (38001, 40000), (40001, 41284)]

f = open('term_freq.csv', 'w')
for min, max in pages:
    for item in download(min, max):
        f.write(','.join(item) + '\n')
f.close()
#download(20001, 22000)
