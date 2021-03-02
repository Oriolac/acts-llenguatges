%option nounput
%option noinput

%{
#define RESERVED_KEYWORD 1
#define NUMBER 2
#define COMMENT 3
%}
%%

("False")|("None")|("True")|("and")|("as")|("assert")|("async")|("await")|("break")|("class")|("continue")|("def")|("del")|("elif")|("else")|("except")|("finally")|("for")|("from")|("global")|("if")|("import")|("in")|("is")|("lambda")|("nonlocal")|("not")|("or")|("pass")|("raise")|("return")|("try")|("while")|("with")|("yield") return RESERVED_KEYWORD;

[0-9]+	|

[0-9]*\.[0-9]+		return NUMBER;

#.*	|
\"{3}.*\"{3}			return COMMENT;	
%%

#include <stdio.h>

int main(){
  int val;

  while ((val=yylex())!=0)
	printf("El token identificat te codi %d\n",val);
}

int yywrap(){
	return(1);
}

