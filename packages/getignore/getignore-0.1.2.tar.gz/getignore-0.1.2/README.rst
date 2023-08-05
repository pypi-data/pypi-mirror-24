==========
Getignorer
==========

Command line utility to fetch common .gitignore files

Installation
============

Install through PyPi::

    λ pip install getignore

Usage
=====

Enter a variable number of language to create the .gitignore file from::

    λ getignore Python Haskell

Output location can be change with -o (default is .gitignore)::

    λ getignore Python -o sample.txt

Output can be previewed with --preview::

    λ getignore --preview

Omitting languages from the command will show a prompt::

    λ getignore        
    Enter programing languages separated by commas in the prompt below
        Press <TAB> to see available completions
        E.g. Python, Go, Node

    Enter languages >   

For a full rundown of available options::

    λ getignore --help
