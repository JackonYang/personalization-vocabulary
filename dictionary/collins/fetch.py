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


def main(word, retry=3):
    """
    return skipped: True/False
    """
    word = word.strip()
    key = word
    filename = os.path.join(data_dir, '%s.html' % key)

    if os.path.exists(filename):
        return True

    for i in range(retry):
        try:
            page_content = download(key)
        except Exception as e:
            page_content = ''
            print('error: %s, %s' % (word, e))
        else:
            break

    if page_content:
        with open(filename, 'w') as f:
            f.write(page_content)
        print('saved to: %s' % filename)
    else:
        print('skip %s' % word)

    return False


if __name__ == '__main__':
    main('leave')
