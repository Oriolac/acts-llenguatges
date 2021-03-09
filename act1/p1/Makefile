
TARGET = python
TEST:=$(shell ls test)
all : $(TARGET)

$(TARGET) : $(TARGET).l
	flex $(TARGET).l
	gcc -Wall lex.yy.c -o $(TARGET) -lfl

clean:
	@rm -f *~ lex.yy.c $(TARGET)

test: clean all
	@printf "`tput bold`Choose one of the following tests:\n`tput sgr0`"
	@echo $(TEST);	\
	read filename;	\
	printf "`tput bold`====== Testing $$filename ======`tput sgr0`\n";	\
	./python < test/$$filename;

tests: clean all
	@for filename in $(TEST); do \
		echo "======" $$filename "======";			\
		./python < test/$$filename; \
	done
