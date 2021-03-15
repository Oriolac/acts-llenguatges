
%option nounput
%option noinput


%{
#include <stdio.h>
#include <assert.h>

#define MAX_NAME_FILE 100

char filename[MAX_NAME_FILE + 1];

%}

%X MULTIPLE_COMMENT INLINE_COMMENT INCLUDE DEFINE


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


^"#define"[ \t]+            BEGIN(DEFINE);

<DEFINE>\n                      {printf("Error al definir la macro.\n"); BEGIN(0);}

<DEFINE>{patromacro}[ \t]+      {
    
}

\n                              ;

%%

int yywrap(){
    yypop_buffer_state();
    if ( !YY_CURRENT_BUFFER )
        return 1;
    else
        return 0;
}


int main( int argc, char *argv[] ) {
   yylex();
   return 0;
}
