# Makefile in docs directory

# You can change this to your desired output directory
BUILDDIR      = _build

# You can change this to your desired sphinx build command
SPHINXBUILD   = sphinx-build

# You can change this to your desired source directory
SRCDIR        = .
# You can change this to your desired configuration file
CONFDIR       = $(SRCDIR)

# All .rst files are source files
SOURCEDIR     = $(SRCDIR)

# The output directory for built documentation.
HTMLDIR       = $(BUILDDIR)/html

# The filename for the built documentation index.
HTML_INDEX    = $(HTMLDIR)/index.html

# All .txt files are considered as reStructuredText files.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) -c $(CONFDIR) \
                -A language=$(LANGUAGE) $(SPHINXOPTS) $(SOURCEDIR)
# The theme to use for HTML and HTML Help pages.  See the documentation for
# valid values.
HTML_THEME    = sphinx_rtd_theme

# If you change this, also update the conf.py file
# You can add more configuration here if needed

.PHONY: help clean html

help:
        @echo "Please use \`make <target>' where <target> is one of"
        @echo "  html       to make standalone HTML files"
        @echo "  clean      to remove build files"

clean:
        rm -rf $(BUILDDIR)

html:
        $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(HTMLDIR)
        @echo
        @echo "Build finished. The HTML pages are in $(HTMLDIR)."