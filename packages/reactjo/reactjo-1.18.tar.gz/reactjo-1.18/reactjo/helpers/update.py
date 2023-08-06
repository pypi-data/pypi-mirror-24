from reactjo.helpers.config_manager import get_cfg, set_cfg
import os, shutil, subprocess

def update():
	cfg = get_cfg()
	extensions = cfg['paths']['reactjorc'] + '/extensions/'

	# Remove all extensions and reinstall them.
	if os.path.exists(extensions):
		shutil.rmtree(extensions)
	os.mkdir(extensions)

	for ext in cfg['extensions']:
		path = extensions + ext['title']

		if 'branch' in ext:
			subprocess.call(['git', 'clone', '-b', ext['branch'], ext['uri'], path])
		else:
			subprocess.call(['git', 'clone', ext['uri'], path])

		dependencies = path + '/requirements.txt'
		if os.path.exists(dependencies):
			deps = open(dependencies, 'r').read()
			if len(deps) > 0:
				subprocess.call(['pip3', 'install', '-r', dependencies])
