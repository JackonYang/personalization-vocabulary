import os
import requests


url_ptn = 'https://www.collinsdictionary.com/dictionary/english/%s'
data_dir = 'raw_html_rsp'

if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    

def download(word):
    url = url_ptn % word
    rsp = requests.get(url)
    return rsp.text


def main(word):
    key = word
    page_content = download(key)

    filename = os.path.join(data_dir, '%s.html' % key)
    with open(filename, 'w') as f:
        f.write(page_content)
    print('saved to: %s' % filename)
    

if __name__ == '__main__':
    main('leave')