import envoy
import re

done = {}

def rewriteLine(path, lineNo, ident):
	key = '%s%d%s' % (path,lineNo,ident)
	if key in done:
		return
	done[key] = True
	print path, lineNo, ident
	infile = open(path)
	outfile = open('tmp.go', 'w')
	i = 1
	changed = False
	for line in infile:
		if i == lineNo:
			before = line
			print 'before', line
			line = re.sub(r"([^a-zA-Z0-9_\.])%s([^a-zA-Z0-9_])" % ident, r"\1m.%s\2" % ident, line)
			if line != before:
				changed = True
			print 'after', line
		outfile.write(line)
		i = i + 1
	infile.close()
	outfile.close()
	envoy.run('mv tmp.go ' + path)
	return changed

def main():
	anyChanged = True
	while anyChanged:
		anyChanged = False
		r = envoy.run('go test el/components/...')
		print r.std_err
		for l in r.std_err.split('\n'):
			if 'undefined:' not in l:
				continue
			components = l.split(':')
			path = '/Users/reilly/league/services/' + components[0][9:]
			lineNo = int(components[1])
			ident = components[-1].strip()
			if rewriteLine(path, lineNo, ident):
				anyChanged = True

if __name__ == '__main__':
	main()