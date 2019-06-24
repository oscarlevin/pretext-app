#!/usr/bin/env python3
# import subprocess
import lxml.etree as ET


def build_html():
    import os
    xsltfile = "../../mathbook/xsl/mathbook-html.xsl"
    ptxfile = "../../mathbook/examples/minimal/minimal.xml"
    outputdir = "./html"
    os.chdir("./html-test") #change to output dir. 
    if not os.path.exists('knowl'):
        os.makedirs('knowl')
    # Need to ensure folders exist first.
    dom = ET.parse(ptxfile)
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    transform(dom)
    # newdom = transform(dom)
    # # print(ET.tostring(newdom, pretty_print=True))
    # # infile = str((ET.tostring(newdom, pretty_print=True)))
    # outfile = open("output-test.tex", 'w', encoding="utf-8", newline='')
    # outfile.write(str(newdom))
    # outfile.close()
    
def build_latex():
    xsltfile = "../mathbook/xsl/mathbook-latex.xsl"
    ptxfile = "../mathbook/examples/minimal/minimal.xml"
    dom = ET.parse(ptxfile)
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    # transform(dom)
    newdom = transform(dom)
    # print(ET.tostring(newdom, pretty_print=True))
    # infile = str((ET.tostring(newdom, pretty_print=True)))
    outfile = open("output-test.tex", 'w', encoding="utf-8", newline='')
    outfile.write(str(newdom))
    outfile.close()
    
    
    
build_html()
# build_latex()