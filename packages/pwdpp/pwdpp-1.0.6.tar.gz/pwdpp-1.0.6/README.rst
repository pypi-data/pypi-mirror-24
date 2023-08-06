pwdpp
*****
"pwdpp" is a portable pwd (print working directory) written in Python.

Requirements
============
* Python 2.7 or later
* `psutil <http://pythonhosted.org/psutil>`_ if you use the official CPython Windows binary.

Usage
=====
::

    you@yourhost: ~$ pwdpp --help

    usage: pwdpp [-h] [-P] [-L] [-s {bs,fs}] [-W]
    
    Print the full filename of the current working directory.
    
    optional arguments:
      -h, --help            show this help message and exit
      -P, --physical        
                            avoid all symlinks (default).
                            (if your system can reveal symlinks.)
                            
      -L, --logical         
                            use PWD from environment, even if it
                            contains symlinks. 
                            (if your system can't detect symlinks,
                            this option has no effect.)
                            
      -s {bs,fs}, --pathsep {bs,fs}
                            
                            specify path separator.
                            (bs: backslash / fs: forward slash.)
                            
      -W                    
                            print the Win32 value of the physical
                            directory. this is a simple emulation of
                            bash's pwd on MSYS(2). Of course, this makes
                            no sense on *nix.
                            
You might have to set `PYTHONIOENCODING` environment variable, like 'PYTHONIOENCODING=utf-8'.

Motivation
==========
1. bash's builtin pwd of msys and msys2 has windows specific *-W* option for printing the real windows path.
2. but bash's builtin pwd of cygwin doesn't have it.
3. *-W* option is of course windows specific, so we can never use it in \*nix platform.
4. Cygwin, msys, and msys2 each maintain their own mount tables, and the absolute path expressions based thereon are different from each other.

  * If you are in these boxes, normally you want to follow these manners.
  * But sometimes you need to know the path as Windows native path.
  * If so, the lack of *-W* on cygwin's pwd is the matter.


Using pwdpp as Python module
============================
*pwdpp* as a module is very simple, it exposes only two methods and one variable:

::

    >>> import os
    >>> import pwdpp
    >>> pwdpp.__all__
    [u'caller_type', u'curdir', u'main']
    >>> pwdpp.caller_type
    (u'win32', u'mingw32', u'C:\\MinGW\\msys\\1.0\\bin\\sh.exe')
    >>> help(pwdpp.curdir)
    Help on function curdir in module pwdpp:
    
    curdir(physical, winpath=False)
        Return the current directory according to the following rules:
        +---------------+-----------------------------+----------------------+
        | from          | python                      | default              |
        +===============+=============================+======================+
        | cmd.exe       | official CPython on windows | follow the behavior  |
        |               |                             | of windows native.   |
        +---------------+-----------------------------+----------------------+
        | msys          | official CPython on windows | follow the behavior  |
        | (bash, etc.)  +-----------------------------+ of MSYS.             |
        |               | msys CPython? if any,       |                      |
        +---------------+-----------------------------+----------------------+
        | msys2         | official CPython on windows | follow the behavior  |
        | (bash, etc.)  +-----------------------------+ of MSYS2.            |
        |               | msys2 CPython               |                      |
        +---------------+-----------------------------+----------------------+
        | cygwin        | official CPython on windows | follow the behavior  |
        | (bash, etc.)  +-----------------------------+ of cygwin.           |
        |               | cygwin CPython              |                      |
        +---------------+-----------------------------+----------------------+
        | *nix shell    | various                     | follow the behavior  |
        |               |                             | of *nix native.      |
        +---------------+-----------------------------+----------------------+
        Except but the case following windows native, physical=True
        corresponds to "pwd -P", physical=False corresponds to "pwd -L".
        
        If winpath=True, this function follow the behavior of windows native,
        even if cygwin. Of course this makes no sense on real *nix.
    
    >>> pwdpp.curdir(True, True)
    u'c:\\Users\\hhsprings\\work'
    >>> pwdpp.curdir(True, False)
    u'/c/Users\\hhsprings\\work'
    >>> os.chdir("c:/MinGW/msys/1.0/bin")  # my msys root
    >>> pwdpp.curdir(True, True)
    u'c:\\MinGW\\msys\\1.0\\bin'
    >>> pwdpp.curdir(True, False)
    u'\\usr\\bin'
    >>> pwdpp.curdir(True, False).replace(u"\\", u"/")
    u'/usr/bin'

`main` is just an entry point to CLI.

History
=======

1.0.6 (2017-8-09)
~~~~~~~~~~~~~~~~~
* source code is identical to 1.0.3. (just for uploading to pypi.)

1.0.4 - 1.05 (2017-8-09)
~~~~~~~~~~~~~~~~~~~~~~~~
* missing. this is just mistake to upload to pypi.

1.0.3 (2017-8-09)
~~~~~~~~~~~~~~~~~
* fix if cwd is msys root.

1.0.2 (2017-8-09)
~~~~~~~~~~~~~~~~~
* fix if parent is 'env.exe'.
* second item of caller_type was broken...

1.0.1 (2017-8-09)
~~~~~~~~~~~~~~~~~
* fix unicode problem (python 3.x)

1.0.0 (2017-8-09)
~~~~~~~~~~~~~~~~~
* first release
