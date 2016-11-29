# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from jwzthreading import Message, thread, print_container
from jwzthreading.utils import parse_mailman_gzfiles

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data/fedora-devel-mailman') 

def test_fedora():
    """ Test threading on the fedora-devel mailing list data"""
    # 2010-January https://www.redhat.com/archives/fedora-devel-list/
    #import mailbox


    msglist = parse_mailman_gzfiles(os.path.join(DATA_DIR, '2010-January.txt.gz'),
                         encoding='latin1', headersonly=True)

    msglist_parsed = map(Message, msglist)

    subject_table = thread(msglist_parsed)

    subjects = subject_table.items()
    subjects = sorted(subjects)
    for idx, (_, container) in enumerate(subjects):
        #print(idx)
        #print_container(container)
        pass





