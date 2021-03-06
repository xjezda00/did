# coding: utf-8
""" Tests for the GitHub plugin """

from __future__ import unicode_literals, absolute_import

import pytest
import did.cli
import did.base


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INTERVAL = "--since 2015-09-05 --until 2015-09-06"

CONFIG = """
[general]
email = "Petr Splichal" <psplicha@redhat.com>

[gh]
type = github
url = https://api.github.com/
login = psss
"""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Tests
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_github_issues_created():
    """ Created issues """
    did.base.Config(CONFIG)
    stats = did.cli.main(INTERVAL)[0][0].stats[0].stats[0].stats
    assert any([
        "psss/did#017 - What did you do" in unicode(stat) for stat in stats])

def test_github_issues_closed():
    """ Closed issues """
    did.base.Config(CONFIG)
    stats = did.cli.main(INTERVAL)[0][0].stats[0].stats[1].stats
    assert any([
        "psss/did#017 - What did you do" in unicode(stat) for stat in stats])

def test_github_invalid_token():
    """ Invalid token """
    did.base.Config(CONFIG + "\ntoken = bad-token")
    with pytest.raises(did.base.ReportError):
        did.cli.main(INTERVAL)

def test_github_missing_url():
    """ Missing url """
    did.base.Config("[gh]\ntype = github")
    with pytest.raises(did.base.ReportError):
        did.cli.main(INTERVAL)

def test_github_unicode():
    """ Created issues with Unicode characters """
    INTERVAL = "--since 2016-02-23 --until 2016-02-23"
    EMAIL = " --email hasys@example.org"
    did.base.Config("[gh]\ntype = github\nurl = https://api.github.com/")
    stats = did.cli.main(INTERVAL + EMAIL)[0][0].stats[0].stats[0].stats
    assert any([
        u"Boundary events lose it’s documentation" in unicode(stat)
        for stat in stats])
