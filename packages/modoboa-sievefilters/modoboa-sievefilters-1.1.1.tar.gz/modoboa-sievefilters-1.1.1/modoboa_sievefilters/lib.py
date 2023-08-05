# coding: utf-8

"""Internal tools."""

from sievelib.factory import FiltersSet
from sievelib.managesieve import Client, Error
from sievelib.parser import Parser

from django.utils.translation import ugettext as _

from modoboa.lib.connections import ConnectionsManager, ConnectionError
from modoboa.lib.exceptions import ModoboaException
from modoboa.parameters import tools as param_tools


class SieveClientError(ModoboaException):
    http_code = 424


class SieveClient(object):
    __metaclass__ = ConnectionsManager

    def __init__(self, user=None, password=None):
        try:
            ret, msg = self.login(user, password)
        except Error as e:
            raise ConnectionError(str(e))
        if not ret:
            raise ConnectionError(msg)

    def login(self, user, password):
        conf = dict(param_tools.get_global_parameters("modoboa_sievefilters"))
        self.msc = Client(conf["server"], conf["port"], debug=False)
        authmech = conf["authentication_mech"]
        if authmech == "AUTO":
            authmech = None
        try:
            ret = self.msc.connect(
                user, password, starttls=conf["starttls"], authmech=authmech)
        except Error:
            ret = False
        if not ret:
            return False, _(
                "Connection to MANAGESIEVE server failed, check your "
                "configuration"
            )
        return True, None

    def logout(self):
        self.msc.logout()
        self.msc = None

    def refresh(self, user, password):
        import ssl

        if self.msc is not None:
            try:
                self.msc.capability()
            except Error as e:
                pass
            else:
                return
        try:
            ret, msg = self.login(user, password)
        except (Error, ssl.SSLError) as e:
            raise ConnectionError(e)
        if not ret:
            raise ConnectionError(msg)

    def listscripts(self):
        return self.msc.listscripts()

    def getscript(self, name, format="raw"):
        content = self.msc.getscript(name)
        if content is None:
            raise SieveClientError(self.msc.errmsg)
        if format == "raw":
            return content
        p = Parser()
        if not p.parse(content):
            print "Parse error????"
            return None
        fs = FiltersSet(name)
        fs.from_parser_result(p)
        return fs

    def pushscript(self, name, content, active=False):
        if isinstance(content, unicode):
            content = content.encode("utf-8")
        if not self.msc.havespace(name, len(content)):
            error = "%s (%s)" % (
                _("Not enough space on server"), self.msc.errmsg)
            raise SieveClientError(error)
        if not self.msc.putscript(name, content):
            raise SieveClientError(self.msc.errmsg)
        if active and not self.msc.setactive(name):
            raise SieveClientError(self.msc.errmsg)

    def deletescript(self, name):
        if not self.msc.deletescript(name):
            raise SieveClientError(self.msc.errmsg)

    def activatescript(self, name):
        if not self.msc.setactive(name):
            raise SieveClientError(self.msc.errmsg)
