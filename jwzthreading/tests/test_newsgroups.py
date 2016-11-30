# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from unittest import SkipTest

from jwzthreading import (Message, thread, print_container,
                          sort_threads)
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
    threads_ref = sort_threads(threads_ref, key='subject', missing='Z')


    threads = thread([Message(el, message_idx=idx) for idx, el in enumerate(msglist)],
                     group_by_subject=False)
    threads = sort_threads(threads, key='subject', missing='Z')



    for idx, container_ref in enumerate(threads_ref):
        container = threads[idx]
        if container.message is not None:
            subject = container.message.subject
            message_idx = container.message.message_idx
        else:
            subject = None
            message_idx = None
        if container_ref.size == container.size and\
                container_ref.message.message_idx == message_idx:
            print(idx, '   [OK]')
            continue
        print(idx)
        print('Ref :  {:3} {} {}'.format(container_ref.size, container_ref.message.message_idx,
                                         container_ref.message.subject))
        print('Comp:  {:3} {} {}'.format(container.size, message_idx, subject))

    assert sum([el.size for el in threads]) == N_EMAILS_JUNE2010
    #assert len(subjects) == N_THREADS_JUNE2010





