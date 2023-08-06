import re

def get_type(string):
	curly = string.find('{')
	square= string.find('[')
	paren = string.find('(')
	types = [curly, square]
	existing_types = []
	
	for t in types:
		if t != -1:
			existing_types.append(t)
			type_pos = sorted(existing_types)
			typ = string[type_pos[0]]

	opposites = {'{':'}','[':']', '(':')'}
	opposite = opposites[typ]
	
	return {
		'typ': typ,
		'opposite': opposite,
		'index': type_pos[0]
	}

def get_string_contents(string, start):
    first_single = string.find("'", start)
    first_double = string.find('"', start)
    first = None
    if first_single == -1 and first_double == -1:
        return -1
    elif first_single == -1:
        first = { 't': '"', 'i': first_double }
    else:
        first = { 't': "'", 'i': first_single }

    last = string.find(first['t'], first['i'] + 1)
    return string[first['i']:last + 1]

def get_variable(string, data):
    if len(data['target']) == 1:
        query = data['target'][0]
    candidates = [(m.start(0), m.end(0)) for m in re.finditer(r'' + query +'', string)]

    for c in candidates:
        lh_start = c[0]
        lh_end = c[1]
        rh_start = None
        def check_next(end):
            relevant_string = string[end:]
            if relevant_string[1] in [' ','"', "'"]:
                end += 1
                return check_next(end)
            elif relevant_string[1] in [':', '=']:
                end += 1
                nonlocal rh_start 
                rh_start = end + 1
                return True
            else:
                return False
        is_valid = check_next(lh_end)
        if is_valid:
            break

    rh_end = string.find('\n', rh_start) 
    if string[rh_end - 1:] == ',':
        rh_end -= 1

    return {
        'lh_start': lh_start,
        'lh_end': lh_end,
        'rh_start': rh_start,
        'rh_end': rh_end,
        'string': string[lh_start:rh_end],
        'lh_string': string[lh_start:lh_end],
        'rh_string': string[rh_start:rh_end]
    }

def get_brackets(string, start = 0):
	typ = get_type(string[start:])
	block_start = start + typ['index']
	
	pos = block_start

	depth = 0
	while depth != -1:
		closing = string.find(typ['opposite'], pos + 1)
		child   = string.find(typ['typ']     , pos + 1)

		if child == -1:
			depth -= 1
			pos = closing
		elif child < closing:
			depth += 1
			pos = child
		else:
			depth -= 1
			pos = closing

	return { 'start': block_start, 'stop': pos }

def list_index_positions(string, start, stop):
	li = string[start:stop]
	positions = []
	quoted = False
	nested = 0
	
	for i, c in enumerate(li):
		# ignore commas in strings
		if c in ['"', "'"]:
			quoted = not quoted

		# find child elements
		elif c in ['[','{','('] and len(positions) > 0:
			nested += 1
		elif c in [']','}',')']:
			nested -= 1

		# this is index 0
		elif c == '[' and len(positions) == 0:
			positions.append(i + start + 1)
		# add any remaining indices detected.
		elif c == ',' and quoted == False and nested <= 0:
			positions.append(i + start + 1)

	return positions

def detect_duplicate(target, content):
	raw_compare = target.find(content) != -1
	if raw_compare:
		return True
	else:
		clean_content = (content
			.replace('\n','')
			.replace('\t','')
			.replace(',','')
			.replace(' ','')
			.replace('"','')
			.replace("'",""))

		return target.find(clean_content) != -1
