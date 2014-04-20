# textextractor

Extract relevant body of text from HTML page content

![Image](./textextractor.png?raw=true)

## Installation

``` bash
sudo apt-get install build-essential python-dev
sudo pip install git+git://github.com/prashanthellina/textextractor.git
```

## Usage

### As a script

``` bash
wget -O test.html "http://www.telegraph.co.uk/finance/newsbysector/mediatechnologyandtelecoms/digital-media/10773901/Google-the-unelected-superpower.html"
cat test.html | textextractor
Researchers at Princeton and Northwestern universities have pored over 1,800
  US policies and concluded that America is an oligarchy. Instead of looking
  out for the majority of the country’s citizens, the US government is ruled
  by the interests of the rich and the powerful, they found. No great
  surprises there, then.
But the government is not the only American power whose motivations need to be
  rigourously examined. Some 2,400 miles away from Washington, in Silicon
  Valley, Google is aggressively gaining power with little to keep it in check.
It has cosied up to governments around the world so effectively that its
  chairman, Eric Schmidt, is a White House advisor. In Britain, its executives
  meet with ministers more than almost any other corporation.
Google can’t be blamed for this: one of its jobs is to lobby for laws that
  benefit its shareholders, but it is up to governments to push back. As
  things stand, Google – and to a lesser extent, Facebook – are in danger of
  becoming the architects of the law.
Meanwhile, these companies are becoming ever more sophisticated about the
  amount of information they access about users. Google scans our emails. It
  knows where we are. It anticipates what we want before we even know it. Sure
  there are privacy settings and all that, but surrendering to Google also
  feels nigh on impossible to avoid if you want to live in the 21st century.
  It doesn’t stop there either. If Google Glass is widely adopted, it will be
  able to clock everything we see, while the advance of Google Wallet could
  position the company at the heart of much of the world’s spending.
Related Articles
Who really uses YouTube?
18 Apr 2014
British Pathé uploads 85,000 historic films to YouTube
17 Apr 2014
Google's aquisition spree
16 Apr 2014
Google feels weight of mobile as sales fall short
17 Apr 2014
Google Street View algorithm can beat CAPTCHAs
17 Apr 2014
More than $22bn wiped off Google
16 Apr 2014
One source at the technology giant put it well when she referred to the
  company as an “unelected superpower”. I think this is a fair summary. So
  far, we are fortunate that that dictatorship is a relatively benign one. The
  company’s mantra is “do no evil”, and while people may disagree on what evil
  means, broadly speaking, its founders are pretty good guys. But Larry Page
  and Sergey Brin will not be around forever. Nor should we rely on any entity
  that powerful to regulate its own behaviour.
The government in America, and its counterparts around the world, should stop
  kowtowing to Google and instead work in concert to keep this and any other
  emerging corporate superpowers firmly in check.
```

### As a module/library

Example python script: example.py
``` python
import urllib2
import pprint
from textextractor import process_text

html_data = urllib2.urlopen('http://www.telegraph.co.uk/finance/newsbysector/mediatechnologyandtelecoms/digital-media/10773901/Google-the-unelected-superpower.html').read()

data = process_text(html_data)

pprint.pprint(data)
```

### Debugging/Understanding using Graphviz output

Textextractor can be instructed to dump a DOT format definition of the tree of the in-memory HTML document in-order to help in understanding the process of body text extraction. You will need to ensure that Graphviz is installed.

``` bash
sudo apt-get install graphviz
```

This is an example of how to run the command to dump DOT format graph output.

``` bash
prashanth@almatrix1:/tmp$ cat test.html | textextractor --graph
digraph G {
139904898052608 [label="body" ];
139904898056064 [label="div" style=filled color=lightblue];
139904897709984 [label="p (513)" ];
139904898053256 [label="div" ];
139904898052824 [label="div" ];
139904898054552 [label="div" ];
139904898145384 [label="p (329)" ];
139904898052896 [label="html" ];
139904898053616 [label="div" ];
139904898145960 [label="p (611)" ];
139904898053832 [label="div" ];
139904898053040 [label="div" ];
139904898145672 [label="p (215)" ];
139904898052536 [label="div" ];
139904898054408 [label="div" ];
139904898053184 [label="div" ];
139904898055776 [label="div" ];
139904898053472 [label="div" ];
139904898145816 [label="p (265)" ];
139904898052680 [label="div" ];
139904898054336 [label="div" ];
139904898053328 [label="div" ];
139904898133816 [label="h2 (113)" ];
139904898134744 [label="span (77)" ];
139904898052248 [label="div" ];
139904898052320 [label="div" ];
139904898052968 [label="div" ];
139904898052464 [label="div" ];
139904898054120 [label="div" ];
139904897710056 [label="p (206)" ];
139904898145528 [label="p (234)" ];
139904898053400 [label="div" ];
139904898052608 -> 139904898052896;
139904898056064 -> 139904898053256;
139904898053256 -> 139904898053328;
139904898052824 -> 139904898052248;
139904898054552 -> 139904898054120;
139904898145384 -> 139904898055776;
139904897709984 -> 139904898053832;
139904898053616 -> 139904898056064;
139904898053184 -> 139904898053400;
139904898145960 -> 139904898053616;
139904898053832 -> 139904898056064;
139904898053040 -> 139904898052824;
139904898145672 -> 139904898054408;
139904898052536 -> 139904898052608;
139904898054408 -> 139904898056064;
139904898054336 -> 139904898056064;
139904898055776 -> 139904898056064;
139904898053472 -> 139904898056064;
139904898145816 -> 139904898053472;
139904898052680 -> 139904898054552;
139904898053328 -> 139904898052248;
139904898133816 -> 139904898052824;
139904898134744 -> 139904898052968;
139904898052248 -> 139904898052320;
139904898052320 -> 139904898052464;
139904898052968 -> 139904898052680;
139904898052464 -> 139904898052536;
139904898054120 -> 139904898053184;
139904897710056 -> 139904898053832;
139904898145528 -> 139904898054336;
139904898053400 -> 139904898053040;
}
```

This is example of how to produce a rendering of the graph in PNG format

``` bash
cat test.html | textextractor --graph | dot -Tpng > /tmp/test.png
eog /tmp/test.png
```

The rendered graph looks like this. Note that all text under the node marked in blue is extracted.

![Image](./example_graph.png?raw=true)
