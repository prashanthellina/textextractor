'''
Extracts the relevant body of text from a HTML page by
ignoring text in things like navigation boxes etc.
'''

import sys
import pprint
import urllib2
import argparse
from cStringIO import StringIO

from lxml import etree #http://codespeak.net/lxml/

IGNORABLE_TAGS = set(['script', 'a', 'head', 'title'])
MIN_TEXT_LEN = 50

def remove_node(node):
    node.getparent().remove(node)

def get_text(node):
    '''
    Given a XML node, extract all the text it contains.
    (does not recurse into children)
    '''
    text = [node.text or '']
    for cnode in node.getchildren():
        tail = cnode.tail
        if tail is not None:
            text.append(cnode.tail)

    text = '\n'.join(text).strip()
    return text

def get_xml(node):
    '''
    Convert the sub-tree from node downwards
    into string XML representation.
    '''
    return etree.tostring(node)

def create_doc(data):
    '''
    Construct XML tree datastructure from xml string representation.
    '''
    parser = etree.HTMLParser()
    doc = etree.parse(StringIO(data), parser)
    return doc


def get_meta_info(html_page):
    meta_desc = html_page.xpath('//meta[@name = "description"]/@content')
    meta_title =html_page.xpath('//meta[@name = "title"]/@content')
    meta_keywords = html_page.xpath('//meta[@name = "keywords"]/@content')

    if not meta_desc:
        meta_desc = [""]

    if not meta_title:
        meta_title = [""]

    if not meta_keywords:
        meta_keywords = [""]

    return meta_desc,meta_title,meta_keywords

def get_content_nodes(doc):
    '''
    Identify nodes in the XML document that
    have substantial text.
    '''
    nodes = []

    for n in doc.xpath('//*'):
        tag = n.tag

        if tag.lower() in IGNORABLE_TAGS:
            continue

        text = get_text(n)
        if not text:
            continue

        if len(text) < MIN_TEXT_LEN:
            continue

        nodes.append(n)

    return nodes

def make_pruned_tree(content_nodes):
    '''
    Prune the whole XML tree by remnoving nodes
    other than content nodes and their ancestors.
    '''
    nodes = {}
    links = {}
    for node in content_nodes:

        nodes[id(node)] = node

        parent = node.getparent()
        if parent is not None:
            links[id(node)] = id(parent)

        for anode in node.iterancestors():
            _id = id(anode)
            parent = anode.getparent()
            if parent is not None:
                links[_id] = id(parent)

            if _id not in nodes:
                nodes[_id] = anode
    return nodes, links

def get_inlink_counts(links):
    '''
    Given the inter-node links, find out which
    node has maximum number of links coming into it.
    '''
    counts = {}

    for from_id, to_id in links.iteritems():
        count = counts.setdefault(to_id, 0)
        counts[to_id] = count + 1

    return counts

def get_most_linked_node(nodes, links):
    '''
    Identify the node which is most linked.
    (i,e) has most number of inlinks.
    '''
    inlink_counts = get_inlink_counts(links)

    mcount, mid = max([(count, _id) for _id, count in inlink_counts.iteritems()])
    node = nodes[mid]
    return node

def make_dot_graph(nodes, links, chosen_node, stream):
    '''
    Construct the dot format graph representation
    so that graphviz can render the tree for visualization.
    '''
    o = stream
    graph_code = ''
    graph_code += "digraph G {\n"

    for _id, node in nodes.iteritems():

        tlen = len(get_text(node))
        tag = node.tag

        if tlen:
            text = '%s (%d)' % (tag, tlen)
        else:
            text = tag

        if _id == chosen_node:
            attrs = 'style=filled color=lightblue'
        else:
            attrs = ''

        graph_code += "%s [label=\"%s\" %s];\n" % (_id, text, attrs)

    for fid, tid in links.iteritems():
        graph_code += "%d -> %d;\n" % (fid, tid)

    graph_code += "}"
    return graph_code

def process_text(html_page_text):
    '''
    Parses the html page data in @html_page_text and extracts
    the relevant body text ignoring text in navigation areas etc.

    returns: dict
    with keys 'text' = extracted text,
              'meta' = meta information about the page such as title,
              'graph' = a dot format graph layout definition for the
                page structure useful for debugging and understanding.
    '''
    if isinstance(html_page_text, unicode):
        html_page_text = html_page_text.encode('utf8')

    # make doc from html data (cleans html)
    # html_page_text is the data in the page i.e. page_source
    doc = create_doc(html_page_text)

    # remove all script/style nodes
    for tag in ('script', 'style'):
        for node in doc.xpath('.//%s' % tag):
            remove_node(node)

    # get meta title, description, keywords
    meta_desc, meta_title, meta_keywords = get_meta_info(doc)

    # identify content nodes
    content_nodes = get_content_nodes(doc)

    if not content_nodes:
        return ''

    # prune xml tree to remove irrelevant nodes
    nodes, links = make_pruned_tree(content_nodes)

    # get the most linked node from pruned tree
    mnode = get_most_linked_node(nodes, links)

    # make the dot graph
    graph_code = make_dot_graph(nodes, links, id(mnode), sys.stdout)

    text = '\n'.join([x.strip() for x in mnode.xpath('.//text()') if x.strip()])
    meta_info = {}
    meta_info['description'] = meta_desc[0]
    meta_info['title'] = meta_title[0]
    meta_info['keywords'] = meta_keywords[0]

    data = {'text': text, 'meta': meta_info, 'graph': graph_code}
    return data

def process_url(url):
    '''
    Fetches the contents of @url and performs text extraction
    on it. To understand the return data please look at the
    documentation for process_text function.
    '''
    page = urllib2.build_opener()
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = page.open(url, timeout=10)
    con_type = page.info().getheader('Content-Type')
    if not 'text/html' in con_type:
        raise Exception('Not text/html type')

    page = page.read()
    return process_text(page)

def textextractor_command():
    parser = argparse.ArgumentParser(description='Extracts relevant body of text from HTML content')
    parser.add_argument('--graph', action='store_true', default=False,
        help='Produce DOT format graph output to visualize the parsed HTML structure')
    parser.add_argument('--raw', action='store_true', default=False,
        help='Output the entire data resulting from the extraction process')

    args = parser.parse_args()

    data = process_text(sys.stdin.read())

    if args.graph:
        print data.get('graph')
    elif args.raw:
        pprint.pprint(data)
    else:
        print data.get('text')

if __name__ == '__main__':
    textextractor_command()
