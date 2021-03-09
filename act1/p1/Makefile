
TARGET = python
TEST:=$(shell ls test)
all : $(TARGET)

$(TARGET) : $(TARGET).l
	flex $(TARGET).l
	gcc -Wall lex.yy.c -o $(TARGET) -lfl

clean:
	rm -f *~ lex.yy.c $(TARGET)

tests: clean all
	@for filename in $(TEST); do \
		echo "======" $$filename "======";			\
		./python < test/$$filename; \
	done
