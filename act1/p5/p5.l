
%option nounput
%option noinput


%{
#include <stdio.h>
#include <assert.h>

#define MAX_NAME_FILE 100

char filename[MAX_NAME_FILE + 1];

%}

%X MULTIPLE_COMMENT INLINE_COMMENT INCLUDE


patrofitxer [a-zA-Z0-9_ ]


%%

\/\/                    BEGIN( INLINE_COMMENT );


<INLINE_COMMENT>\n         BEGIN( INITIAL );


<INLINE_COMMENT>.          ;


\/\*                    BEGIN( MULTIPLE_COMMENT );

<MULTIPLE_COMMENT>\*\/           BEGIN( INITIAL );

<MULTIPLE_COMMENT>.              ;

<MULTIPLE_COMMENT>\\\n           ;

<MULTIPLE_COMMENT>\n             {   printf("ERROR FORMAT COMENTARI");
                            BEGIN( INITIAL );
                        }
    
^"#include"[ \t]+          BEGIN( INCLUDE );

<INCLUDE>(\"|\<){patrofitxer}+(\.{patrofitxer}+)?(\"|\>)   { strcpy( filename, &yytext[1] );            /* treiem les comestes inicials */
                                                    filename[ yyleng-2 ] = '\0';               /* treiem les comestes finals */
                                                    yyin = fopen( filename, "r" );
                                                    assert( yyin != NULL );                     /* filename ok? */
                                                    yypush_buffer_state( yy_create_buffer( yyin, YY_BUF_SIZE ) );
                                                    BEGIN( INITIAL );
                                                    }

%%

int yywrap(){
    yypop_buffer_state();
    if ( !YY_CURRENT_BUFFER )
        return 1;
    else
        return 0;
}


int main( int argc, char *argv[] ) {
   yyin = fopen( argv[ 1 ], "r" );
   yylex();
   return 0;
}
