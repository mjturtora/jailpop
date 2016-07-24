.PHONY: test

test:
	mkdir -p tmp/test
	python code/flatten-layout-b test/data/layout-b.csv > tmp/test/flatten-layout-b.csv
	diff test/expected/flatten-layout-b.csv tmp/test/flatten-layout-b.csv

prod:
	for f in data/hcso-scrape/layout-b-*.csv; do code/flatten-layout-b $$f; done > tmp/layout-b.csv
