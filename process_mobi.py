from bs4 import BeautifulSoup
from process_clippings import preprocess_content
from difflib import SequenceMatcher


#################
# 用于解析mobi7
################

def make_soup(file):
    if isinstance(file, str):
        with open(file) as f:
            return BeautifulSoup(f, 'lxml')
    else:
        return file


def is_match(a, b, threshold=0.5):
    return SequenceMatcher(None, a, b).real_quick_ratio() > threshold


def find_tag_with_content(soup, content):
    soup = make_soup(soup)
    threshold = 0.6

    tags = soup.find_all(lambda tag: content in tag.text)

    while len(tags) == 0:
        tags = soup.find_all(lambda tag: is_match(content, tag.text, threshold=threshold))
        threshold /= 2
    
    return tags[-1]


def get_title_tag(soup, cur_tag, title_tags=('b', ), get_text=False):
    soup = make_soup(soup)
    cursor = cur_tag
    title = None

    while 1:
        cursor = cursor.previous_sibling
        
        if cursor is None:
            return None
        
        for elem in cursor.descendants:
            if elem.name in ('b', ) and len(elem.text) > 0:
                title = elem

        if title is not None:
            return title.text if get_text else title


MARKDOWN_TEMPLATE = """
#### {title}
{content}
"""


def convert_clipping_to_markdown(soup, clipping, title_tags=('b', )):
    content_tag = find_tag_with_content(soup, clipping.content)
    title_tag = get_title_tag(soup=soup,
                             cur_tag=content_tag,
                             title_tags=title_tags)
    return MARKDOWN_TEMPLATE.format(title=title_tag.text if title_tag is not None else '',
                                    content=preprocess_content(clipping.content))
