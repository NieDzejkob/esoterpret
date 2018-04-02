#!/usr/local/bin/python
"""

Esoterpret main program
Usage: ./esoterpret.py --help

Repository: https://github.com/Padarom/Esoterpret

"""

import argparse, os, sys

from esoterpret.language import Language
from esoterpret.terminal import Color

# Add current path to sys.path, so we can import modules
path = os.path.dirname(os.path.realpath(__file__))

def listLanguages():
	for item in os.listdir(path + "/modules"):
		if os.path.isdir(path + "/modules/" + item) and item != "__pycache__":
			try:
				language = Language(item)
				print("- %s%s %s(%s)" % (Color.BOLD, language.Config["name"], Color.NORMAL, item))
			except:
				pass

def useLanguage(language, code, initialization):
	try:
		lang = Language(language)
		interpreter = lang.Class(code, initialization)

		while not(interpreter.hasExecutionFinished()):
			interpreter.nextInstruction()

	except ImportError:
		print("No Interpreter found for %s." % language)
	except FileNotFoundError:
		print("Config file for %s could not be loaded." % language)
	except Exception as e: # Everything else
		print("[%s] %s" % (type(e).__name__, str(e)))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""
	Esoterpret, interpreter and debugger for esoteric programming languages""", 
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument("script",
	                    type=argparse.FileType("r"),
	                    nargs="?",
	                    help="script file to execute")

	parser.add_argument("--gui", 
	                    help="open the gui [WIP]",
	                    action="store_true")

	parser.add_argument("-s", "--stdin",
	                    help="stdin values")

	parser.add_argument("-l", "--language", 
	                    help="the language you want to execute")

	parser.add_argument("--list-languages", 
	                    help="list available languages",
	                    action="store_true")

	arguments = parser.parse_args()

	if arguments.list_languages:
		listLanguages()

	elif arguments.language is not None and not arguments.gui:
		if arguments.script:
			code = arguments.script.read()
			initialization = ""
			if arguments.stdin:
				initialization = arguments.stdin
			arguments.script.close()
			useLanguage(arguments.language, code, initialization)

	else:
		raise hell # unimplemented
