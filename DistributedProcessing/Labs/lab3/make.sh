#!/bin/bash
gcc multiprocessing.c -L. -l_listdyn -Wl,-rpath=. -o multiprocessing.out