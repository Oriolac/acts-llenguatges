%{

#include<stdio.h>
#include<ctype.h>

extern int yylex(void);
void yyerror (char const *);
extern int nlin;

%}


%start fitxer

%union{int valor;
    char word[20];
    struct stack{
        char word[20];
        struct stack *below;
    };}

%token <valor> INTEGER
%token <word> '+'

%left '+' '-'
%left '*' '/' '%'

%type <word> expr sentencia fitxer

%%

fitxer:         sentencia
      |         fitxer sentencia
      ;

sentencia:      ';'  {;}
         |      expr ';'        {printf("Línea: %s\n", $1);}
         |      error ';'       {fprintf(stderr,"ERROR EXPRESSIO INCORRECTA Línea %d \n", nlin);
                                                    yyerrok;	}
         ;


expr:   '(' expr ')' {sprintf($$, "%s", $2);}
    |   expr '+' expr {sprintf($$, "%s + %s", $1, $3);}
    |   INTEGER {sprintf($$, "%d", $1);}
    ;

%%

/* Called by yyparse on error. */

void yyerror (char const *s){
    fprintf (stderr, "%s\n", s);
}

int main(){
    
    if (yyparse()==0){
        return(0);
    } else{
    return(1);
    }
    
}
