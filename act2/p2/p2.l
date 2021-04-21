
%{

#include "p2.tab.h"
#include "stdio.h"

int nlin = 0;

%}

%option nounput
%option noinput
%option noyywrap

%%

[0-9]+       {yylval.valor = atoi(yytext); return(INTEGER);}


";"         {nlin++;return(yytext[0]);}

" "         |
"\t"        |
"\n" ;

.           {return(yytext[0]);}
