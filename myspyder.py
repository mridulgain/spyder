import sys

def remove_html_markup(txt):
	tag = False
	quote = False
	out = ""
	
	for c in txt:
		if c == '<' and not quote:
			tag = True
		elif c == '>' and not quote:
			tag = False
		elif (c == '"' or c == "'") and tag:
			quote = not quote
		elif not tag:
			out = out + c
	
	return out

stepping = True
breakpoints = {9:True}

def debug(command, my_locals):#accesses the states of debugger
	global stepping
	global breakpoints
	
	if command.find(' ') > 0:
		arg = command.split(' ')[1]
	else:
		arg = None
		
	if command.startswith('s'):
		stepping = True
		return True
	elif command.startswith('c'):
		stepping = False
		return True
	elif command.startswith('q'):
		sys.exit(0)
	else:
		print "No such command", repr(command)

def input_command():
	command = raw_input("(my-spyder) ")
	return command
	
def traceit(frame, event, arg):
	#print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals	
	global stepping
	global breakpoints
	#frame.f_locals["tag"] = True
	#print frame.f_locals
	
	if event == 'line':
		if stepping or breakpoints.has_key(frame.f_lineno):
			resume = False
			while not resume:
				print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
				command = input_command()
				resume = debug(command, frame.f_locals)
	return traceit
				
sys.settrace(traceit)
print remove_html_markup('<b>xyz</b>')
sys.settrace(None)
