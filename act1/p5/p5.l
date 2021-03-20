
%option nounput
%option noinput


%{
#include <stdio.h>
#include <assert.h>
#include <string.h>

#define MAX_NAME_FILE 100
#define NUM_MACROS 100
#define MACROS_KEY_LENGTH 100
#define MACROS_VALUE 1000

int yywrap();
void find_key(char text[], char key[]);

char filename[MAX_NAME_FILE + 1];

char macros_const_key[NUM_MACROS][MACROS_KEY_LENGTH];
char macros_const_value[NUM_MACROS][MACROS_VALUE];
int current_const_macros = 0;

char macros_func_key[NUM_MACROS][MACROS_KEY_LENGTH];
char macros_func_value[NUM_MACROS][MACROS_VALUE];
int current_func_macros = 0;

%}

%x MULTIPLE_COMMENT INLINE_COMMENT INCLUDE
%x DEFINE MACRO_CONSTANT MACRO_FUNC


patrofitxer [a-zA-Z0-9_]
patromacro [a-zA-Z_][a-zA-Z0-9_]*


%%

\/\/                    BEGIN(INLINE_COMMENT);


<INLINE_COMMENT>\n         BEGIN(0);


<INLINE_COMMENT>.          ;


\/\*                    BEGIN(MULTIPLE_COMMENT);

<MULTIPLE_COMMENT>\*\/           BEGIN(0);

<MULTIPLE_COMMENT>.              ;

<MULTIPLE_COMMENT>\\\n           ;

<MULTIPLE_COMMENT>\n            ;

    
^"#include"[ \t]+          BEGIN(INCLUDE);

<INCLUDE>(\"|\<){patrofitxer}+(\.{patrofitxer}+)?(\"|\>)   { strcpy(filename, &yytext[1]);  
                                                    filename[yyleng - 2] = '\0';            
                                                    yyin = fopen( filename, "r" );
                                                    assert( yyin != NULL );                 
                                                    yypush_buffer_state( yy_create_buffer( yyin, YY_BUF_SIZE ) );
                                                    BEGIN(0);
                                                    }

<INCLUDE>\n                      {printf("Error al incloure l'arxiu.\n"); BEGIN(0);}


^"#define"[ \t]+          BEGIN(DEFINE);

<DEFINE>\n                      {printf("Error al definir la macro.\n"); BEGIN(0);}

<DEFINE>{patromacro}"("({patromacro},)*{patromacro}")"          {printf("Patro Macro amb parametres\n");BEGIN(MACRO_FUNC);}

<DEFINE>{patromacro}       {strcpy(macros_const_key[current_const_macros], yytext);}

<DEFINE>[ \t]+                    {BEGIN(MACRO_CONSTANT);}

<MACRO_FUNC>[^\n]*          {strcpy(macros_func_value[current_func_macros], yytext); current_func_macros++;}

<MACRO_CONSTANT>[^\n]*         {strcpy(macros_const_value[current_const_macros], yytext); current_const_macros++; BEGIN(0);}

<MACRO_CONSTANT>\n           {printf("Error al definir la macro, falta el valor.\n"); BEGIN(0);}


{patromacro}            {char value[MACROS_KEY_LENGTH];
                        find_key(yytext, value);
                        if(strcmp(value, "") != 0)
                        {
                            fprintf(yyout, "%s", value);
                        } else {
                            fprintf(yyout, "%s", yytext);
                        }
                        }

.                     ECHO;

%%

int yywrap(){
    yypop_buffer_state();
    if ( !YY_CURRENT_BUFFER )
        return 1;
    else
        return 0;
}

void find_key(char yytext[], char value[]) {
    for(int i = 0; i < current_const_macros; i++) {
        if (strcmp(yytext, macros_const_key[i]) == 0) {
        
            strcpy(value, macros_const_value[i]);
            return;
        }
    }
    strcpy(value, "");
}


int main( int argc, char *argv[] ) {
    yyin = fopen(argv[1], "r");
    yyout = fopen(argv[2], "w");
    yylex();
    // for (int i = 0; i < current_const_macros; i++) {
    //     printf("KEY: \"%s\", VALUE: \"%s\"\n", macros_const_key[i], macros_const_value[i]);
    // }
    return 0;
}
