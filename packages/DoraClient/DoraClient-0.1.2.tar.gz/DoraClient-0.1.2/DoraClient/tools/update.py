#!/usr/bin/python
# coding=utf-8


import re
import pip
import urllib
import pkg_resources
from os import execl, environ
from sys import executable, argv
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):

        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)


class PkgNotFoundError(Exception):
    """No package found"""


class NoVersionsError(Exception):
    """No versions found for package"""


def normalize_version(v):
    """Helper function to normalize version
    Returns a comparable object
    Args:
        v (str) version, e.g. "0.1.0"

    """
    rv = []
    for x in v.split("."):
        try:
            rv.append(int(x))
        except ValueError:
            for y in re.split("([0-9]+)", x):
                try:
                    if y != '':
                        rv.append(int(y))
                except ValueError:
                    rv.append(y)
    return rv


class AutoUpdate(object):
    """AutoUpgrade class, holds one package
    """

    def __init__(self, pkg, index=None, verbose=False):
        """Args:
                pkg (str): name of package
                index (str): alternative index, if not given default for *pip* will be used. Include
                             full index url, e.g. https://example.com/simple
        """
        self.pkg = pkg
        if index is None:
            self.index = "https://pypi.python.org/simple"
            self._index_set = False
        else:
            self.index = index.rstrip('/')
            self._index_set = True
        self.verbose = verbose

    def upgrade_if_needed(self, restart=True, dependencies=False):
        """ Upgrade the package if there is a later version available.
            Args:
                restart, restart app if True
                dependencies, update dependencies if True (see pip --no-deps)
        """
        if self.check():
            if self.verbose:
                print("Upgrading %s" % self.pkg)
            self.upgrade(dependencies)
            if restart:
                self.restart()

    def upgrade(self, dependencies=False):
        """ Upgrade the package unconditionaly
            Args:
                dependencies: update dependencies if True (see pip --no-deps)
            Returns True if pip was sucessful
        """
        pip_args = []
        proxy = environ.get('http_proxy')
        if proxy:
            pip_args.append('--proxy')
            pip_args.append(proxy)
        pip_args.append('install')
        pip_args.append(self.pkg)
        if self._index_set:
            pip_args.append('-i')
            pip_args.append(self.index)
        if not dependencies:
            pip_args.append("--no-deps")
        if self._get_current() != [-1]:
            pip_args.append("--upgrade")
        try:
            a = pip.main(args=pip_args)
        except TypeError:
            # pip changed in 0.6.0 from initial_args to args, this is for backwards compatibility
            # can be removed when pip 0.5 is no longer in use at all (2025...)  
            a = pip.main(initial_args=pip_args)
        return a == 0

    def restart(self):
        """ Restart application with same args as it was started.
            Does **not** return
        """
        if self.verbose:
            print("Restarting " + executable + " " + str(argv))
        execl(executable, *([executable] + argv))

    def check(self):
        """ Check if pkg has a later version
            Returns true if later version exists.
        """
        current = self._get_current()
        highest = self._get_highest_version()
        return highest > current

    def _get_current(self):

        try:
            current = normalize_version(pkg_resources.get_distribution(self.pkg).version)
        except pkg_resources.DistributionNotFound:
            current = [-1]
        return current

    def _get_highest_version(self):

        url = "{}/{}/".format(self.index, self.pkg)
        html = urllib.urlopen(url)
        if html.getcode() != 200:
            raise PkgNotFoundError

        hp = MyHTMLParser()
        hp.feed(html.read())
        hp.close()

        versions = []
        for link in hp.links:

            try:
                version = re.search(self.pkg + '-(.*)\.tar\.gz', link).group(1)
                versions.append(normalize_version(version))
            except AttributeError:
                pass
        if len(versions) == 0:
            raise NoVersionsError()
        return max(versions)
