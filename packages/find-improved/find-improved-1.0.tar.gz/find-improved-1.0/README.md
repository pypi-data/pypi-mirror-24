# fim - fIND imPROVED

Usage::

    fim [options] (-|PATH...) [-e CMD]
    
Options::

    -e CMD --cmd=CMD           the command to run, with applied substitutions
                               if specified, on each argument [default: echo]
    -s SUBSTR --substr=SUBSTR  substitution string [default: {}]
    -q --quiet                 suppress echo of the commands being executed
    -d --dry                   do not execute commands
    -x --exit-on-interrupt     exit script on interrupt signal, do not
                               continue executing commands
    -p N --procs=N             run N subprocesses concurrently using
                               multiprocess
    -g --glob                  do not omit arguments that look like globs - use
                               with care!

Like `find -exec` or `xargs` but can specify more complicated commands, e.g.
pipe-chained commands, redirections, etc. and more sophisticated substitutions.
fim takes as input either a list of paths or new line delimited input taken from
standard input and executes a command on each.

The command is specified as the argument to `-e CMD|--cmd=CMD`, which should be a quoted
command that can be run on the command line after replacing the substitution
string with the input line.

The substitution string must be two characters (default {}), and can take the
following forms:

- `{}` : substitute the input argument as is in the command

- `{s:patt:repl:[gi]}` : do on-the-fly substitutions of the input argument (e.g.,
  stripping extensions). `patt` and `repl` are passed to `re.sub` like
  `re.sub(patt,repl,{})`
  
- `{c:command %s}` form for executing embedded commands on the input argument
  (e.g. `basename`).
  
If no substution string is supplied in the `CMD` argument each argument is
appended to the `CMD`.

Examples::

    $ seq 1 3 | fim - -e 'seq 1 {} > {}.txt'
    seq 1 1 > 1.txt
    seq 1 2 > 2.txt
    seq 1 3 > 3.txt
    $ ls
    1.txt 2.txt 3.txt
    $ fim *.txt -e 'mv {} number_{}'
    mv 1.txt number_1.txt
    mv 2.txt number_2.txt
    mv 3.txt number_3.txt
    $ ls
    number_1.txt number_2.txt number_3.txt
    $ fim *.txt -e 'cp {} {s:number_(\d).txt:number_\1by\1.txt:}'
    cp number_1.txt number_1by1.txt
    cp number_2.txt number_2by2.txt
    cp number_3.txt number_3by3.txt
    $ ls
    number_1.txt number_1by1.txt number_2.txt number_2by2.txt number_3.txt
    number_3by3.txt
    $ fim *by* -e 'echo number | cat - {} > {s:.txt:_label.txt:}'
    echo number | cat - number_1by1.txt > number_1by1_label.txt
    echo number | cat - number_2by2.txt > number_2by2_label.txt
    echo number | cat - number_3by3.txt > number_3by3_label.txt
    $ ls *_label.txt
    number_1by1_label.txt number_2by2_label.txt number_3by3_label.txt
    $ fim *_label.txt -e 'ln -s {} symlink_to_{}'
    ln -s number_1by1_label.txt symlink_to_number_1by1_label.txt
    ln -s number_2by2_label.txt symlink_to_number_2by2_label.txt
    ln -s number_3by3_label.txt symlink_to_number_3by3_label.txt
    $ ls *_label.txt
    symlink_to_number_1by1_label.txt symlink_to_number_2by2_label.txt
    symlink_to_number_3by3_label.txt
    $ fim *_label.txt -e 'mv {} {c:basename %s .txt}.pdf' # rename .txt to .pdf
    mv number_1by1_label.txt number_1by1_label.pdf
    mv number_2by2_label.txt number_2by2_label.pdf
    mv number_3by3_label.txt number_3by3_label.pdf
    $ ls *.pdf
    number_1by1_label.pdf number_2by2_label.pdf number_3by3_label.pdf
  

