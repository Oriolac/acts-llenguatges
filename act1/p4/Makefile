
TARGET = p4
all : $(TARGET)

$(TARGET) : $(TARGET).l
	flex $(TARGET).l
	gcc -Wall lex.yy.c -o $(TARGET) -lfl

clean:
	rm -f *~ lex.yy.c $(TARGET)

