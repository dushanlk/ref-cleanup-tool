# `pubmed` and `.ris` duplicate detector

This is to detect duplicates on downloaded references on `.ris` files and `pubmed*.txt` files.

## Pre-requisites

* Python
* Bash

## Limitations

* Only compares `DOI`s.

## How to use

1. Add your `*.ris` and `pubmed*.txt` files to `inputs` dir.
2. Run `./run.sh` script.
3. Check `outputs` dir for output files.
