# encoding: utf-8

from pyramid.security import Allow, Authenticated


class Root(object):
    __acl__ = [(Allow, Authenticated, 'view')]
    def __init__(self, request):
        pass
