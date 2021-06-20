from process_clippings import get_clippings
from process_mobi import convert_clipping_to_markdown


note_path = './data/My Clippings.txt'
book_name = '自控力（经典套装三册） (凯利·麦格尼格尔, SoBooKs.cc)'
mobi_file = '/Users/liuzhehao/Documents/uphill/kindle-notes/output/mobi7/book.html'
output_path = './test.md'


notes = []
for c in get_clippings(note_path):
	if c.book_name == book_name:
		m = convert_clipping_to_markdown(soup=mobi_file,
										 clipping=c,
										 title_tags=('b', ))

		notes.append(m)


with open(output_path, 'w') as f:
	f.write('\n'.join(notes))



