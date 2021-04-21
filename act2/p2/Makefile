TARGET = p2
TEST:=$(shell ls test)
all : $(TARGET)

$(TARGET) : $(TARGET).tab.c $(TARGET).l
	flex $(TARGET).l
	gcc -Wall $(TARGET).tab.c lex.yy.c -o $(TARGET) -lfl


$(TARGET).tab.c: $(TARGET).y
	$(YACC) -d -v $(TARGET).y -o $(TARGET).tab.c

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