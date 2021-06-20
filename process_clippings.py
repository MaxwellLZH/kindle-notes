from dataclasses import dataclass, field, replace
import re
from difflib import SequenceMatcher
import itertools


@dataclass(frozen=True, order=True)
class Clipping:
	book_name: str
	start_pos: int
	end_pos: int
	content: str


def combine_clippings(a, b):
	start_pos = min(a.start_pos, b.start_pos)
	end_pos = max(a.end_pos, b.end_pos)
	c_a, c_b = a.content, b.content
	if a.start_pos > b.start_pos:
		c_a, c_b = c_b, c_a
	match = SequenceMatcher(None, c_a, c_b).find_longest_match(0, len(c_a), 0, len(c_b))
	match_content = c_a[match.a: match.a+match.size]
	c_a = c_a.replace(match_content, '')
	content = c_a + c_b
	return Clipping(a.book_name, start_pos, end_pos, content)


def filter_clipping(clipping):
	return len(clipping.content) > 5


def preprocess_content(content):
	# 开头结尾的符号
	content = re.sub('^[,.。，\s]+', '', content)
	content = re.sub('[,.。，\s]+$', '', content)
	return content


def preprocess_clipping(clipping):
	return replace(clipping, content=preprocess_content(clipping.content))


def get_clippings(note_path):
	all_clippings = []
	with open(note_path, 'r') as f:
		text = f.read()
		for block in text.split("==========\n")[1: ]:
			try:
				lines = block.split('\n')
				if len(lines) <= 1:
					continue
				# 书名有分行符
				while '添加于' not in lines[1]:
					s = lines[0]
					lines = lines[1: ]
					lines[0]= s.strip() + lines[0]

				book_name = lines[0].strip()
				numbers = re.findall(r'[0-9]+', lines[1])
				start_pos, end_pos = numbers[0], numbers[1]
				start_pos, end_pos = int(start_pos), int(end_pos)
				content = '\n'.join([l for l in lines[2:] if l.strip()])
				
				c = Clipping(book_name, start_pos, end_pos, content)
				all_clippings.append(c)
			except:
				print(lines)
				print(numbers)
				raise

	clippings = set()

	for c_a, c_b in itertools.combinations([c for c in all_clippings if filter_clipping(c)], 2):
		if c_a.book_name == c_b.book_name and c_a.start_pos <= c_b.start_pos and c_a.end_pos > c_b.start_pos:
			clippings.add(combine_clippings(c_a, c_b))
		else:
			clippings.add(c_a)
			clippings.add(c_b)

	return clippings



if __name__ == '__main__':
	note_path = './data/My Clippings.txt'
	print(get_clippings(note_path))




