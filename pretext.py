import click
import lxml.etree as ET

class Config(object):
    
    def __init__(self):
        self.verbose = False
        
pass_config = click.make_pass_decorator(Config)

xsltdir = 'C:/Users/oscar.levin/Documents/GitHub/mathbook'
docroot = './src/main.ptx'
ptxfile = docroot
pretext_qs = 'C:/Users/oscar.levin/Documents/GitHub/pretext-quickstart/xsl/pretext-setup.xsl'


@click.group()
@click.option('-v', '--verbose', is_flag=True)
# @click.option('-s', '--string', default='world!!', help='The greeted thing.')
def cli(verbose):
    """A suite of tools to set up and process PreTeXt documents"""
    if verbose:
        click.echo('Verbose mode doesn\'t do anything')

@cli.command()
# @click.option('-t', '--target-format', default="html", help='output format (latex/html/epub)')
@click.option('-o', '--output', type=click.Path(), default='./output', help='output directory path')
@click.argument('format')
def build(format, output):
    """Process PreTeXt files into specified format, either html or latex."""
    if format=='html':
        build_html(output)
    elif format=='latex':
        build_latex(output)
    else:
        click.echo('%s is not yet a supported build target' % format)

@cli.command()
@click.option('-dir', '--directory', type=click.Path(), default='.', help='project directory [.]')
@click.option('-f', '--format', default='book', help='Project format: [book]/article')
def init(directory, format):
    """Initialize PreTeXt project directory"""    
    if format=='book':
        setup_book(directory)
    elif format=='article':
        setup_article(directory)
    else:
        click.echo('%s is not currently supported' % format)

def setup_book(directory):
    import os
    dom = ET.parse(directory + "/outline.xml")
    xslt = ET.parse(pretext_qs)
    transform = ET.XSLT(xslt)
    if not os.path.exists('xsl'):
        os.makedirs('xsl')
    if not os.path.exists('src'):
        os.makedirs('src')
    transform(dom)
    
def setup_article():
    pass

def build_html(output):
    import os
    # xsltfile = xsltdir + '/xsl/mathbook-html.xsl'
    xsltfile = 'C:/Users/oscar.levin/Documents/GitHub/mathbook/xsl/mathbook-html.xsl'
    # ptxfile = 'C:/Users/oscar.levin/Documents/GitHub/discrete-book/ptx/dmoi-sample.ptx'
    # ptxfile = 'C:/Users/oscar.levin/Documents/GitHub/mathbook/examples/sample-book/sample-book.xml'
    ptxfile = 'C:/Users/oscar.levin/Documents/GitHub/new-project/src/main.ptx'
    # ptxfile = "../../mathbook/examples/minimal/minimal.xml"
    # outputdir = "./html"
    if not os.path.exists(output):
        os.makedirs(output)
    os.chdir(output) #change to output dir. 
    if not os.path.exists('knowl'):
        os.makedirs('knowl')
    if not os.path.exists('images'):
        os.makedirs('images')
    dom = ET.parse(ptxfile)
    dom.xinclude()
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    transform(dom)

    
def build_latex(output):
    xsltfile = xsltdir + '/xsl/mathbook-latex.xsl'
    # ptxfile = "../mathbook/examples/minimal/minimal.xml"
    dom = ET.parse(ptxfile)
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    outfile = open("main.tex", 'w', newline='')
    outfile.write(str(newdom))
    outfile.close()
