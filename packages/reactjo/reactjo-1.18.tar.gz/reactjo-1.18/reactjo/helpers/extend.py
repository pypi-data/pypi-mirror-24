import os, subprocess

def extend():
	src = 'https://github.com/aaron-price/reactjo-extension-template.git'
	target = os.getcwd()
	subprocess.call([ 'git', 'clone', src, target + '/template' ])
