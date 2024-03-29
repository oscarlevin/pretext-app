import click
from pathlib import Path
# import os
import appdirs
import yaml
import lxml.etree as ET


config_option = click.option('-c', '--config', default='./ptxconfig.yml', help="User specified config file (default = ptxconfig.yml)")

# Set up cfgs dictionary with default config values:
# cfgs = load_default_configs()

# Testing variables to be moved to config
# xsltdir = 'C:/Users/oscar.levin/Documents/GitHub/mathbook'
# xsltdir = cfgs['pretextdir']
# docroot = './src/main.ptx'
# ptxfile = docroot
# ptxfile = cfgs['mainfile']
# pretext_qs = 'C:/Users/oscar.levin/Documents/GitHub/pretext-quickstart/xsl/pretext-setup.xsl'

# Main Click command entry:
@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('-u', '--update-config', is_flag=True, default=False, help="Update config file with provided options")
@config_option
# @click.option('-c', '--config', default='./ptxconfig.yml', help="User specified config file (default = ptxconfig.yml)")
# @click.option('-s', '--string', default='world!!', help='The greeted thing.')
def cli(verbose, update_config, config):
    """A suite of tools to set up and process PreTeXt documents"""
    if verbose: #Eventually verbose will give more output, or just remove this!
        click.echo('Verbose mode doesn\'t do anything')
    cfgs = get_configs(config)


#### Sub commands: ####
# build sub-command: to build current ptx source into various formats.
@cli.command()
# @click.option('-t', '--target-format', default="html", help='output format (latex/html/epub)')
@click.option('-o', '--output', type=click.Path(), default='./output', help='output directory path')
@click.option('-w', '--webwork', is_flag=True, default=False, help='rebuild webwork')
@click.option('-d', '--diagrams', is_flag=True, default=False, help='regenerate images using mbx script')
@click.argument('format')
@config_option
def build(format, output, webwork, diagrams, config):
    """Process PreTeXt files into specified format, either html or latex."""
    cfgs = get_configs(config)
    if format=='html':
        build_html(output,webwork,diagrams,cfgs)
    elif format=='latex':
        build_latex(output,webwork,cfgs)
    else:
        click.echo('%s is not yet a supported build target' % format)

# init sub-command: to set up project initially.
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

# TODO: set up config function to use app to set values of config file.
@cli.command()
def config():
    """Set project-level or global configuration options"""
    pass


@cli.command()
@config_option
def test(config):
    """Test option for dev"""
    cfgs = get_configs(config)
    # xsltdir = cfgs['pretextdir']
    # click.echo('Pretext is located in ' + xsltdir)
    click.echo(cfgs)
######### End Click Setup ############



#### Helper Functions ####
# set default config variables:
def get_configs(project_config):
    cfg_dir = appdirs.user_config_dir('pretext')
    cfg_file = Path(cfg_dir) /  'ptxconfig.yml'
    if not cfg_file.exists():
        create_user_config(cfg_file)
    with cfg_file.open() as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    #load project specific config file, and update cfg with it:
    # project_config = './ptxconfig.yml'
    if Path(project_config).exists():
        with Path(project_config).open() as local_ymlfile:
            cfg.update(yaml.safe_load(local_ymlfile))
    else:
        click.echo("Warning: did not find "+project_config+"; using system wide defaults.")
    return cfg

# include custom config file if requested:
def load_custom_configs(configfile):
    pass

# from https://stackoverflow.com/questions/40193112/python-setuptools-distribute-configuration-files-to-os-specific-directories
def create_user_config(cfg_file):
    # source = pkg_resources.resource_stream(__name__, 'my_package.conf.dist')
    print('Trying to write cfg file')
    cfg_file.parent.mkdir(parents=True, exist_ok=True)
    # os.makedirs(os.path.dirname(cfg_file), exist_ok=True) #make directory if needed.
    with cfg_file.open('w') as dest:
        dest.writelines('#ptxconfig.\n test: key\n')

### Setup PreTeXt:
#Setup functions:
def setup_book(directory):
    dom = ET.parse(directory + "/outline.xml")
    pretext_qs = 'C:/Users/oscar.levin/Documents/GitHub/pretext-quickstart/xsl/pretext-setup.xsl'
    xslt = ET.parse(pretext_qs)
    transform = ET.XSLT(xslt)
    # Make directories if don't exist
    Path('xsl').mkdir(exist_ok=True)
    Path('src').mkdir(exist_ok=True)
    # if not os.path.exists('xsl'):
    #     os.makedirs('xsl')
    # if not os.path.exists('src'):
    #     os.makedirs('src')
    transform(dom)
    
def setup_article(directory):
    pass

#config setup:
def find_mathbook():
    pass



#Build functions:
def build_html(output,webwork,diagrams,cfgs):
    from os import chdir
    # xsltfile = xsltdir + '/xsl/mathbook-html.xsl'
    xsltfile = 'C:/Users/oscar.levin/Documents/GitHub/mathbook/xsl/mathbook-html.xsl'
    # ptxfile = 'C:/Users/oscar.levin/Documents/GitHub/discrete-book/ptx/dmoi-sample.ptx'
    # ptxfile = 'C:/Users/oscar.levin/Documents/GitHub/mathbook/examples/sample-book/sample-book.xml'
    ptxfile = 'C:/Users/oscar.levin/Documents/GitHub/new-project/src/main.ptx'
    # ptxfile = "../../mathbook/examples/minimal/minimal.xml"
    # outputdir = "./html"
    Path(output).mkdir(parents=True, exist_ok=True)
    # if not os.path.exists(output):
    #     os.makedirs(output)
    chdir(output) #change to output dir. 
    Path('knowl').mkdir(exist_ok=True)
    # if not os.path.exists('knowl'):
    #     os.makedirs('knowl')
    Path('images').mkdir(exist_ok=True)
    # if not os.path.exists('images'):
    #     os.makedirs('images')
    dom = ET.parse(ptxfile)
    dom.xinclude()
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    transform(dom)

    
def build_latex(output,webwork,cfgs):
    xsltfile = cfgs['xsltdir'] + '/xsl/mathbook-latex.xsl'
    ptxfile = "../mathbook/examples/minimal/minimal.xml"
    dom = ET.parse(ptxfile)
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    outfile = open("main.tex", 'w', newline='')
    outfile.write(str(newdom))
    outfile.close()
