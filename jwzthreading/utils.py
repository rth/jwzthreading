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


def parse_mailman_htmlthread(filename):
    """ Parse a gzipped files with multiple concatenaged emails
    that can be downloaded from mailman.

    Parameters
    ----------
    filename : str
      path to the filename

    Returns
    -------

    response : list
      a thread list
    """
    from lxml import etree
    from .jwzthreading import Container, Message

    if filename.endswith('.gz'):
        import gzip
        fopen = gzip.open
    else:
        fopen = open

    parser = etree.HTMLParser()
    with fopen(filename, 'rt') as fh:
        tree = etree.parse(fh, parser)

    elements = filter(lambda x: x.tag == 'ul', tree.find('body'))

    tree = list(elements)[-1].getchildren() # pick last <ul> element

    def create_thread(root, parent_container=None):
        """ Parse the html nested lists to produce the threading structure"""
        #print(dir(root))
        if root.tag != 'li':
            raise ValueError('Element {} was not expected'.format(root))

        if len(root.getchildren()) == 0:
            # this is a dummy element "<li>Possible follow-ups</li>"
            return None

        container = Container()
        for child in root.getchildren():
            if child.tag == 'strong':
                # url with to the actual email
                a_el = child.getchildren()[0]
                container.message = Message()
                container.message.subject = a_el.text
                container.message.message_idx = int(a_el.get('name'))
            elif child.tag == 'em':
                pass  # email sender, ignore this line
            elif child.tag == 'ul':
                for nested_child in child.getchildren():
                    create_thread(nested_child, parent_container=container)
            else:
                raise ValueError('Unexpected element {}'.format(child))
        if parent_container is not None:
            parent_container.add_child(container)

        return container

    threads = [create_thread(el) for el in tree]

    return threads

