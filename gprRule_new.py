

def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

def outerParenthes_span(string):
	stack = []
	output=[]
	for i, c in enumerate(string):
		if c == '(':
			stack.append(i)
		elif c == ')' and stack:
			start = stack.pop()
			if len(stack)==0:
				output.append([start,i])
	yield (output)
			
def parenthetic_parseContents(string):
	stack = []
	oldRule=[]
	newRule=[]
	for i, c in enumerate(string):
		if c == '(':
			stack.append(i)
		elif c == ')' and stack:
			start = stack.pop()
			txt=string[start + 1: i]
			if newRule and oldRule:
				txt=txt.replace(oldRule[0],newRule[0])
				result=re.findall(r'\(\s\w\s\)',text)
				if result:
					for subTxt in result:
						text=text.replace(subTxt,re.search(r'\w',subTxt).group())
				oldRule.pop()
				newRule.pop()
			seen=set()
			output=[]
			if ('(')in txt.split():
				parentheticSpan=list(outerParenthes_span(txt))
				flat_spanlist = [item for sublist in parentheticSpan for item in sublist]
				i=0
				while i<len(flat_spanlist)-1:
					start=flat_spanlist[i]
					end=flat_spanlist[i+1]
					span=[start,end]
					if span in parentheticSpan:
						if txt[start:end] not in seen:
							output.append(txt[start:end+1])
							seen.add(txt[start:end+1])
					elif 'and' in txt[start:end]:
						operet=' and '
						for word in txt[start:end].split('and'):
							if word.strip() not in seen:
								output.append(word.strip())
								seen.add(word.strip())
					elif 'or' in txt[start:end]:
						operet=' or '
						for word in txt[start:end].split('or'):
							if word.strip() not in seen:
								output.append(word.strip())
								seen.add(word.strip())
				i+=1
				if len(stack)>0:
					oldRule=oldRule+[txt]
					newRule=newRule+[operet.join(output)]
				else:
					yield (operet.join(output))
			elif 'and' in txt:
				operet=' and '
				for word in txt.split(' and '):
					if word.strip() not in seen:
						output.append(word.strip())
						seen.add(word.strip())
				if len(stack)>0:
					oldRule=oldRule+[txt]
					newRule=newRule+[operet.join(output)]
				else:
					yield (operet.join(output))
			elif 'or' in txt:
				operet=' or '
				for word in txt.split('or'):
					if word.strip() not in seen:
						output.append(word.strip())
						seen.add(word.strip())
				if len(stack)>0:
					oldRule=oldRule+[txt]
					newRule=newRule+[operet.join(output)]
				else:
					yield (operet.join(output))
