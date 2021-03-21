%option nounput
%option noinput

%{

#define SYMBOL 1
#define LAMBDA 2
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

"BUIDA"     |
"buida"     return LAMBDA;

[a-d]       return SYMBOL;

"|"         return '|';

"."         return '.';

"*"         return '*';

"+"         return '+';

"?"         return '?';

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
        printf("%s ", yytext);
        if (val == '\n') {
            num_line++;
        } else if (val == ERROR) {
            printf("Error caràcter \"%c\" no vàlid a la línea: %i\n", yytext[0], num_line);
            num_line++;
            bad_lines++;
        }
	}
    printf("Un total de %i línies errònees.\n", bad_lines);
}