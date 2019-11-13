# -*- coding: utf-8 -*-

import json, base64, argparse, printc
from server import Start

props = {
	'encoding': 'UTF-8',
	'version': '2.0.0'
}

class Processer(object):
	def __init__(self):
		super(Processer, self).__init__()
		'''
		Please refer to: https://github.com/shadowsocksrr/shadowsocks-rss/wiki/SSR-QRcode-scheme
		ssr://base64(host:port:protocol:method:obfs:base64pass/?
			obfsparam=base64param&protoparam=base64param&remarks=base64remarks
			&group=base64group&udpport=0&uot=0)
		'''
		self.link = '{server}:{server_port}:{protocol}:{method}:{obfs}:{password}/?obfsparam={obfs_param}&protoparam={protocol_param}&remarks={remarks}&group={group}'

		self.params = [
			{ 'key': 'server' },
			{ 'key': 'server_port' },
			{ 'key': 'protocol' },
			{ 'key': 'method' },
			{ 'key': 'obfs' },
			{ 'key': 'password', 'b64': True },
			{ 'key': 'obfs_param', 'b64': True },
			{ 'key': 'protocol_param', 'b64': True },
			{ 'key': 'remarks', 'b64': True, 'default': 'THRAEX-NODE',  },
			{ 'key': 'group', 'b64': True, 'default': 'THRAEX' }
		]

	def run_old(self):
		with open('configs/config.json') as f:
			configs = json.load(f)

		target = 'configs/ssr-links'
		with open(target, 'w') as f:
			for cfg in configs:
				b64_pass = self.b64encode(cfg['password'])
				b64_obfsparam = self.b64encode(cfg['obfs_param'])
				b64_protoparam = self.b64encode(cfg['protocol_param'])
				b64_group = self.b64encode(cfg.get('group', ''))
				b64_remarks = self.b64encode(cfg.get('remarks', ''))

				b64_link = self.b64encode(self.link % (cfg.get('server'), cfg.get('server_port'), 
					cfg.get('protocol'), cfg.get('method'), cfg.get('obfs'), b64_pass, b64_obfsparam, 
					b64_protoparam, b64_remarks, b64_group))

				final_link = ('ssr://%s' % b64_link)
				print(final_link)
				f.write(final_link)
				f.write('\n')

		print('******************************************')
		with open(target) as f:
			data = f.read().encode(props['encoding'])
			print('%s\n' % data)
			final = base64.b64encode(data).decode(props['encoding']) 
			print(final)

			with open('configs/ssr-dist', 'w') as fo:
				fo.write(final)

		Start().UP()

	def run(self):
		printc.infoln('Loading configuration file...')

		printc.info('-------------------< %s >------------------' % 
			printc.cyan('ssr-subscribe-generator'))
		printc.info('Subscription Generator of SSR')
		printc.infoln('---------------------------[ %s ]---------------------------' %
			printc.cyan('Base64'))

		cfgs = self.configs()
		links = self.links(cfgs)
		self.coding(links)

	def configs(self):
		cfg_path = 'configs/config.json'

		printc.info('---------------------< %s >--------------------' % 
			printc.cyan(cfg_path))

		configs = None
		try:
			with open(cfg_path) as f: configs = json.load(f)

			total = len(configs)

			if total > 0:
				printc.infoln('Total: %s. The original information is:' % total)

				for i in range(total):
					printc.info('Server %d:' % (i + 1))
					printc.info(printc.green((configs[i])))

				printc.info()
			else:
				printc.warning('No server node information.')
		except Exception as e:
			printc.error(e)

		return configs

	def links(self, cfgs):
		if not cfgs: return

		printc.info('---------------------< %s >--------------------' % 
			printc.cyan('Generate SSR links'))

		ssr_links = []
		for i in range(len(cfgs)):
			ind, item, b64_item = i + 1, {}, {}
			for p in self.params:
				key, def_val = p['key'], ''

				if 'default' in p:
					if key == 'remarks':
						def_val = '%s-%d' % (p.get('default'), ind)
					else:
						def_val = p.get('default')

				item[key] = cfgs[i].get(key, def_val)

				bval = cfgs[i].get(key, def_val)
				if p.get('b64'): bval = self.b64encode(bval)
				b64_item[key] = bval

			printc.info('Server %d:' % ind)
			print(' ==> %s' % printc.green(self.link.format(**item)))
			b64_link = self.link.format(**b64_item)
			print(' ==> %s' % printc.green(b64_link))
			ssr_link = 'ssr://%s' % self.b64encode(b64_link)
			print(' ==> %s' % printc.green(ssr_link))
			ssr_links.append(ssr_link)

		printc.info()
		# printc.info('---------------------< %s >--------------------' % 
		# 	printc.cyan('Output SSR links'))
		# printc.info(printc.green('Output SSR links'))
		ssr_links = '\n'.join(ssr_links)
		printc.info('---------------------------------------------------------------')
		print(printc.green(ssr_links))
		printc.infoln('---------------------------------------------------------------')

		return ssr_links

	def coding(sefl, links):
		if not links: return

		printc.infoln('---------------------< %s >---------------------' % 
			printc.cyan('Encoding SSR link'))

		target = 'configs/ssr-dist'
		printc.info('Contents are written to %s:' % printc.green(target))

		data = links.encode(props['encoding'])
		final = base64.b64encode(data).decode(props['encoding'])

		printc.info('---------------------------------------------------------------')
		print(printc.green(final))
		printc.infoln('---------------------------------------------------------------')

		with open(target, 'w') as fo: fo.write(final)

		printc.info('Execute %s to access %s.' % 
			(printc.green('server.py'), printc.green('ssr-dist')))

	def b64encode(self, s):
		return base64.urlsafe_b64encode(s.encode(props['encoding'])).decode(props['encoding']).rstrip('=')

if __name__ == '__main__':
	# Processer().run()

	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', help = 'Increase output verbosity', action = 'store_true')
	parser.add_argument('-V', '--version', help = 'Display version information', action = 'store_true')
	args = parser.parse_args()

	print(args)
	print(args.verbose)
	print('merge branch test1')
	print('merge branch test2')
	print('merge branch test3')

	# print(argparse.ArgumentParser().add_argument())
	# print(parser.add_argument.__doc__)
