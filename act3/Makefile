TEST:=$(shell ls tests)

one:
	python3 main.py one.txt

all:
	@for filename in $(TEST); do \
		echo "======" $$filename "======";			\
		python3 main.py tests/$$filename; \
	done

clean:
	rm parser.out
	rm parsetab.py
