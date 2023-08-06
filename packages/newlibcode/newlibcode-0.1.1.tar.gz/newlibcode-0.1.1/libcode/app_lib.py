# -*- coding: utf-8 -*-


def app(a,b):
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('a')
	parser.add_argument('b')
	args = parser.parse_args()
	'''
	print('Running lib test [receiving params]...')
	# print(args.a, args.b)
	print(a, b)
	print('Real params type:\na: %s\nb: %s' % (
		type(a), type(b)
	))
