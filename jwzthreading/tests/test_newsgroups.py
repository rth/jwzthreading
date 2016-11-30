# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from unittest import SkipTest

from jwzthreading import Message, thread, print_container
from jwzthreading.utils import (parse_mailman_gzfiles,
                                parse_mailman_htmlthread)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data/fedora-devel-mailman') 

# Expected number of emails and threads
N_EMAILS_JUNE2010 = 292
N_THREADS_JUNE2010 = 63



def test_parse_mailman_gzfiles():
    """ Test that we can parse mailman files """
    msglist = parse_mailman_gzfiles(os.path.join(DATA_DIR, '2010-January.txt.gz'),
                         encoding='latin1', headersonly=True)

    assert len(msglist) == N_EMAILS_JUNE2010

def test_parse_mailman_htmlthread():
    """ Test that we can parse mailman html thread """
    try:
        import lxml
    except ImportError:
        raise SkipTest
    threads = parse_mailman_htmlthread(os.path.join(DATA_DIR,
                                      '2010-January_thread.html'))

    #assert len(threads) == N_THREADS_JUNE2010
    #for el in threads:
    #    print(' - ({})'.format(el.size), el.message.subject)
    assert sum([el.size for el in threads]) == N_EMAILS_JUNE2010

    #for el in threads:
    #    print_container(el)





def test_fedora():
    """ Test threading on the fedora-devel mailing list data
    from June 2010"""

    try:
        import lxml
    except ImportError:
        raise SkipTest


    msglist = parse_mailman_gzfiles(os.path.join(DATA_DIR, '2010-January.txt.gz'),
                         encoding='latin1', headersonly=True)

    assert len(msglist) == N_EMAILS_JUNE2010


    threads_ref = parse_mailman_htmlthread(os.path.join(DATA_DIR,
                                      '2010-January_thread.html'))


    threads = thread([Message(el) for el in msglist])

    for container in threads:
        #print(idx)
        #print_container(container)
        pass
    #assert sum([el.size for el in threads]) == N_EMAILS_JUNE2010

    #assert len(subjects) == N_THREADS_JUNE2010





