import sys
sys.path.append('../colify')

import pytest
from colify import Colify

spain = ["madrid", "barcelona", "bilbao", "Malaga"]
italy = ["rome", "florence", "milan", "venice", "palermo", "padua"]
france = ["paris", "lyon", "toulouse", "nantes"]
countries = {}
countries['spain'] = spain
countries['italy'] = italy
countries['france'] = france

def test_max_rows():
	c = Colify(countries)
	# length of the longest array 
	assert(c.max_rows() == 6)

def test_max_column_width():
	c = Colify(countries)
	# length of longest word in any array (barcelona)
	assert(c.max_column_width() == 9)

def test_output_string():
	c = Colify(countries)
	# {} is a placeholder for the string format() function  
	# :>9 indicates the spacing of each cell and is based off max_column_width()
	# | is literal pipe char (visual seperator) 
	assert(c.output_string() =="{:>9} | ") 

def test_print_headers(capsys):
	c = Colify(countries)
	c.print_headers()
	out, err = capsys.readouterr()
	# \x1b[4m is a control character to begin underlining text
	# | is literal pipe char (visual seperator) 
	# \x1b[0m is a control character to stop underlining text 
	# \n is a newline
	assert(out == "\x1b[4m|     SPAIN |     ITALY |    FRANCE | \x1b[0m\n" )

def test_build_line():
	c = Colify(countries)
	line = c.build_line(1)
	# one cell per array
	assert(line[0] == "| {:>9} | {:>9} | {:>9} | ")
	# values should be the second item in each array (index 1)
	assert(line[1] == ['barcelona', 'florence', 'lyon'])

def test_print_body(capsys):
	spec_output = (
		"|    madrid |      rome |     paris | \n"
		"| barcelona |  florence |      lyon | \n"
		"|    bilbao |     milan |  toulouse | \n"
		"|    Malaga |    venice |    nantes | \n"
		"|           |   palermo |           | \n"
		)
	c = Colify(countries)
	c.print_body()
	out, err = capsys.readouterr()
	assert(out == spec_output)
