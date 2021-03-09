
%option nounput
%option noinput

%{
#define KEY_False 1
#define KEY_None 2
#define KEY_True 3
#define KEY_and 4
#define KEY_as 5
#define KEY_assert 6
#define KEY_async 7
#define KEY_await 8
#define KEY_break 9
#define KEY_class 10
#define KEY_continue 11
#define KEY_def 12
#define KEY_del 13
#define KEY_elif 14
#define KEY_else 15
#define KEY_except 16
#define KEY_finally 17
#define KEY_for 18
#define KEY_from 19
#define KEY_global 20
#define KEY_if 21
#define KEY_import 22
#define KEY_in 23
#define KEY_is 24
#define KEY_lambda 25
#define KEY_nonlocal 26
#define KEY_not 27
#define KEY_or 28
#define KEY_pass 29
#define KEY_raise 30
#define KEY_return 31
#define KEY_try 32
#define KEY_while 33
#define KEY_with 34
#define KEY_yield 35

#define CONSTANT 36
#define COMMENT 37
#define IDENTIFIERS 38
#define OPERATORS 39
#define DELIMITING_SYMBOL 40
#define SEPARATING_SYMBOL 41
#define OTHER 42

#define NUM_RESERVED_WORDS 34
#define NUM_TOKENS 8

unsigned char string_buffer[200];
%}

%%

%{
	/* Seccio de REGLES */

%}

#.*	|

\"{3}[.\n]*\"{3}			return COMMENT;

" " |

\t			return SEPARATING_SYMBOL;

False			return KEY_False;
None			return KEY_None;
True			return KEY_True;
and			return KEY_and;
as			return KEY_as;
assert			return KEY_assert;
async			return KEY_async;
await			return KEY_await;
break			return KEY_break;
class			return KEY_class;
continue			return KEY_continue;
def			return KEY_def;
del			return KEY_del;
elif			return KEY_elif;
else			return KEY_else;
except			return KEY_except;
finally			return KEY_finally;
for			return KEY_for;
from			return KEY_from;
global			return KEY_global;
if			return KEY_if;
import			return KEY_import;
in			return KEY_in;
is			return KEY_is;
lambda			return KEY_lambda;
nonlocal			return KEY_nonlocal;
not			return KEY_not;
or			return KEY_or;
pass			return KEY_pass;
raise			return KEY_raise;
return			return KEY_return;
try			return KEY_try;
while			return KEY_while;
with			return KEY_with;
yield			return KEY_yield;

[0-9]+	|

[0-9]*\.[0-9]+		return CONSTANT;

[A-Za-z_][A-Za-z0-9_]+		return IDENTIFIERS;


.				return OTHER;

%%

#include <stdio.h>

int main(){
	int val;
	int freq_tokens[NUM_TOKENS];
	char *name_tokens[NUM_TOKENS] = {
		"Paraules reservades",
		"Constants",
		"Comentaris",
		"Identificadors",
		"Operadors",
		"Símbols delimitadors",
		"Símbols de separació",
		"Altres"
	};
	for(int i=0; i < NUM_TOKENS; i++) {
		freq_tokens[i] = 0;
	}
	while ((val=yylex())!=0) {
		printf("%i", val);
		if(val < NUM_RESERVED_WORDS) {
			freq_tokens[1]++;
		} else {
			freq_tokens[val-NUM_RESERVED_WORDS - 1]++;
		}
	}
	for(int i=0; i < NUM_TOKENS; i++) {
		printf("%s: %i\n", name_tokens[i], freq_tokens[i]);
	}
}

// ; és fi d'instrucció i \n és delimitador

int yywrap(){
	return(1);
}

