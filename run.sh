pip3 show tabulate >/dev/null 2>&1 || pip3 install tabulate

rm -rf outputs
mkdir outputs

python ./cleanup-ris.py
python ./cleanup-pubmed.py