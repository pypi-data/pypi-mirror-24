Princeton Bibliography Reducer
==============================

This is a package for reducing LaTeX *.bib* files to include just what you want.

Shameless plug: check out our book_.

.. _book: https://www.crcpress.com/Neuromorphic-Photonics/Prucnal-Shastri/p/book/9781498725224

Made by Alex Tait

Installation
------------
``$ pip install princeton-bibreduce``

Usage
-----
There are three ways to call the same thing

1: UNIX command line executable::

    $ princeton-bibreduce -cu myManuscript.aux

2: python command line::

    $ python -m bibreduce -cu myManuscript.aux

3: from python code::

    import bibreduce
    bibreduce.main('myManuscript.aux', coauthors=True, urlLinks=True)

Behavior
--------
Generates a *.bib* file. By default, it adds the ``_proc`` suffix to the generated *.bib*. The customizable fields are:

* title (flag -t)
* coauthors (flag -c)
* doiLinks (flag -d)
* urlLinks (flag -u)
* abstract (flag -a)

Specifying the flag transfers that field. All fields not on this list are transferred over.

Get more help with::

    $ princeton-bibreduce -h

**Special behavior for links**

If a link format is specified, it populates the field ``link``. For urlLinks, it just copies over what is in the ``url`` field. For doiLinks, it puts "\http://dx.doi.org/thedoi" in the ``link`` field.

Typical TeX workflow
--------------------
The goal here is to remove titles from references and try to add URLs.

**(optional) Centralized bib libraries**

Suppose you have a centralized bib library ``MasterLibrary.bib`` Bib globals should go in

    OSX: ``~/Library/texmf/bibtex/bib/local/MasterLibrary.bib``

    Linux: ``~/texmf/bibtex/bib/local/MasterLibrary.bib``

    Windows: ``C:\Users\<user name>\texmf\bibtex\bib\local\MasterLibrary.bib``

**The TeX file**

Suppose you are then working on a TeX file ``myManuscript.tex`` containing::

    \begin{document}
    The text of your paper.
    ...
    \bibliography{MasterLibrary}
    \end{document}

This will pull from your centralized library.

**Flow**

Compile it with::

    $ pdflatex myManuscript.tex
    $ bibtex myManuscript.aux
    $ pdflatex myManuscript.tex

Your *.aux* file includes everything you need to extract a *.bib* that is specific to this manuscript. This is where you use this module::

    $ princeton-bibreduce myManuscript.aux -cu

to generate ``myManuscript_proc.bib``. Now, go back to the *.tex* file and change the bibliography to the reduced one::

    \bibliography{myManuscript_proc}

One more time, call::

    $ pdflatex myManuscript.tex
    $ bibtex myManuscript.aux
    $ pdflatex myManuscript.tex
