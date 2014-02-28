#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import string
from django import template
from django.template import TemplateSyntaxError
from django.utils.translation import ugettext as trans

register = template.Library()

class PartialFormatDict(dict):
	def __missing__(self, key):
		return u'{%s}' % key

def getContextValueByPath(context, path):
	'''
		Path syntax:
			request.session$csrf_token -> context['request'].session['csrf_token']
			test#2.session#0.somefield$foo$bar -> context['test'][2].session[0].somefield['foo']['bar']
			funcpool.somefunc.getList#5 -> context['funcpool'].somefunc().getList()[5]
	'''

	try:
		paths = filter(lambda x : x, path.split('.'))
		ret = context
		first = True
		for cur in paths:
			tmp = cur.split(u'$')
			nodes = []
			for t in tmp:
				_ = t.split(u'#')
				nodes.append(_[0])
				nodes.extend(map(int, _[1:]))
			if first:
				ret = ret[nodes[0]]
				first = False
			else:
				ret = getattr(ret, nodes[0])
			if callable(ret):
				try:
					ret = ret()
				except:
					pass
			del nodes[0]
			for node in nodes:
				ret = ret[node]
				if callable(ret):
					try:
						ret = ret()
					except:
						pass
		return ret
	except Exception, e:
		return ''

class FormatNode(template.Node):
	def __init__(self, data, args):
		self._fmt_base = data
		self._fmt_data = args

	def render(self, context):
		args = []
		kwargs = {}
		for data in self._fmt_data:
			pos = data.find(u'=')
			if pos == 0:
				# Starts with =, ignored.
				continue
			if pos < 0:
				if data and data[0] == u'$': # Should be regarded as variable
					args.append(getContextValueByPath(context, data[1:]))
				else:
					args.append(int(data) if data.isdigit() else data)
			else:
				key, value = data.split(u'=', 1)
				if value and value[0] == u'$':
					kwargs[key] = getContextValueByPath(context, value[1:])
				else:
					kwargs[key] = int(value) if value.isdigit() else value
		try:
			formatter = string.Formatter()
			mapping = PartialFormatDict(**kwargs)
			return formatter.vformat(self._fmt_base, args, mapping)
		except Exception, e:
			raise TemplateSyntaxError(u'Failed to format string: ' + unicode(e))

@register.tag
def format(parser, token):
	tokens = token.split_contents()
	if len(tokens) < 3: # At least one argument to format.
		raise TemplateSyntaxError(u'At lease two argument should be provided.')
	data = tokens[1]
	if data[0] != data[-1] or data[0] not in '\'"':
		raise TemplateSyntaxError(u'Format string should be quoted')
	data = data[1:-1]
	if not data:
		raise TemplateSyntaxError(u'Unexpected empty format string.')
	args = []
	for tk in tokens[2:]:
		if tk[0] == tk[-1] and tk[0] in '\'"':
			args.append(tk[1:-1])
		else:
			if tk.isdigit():
				args.append(int(tk))
			else:
				args.append(tk)
	return FormatNode(data, args)

@register.tag
def transformat(parser, token):
	tokens = token.split_contents()
	if len(tokens) < 3:
		raise TemplateSyntaxError(u'At lease two argument should be provided')
	data = tokens[1]
	if data[0] != data[-1] or data[0] not in '\'"':
		raise TemplateSyntaxError(u'Format string should be quoted')
	data = data[1:-1]
	if not data:
		raise TemplateSyntaxError(u'Unexpected empty format string.')
	data = trans(data)
	args = []
	for tk in tokens[2:]:
		if not tk:
			continue
		if tk[0] == tk[-1] and tk[0] in '\'"':
			args.append(tk[1:-1])
		else:
			if tk.isdigit():
				args.append(int(tk))
			else:
				args.append(tk)
	return FormatNode(data, args)

# You may try {% format "Hi, {username}! Your session id is {session_id}, csrf_token is {csrf_token}." username=$request.getUser.displayname csrf_token=$request.COOKIES$csrf_token session_id=$request.COOKIES$sessionid %}
