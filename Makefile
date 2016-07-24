.PHONY: test

test:
	mkdir -p tmp/test
	python code/flatten-layout-b test/data/layout-b.csv > tmp/test/flatten-layout-b.csv
	diff test/expected/flatten-layout-b.csv tmp/test/flatten-layout-b.csv
