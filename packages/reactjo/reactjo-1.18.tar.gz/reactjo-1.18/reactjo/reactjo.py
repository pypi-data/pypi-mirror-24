# -*- coding: utf-8 -*-
"""reactjo.reactjo: provides entry point main()."""
__version__ = "1.0.0"

import sys, os, subprocess
from reactjo.helpers.config_manager import get_cfg, set_cfg, build_cfg
from reactjo.helpers.worklist import print_worklist
from reactjo.helpers.extend import extend
from reactjo.helpers.update import update

def initialize():
	if not os.path.exists('reactjorc'):
		os.mkdir('reactjorc')
	if not os.path.exists('reactjorc/extensions'):
		os.mkdir('reactjorc/extensions')
	if not os.path.exists('reactjorc/config.json'):
		build_cfg()

	project_root = get_cfg()['paths']['project_root']
	if not os.path.exists(project_root):
		os.mkdir(project_root)

def main():
	cmd = sys.argv[1]
	if cmd in ['init', 'initialize', 'i']:
		initialize()
		update()
	elif cmd in ['update', 'u']:
		update()
	elif cmd in ['extend', 'extension', 'e']:
		extend()
	elif cmd in ['serve', 'server', 's']:
		serve()
	else:
		cfg = get_cfg()
		for ext in cfg['extensions']:
			path = cfg['paths']['reactjorc'] + '/extensions/{}/entry.py'.format(
				ext['title'])
			subprocess.call(['python3', path, cmd])

		print_worklist()
