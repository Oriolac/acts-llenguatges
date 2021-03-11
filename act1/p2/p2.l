
%option nounput
%option noinput

%{

#define LITERAL 1
#define IMPLICACIO 2
#define DOBLE_IMPLICACIO 3
#define ERROR -1

#define LINE_BUFFER 200

%}

%x panic
%x comment

%%

<panic>"\n"     BEGIN(0);

<panic>.    ;

#           BEGIN(comment);

<comment>[^\n]       ;

<comment>\n     BEGIN(0); return '\n';

[A-Z]       {return LITERAL;}

"!"         return '!';

"^"         return '^';

"∨"         return 'v';

"->"       return IMPLICACIO;

"<->"       return DOBLE_IMPLICACIO;

"("         return '(';

")"         return ')';

"\n"        return '\n';

" "         |
"\t"         ;

.           {BEGIN(panic); return ERROR;}

%%

#include <stdio.h>

int main() {
    char val;
    int num_line = 1;
    int bad_lines = 0;
    while ((val=yylex())!=0) {
        if (val == '\n') {
            num_line++;
        } else if (val == ERROR) {
            printf("Error caràcter \"%c\" no vàlid a la línea %i:\n", yytext[0], num_line);
            num_line++;
            bad_lines++;
        }
	}
    printf("Un total de %i línies errònees.\n", bad_lines);
}