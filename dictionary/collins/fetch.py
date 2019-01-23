import os
import requests


url_ptn = 'https://www.collinsdictionary.com/dictionary/english/%s'
data_dir = 'raw_html_rsp'


if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def download(word):
    url = url_ptn % word
    # print('fetching %s' % word)
    rsp = requests.get(url, timeout=3)
    return rsp.text


def main(word):
    """
    return skipped: True/False
    """
    key = word
    filename = os.path.join(data_dir, '%s.html' % key)

    if os.path.exists(filename):
        return True

    page_content = download(key)

    with open(filename, 'w') as f:
        f.write(page_content)
    print('saved to: %s' % filename)
    return False


if __name__ == '__main__':
    main('leave')
