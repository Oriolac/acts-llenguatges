TARGET = p3
TEST:=$(shell ls test)
all : $(TARGET)

$(TARGET) : $(TARGET).l
	flex $(TARGET).l
	gcc -Wall lex.yy.c -o $(TARGET) -lfl

clean:
	@rm -f *~ lex.yy.c $(TARGET)

test: clean all
	@printf "`tput bold`Choose one of the following tests:\n`tput sgr0`";	\
	printf "$(TEST)\n";	\
	read filename;	\
	printf "`tput bold`====== Testing $$filename ======`tput sgr0`\n";	\
	./$(TARGET) < test/$$filename;

tests: clean all
	@for filename in $(TEST); do \
		echo "======" $$filename "======";			\
		./$(TARGET) < test/$$filename; \
	done

try: clean all
	./$(TARGET)