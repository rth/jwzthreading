# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals



def parse_mailman_gzfiles(filename, encoding='utf-8', headersonly=False):
    """ Parse a gzipped files with multiple concatenaged emails
    that can be downloaded from mailman.
    
    Parameters
    ----------
    filename : str
      path to the filename
    encoding : str
      filename encoding
    headersonly : bool
      whether only headers should be parsed

    Returns
    -------

    response : list
      a list of email.Message objects
    """

    from email.parser import Parser
    import gzip
    import sys
    mailbox = []
    container = []

    with gzip.open(filename, 'rb') as fh:
        for idx, line in enumerate(fh):
            if encoding != 'utf-8':
                line = line.decode(encoding)
            if line.startswith('From ') and '@' in line:
                if container:
                    mailbox.append(''.join(container))
                container = []
            container.append(line)

        if container:
            mailbox.append(''.join(container))
    out = []
    for message in mailbox: 
        if sys.version_info < (3, 0) and encoding != 'utf-8':
            message = message.encode('utf-8')
        msg_obj = Parser().parsestr(message, headersonly=headersonly)
        out.append(msg_obj)
    return out

