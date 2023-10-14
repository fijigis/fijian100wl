from zope.interface import Attribute, Interface


class ICommunalect(Interface):
    name = Attribute("")


class ICommunalectGroup(Interface):
    name = Attribute("")
