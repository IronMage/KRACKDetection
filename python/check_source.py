f_name = raw_input("File to be checked: ")

with open(f_name) as fp:
	for i, line in enumerate(fp):
		if '\xe2' in line:
			print i, repr(line)
