TEST:=$(shell ls tests)

all:
	@for filename in $(TEST); do \
		echo "======" $$filename "======";			\
		python3 main.py tests/$$filename; \
	done

one:
	python3 main.py one.txt

clean:
	rm parser.out
	rm parsetab.py
