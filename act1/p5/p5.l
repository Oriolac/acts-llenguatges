
%option nounput
%option noinput


%{
#include <stdio.h>
#include <assert.h>
#include <string.h>

#define MAX_NAME_FILE 20
#define NUM_MACROS 50
#define MACROS_KEY_LENGTH 20
#define MACROS_VALUE 1000
#define NUM_ARGS_MACRO 10
#define MAX_LENGHT_ARG_STR 10
#define NO_FMACRO "NOT FOUND"

struct ExpansionMacro {
    int num_args;
    char key[MACROS_KEY_LENGTH];
    char args[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR];
    char value[MACROS_VALUE];
};

int yywrap();

void find_const_key(char text[], char key[]);
struct ExpansionMacro find_func_key(char text[]);
void print_fmacro(struct ExpansionMacro fmacro);
void add_arg(struct ExpansionMacro *fmacro, char arg[]);
void transform_text(struct ExpansionMacro macro, char args[]);
void replace_words(char margs[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], char args[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], char text[], int num_args);
char *replace_or_repeat_word(char *tok, char margs[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], char args[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], int num_args);

char filename[MAX_NAME_FILE + 1];

char macros_const_key[NUM_MACROS][MACROS_KEY_LENGTH];
char macros_const_value[NUM_MACROS][MACROS_VALUE];
int current_const_macros = 0;

char macros_func_key[NUM_MACROS][MACROS_KEY_LENGTH];
struct ExpansionMacro macros_func_value[NUM_MACROS];
int current_func_macros = 0;

%}

%x MULTIPLE_COMMENT INLINE_COMMENT INCLUDE
%x DEFINE MACRO_CONSTANT
%x MACRO_FUNC READ_ARG


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


^"#define"[ \t]+          {BEGIN(DEFINE);}

<DEFINE>\n                      {printf("Error al definir la macro.\n"); BEGIN(0);}

<DEFINE>{patromacro}"("          {  
                                    yytext[yyleng - 1] = '\0';
                                    strcpy(macros_func_key[current_func_macros], yytext);
                                    strcpy(macros_func_value[current_func_macros].key, yytext);
                                    macros_func_value[current_func_macros].num_args = 0;
                                    BEGIN(READ_ARG);
                                }

<READ_ARG>{patromacro}", "          {
                                        yytext[yyleng-2] = '\0';
                                        add_arg(&macros_func_value[current_func_macros], yytext);
                                        
                                    }   

<READ_ARG>{patromacro}") "      {
                                yytext[yyleng-2] = '\0';
                                add_arg(&macros_func_value[current_func_macros], yytext);
                                BEGIN(MACRO_FUNC);
                                }

<DEFINE>{patromacro}       {strcpy(macros_const_key[current_const_macros], yytext);}

<DEFINE>[ \t]+                    {BEGIN(MACRO_CONSTANT);}

<MACRO_FUNC>[^\n]*          {
                                strcpy(macros_func_value[current_func_macros].value, yytext);
                                current_func_macros++;
                                BEGIN(0);
                            }

<MACRO_CONSTANT>[^\n]*         {strcpy(macros_const_value[current_const_macros], yytext); current_const_macros++; BEGIN(0);}

<MACRO_CONSTANT>\n           {printf("Error al definir la macro, falta el valor.\n"); BEGIN(0);}


{patromacro}\((" "*[a-zA-Z0-9_]+" "*," "*)*[a-zA-Z0-9_]+" "*\)       {
                                                                        char delim[] = "(";
                                                                        char *key = strtok(yytext, delim);
                                                                        struct ExpansionMacro macro = find_func_key(key);
                                                                        if (strcmp(macro.key, NO_FMACRO) == 0)
                                                                        {
                                                                            fprintf(yyout, "%s", yytext);
                                                                        } else {
                                                                            char *args = strtok(NULL, delim);
                                                                            args[strlen(args) - 1] = '\0';
                                                                            transform_text(macro, args);
                                                                        }
                                                                    }

{patromacro}            {char value[MACROS_KEY_LENGTH];
                        find_const_key(yytext, value);
                        if(strcmp(value, "") != 0)
                        {
                            fprintf(yyout, "%s", value);
                        } else {
                            fprintf(yyout, "%s", yytext);
                        }
                        }

\n                      ECHO;

.                     ECHO;

%%

int yywrap(){
    yypop_buffer_state();
    if ( !YY_CURRENT_BUFFER )
        return 1;
    else
        return 0;
}

void transform_text(struct ExpansionMacro macro, char argstext[]) { 
    char *delim = ",";
    char arguments[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR];
    char *tok = strtok(argstext, delim);
    int j = 0;
    char text[MACROS_VALUE];
    while (tok != NULL) {
        strcpy(arguments[j], tok);
        j++;
        tok = strtok(NULL, delim);
    }
    strcpy(text, macro.value);
    replace_words(macro.args, arguments, text, macro.num_args);
    fprintf(yyout, "%s", text);
}

void replace_words(char margs[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], char args[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], char text[], int num_args) {
    char *delim = " ";
    char *tok = strtok(text, delim);
    char result[MACROS_VALUE] = "";
    while (tok != NULL) {
        char *word = replace_or_repeat_word(tok, margs, args, num_args);
        strcat(result, word);
        strcat(result, " ");
        tok = strtok(NULL, delim);
    }
    strcpy(text, result); 
}

char *replace_or_repeat_word(char *tok, char margs[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], char args[NUM_ARGS_MACRO][MAX_LENGHT_ARG_STR], int num_args) {
    for(int i = 0; i < num_args; i++) {
        if (strcmp(tok, margs[i]) == 0) {
            return args[i];
        }
    }
    return tok;
}

void print_fmacro(struct ExpansionMacro fmacro) {
    printf("Macro %s [%i](", fmacro.key, fmacro.num_args);
    for(int i= 0; i < fmacro.num_args -1; i++)
    {
        printf("%s, ", fmacro.args[i]);
    }
    printf("%s) {\n", fmacro.args[fmacro.num_args-1]);
    printf("\t%s\n}\n", fmacro.value);
}

void add_arg(struct ExpansionMacro *fmacro, char arg[]) {
    strcpy(fmacro->args[fmacro->num_args], arg);
    fmacro->num_args++;
}

void find_const_key(char yytext[], char value[]) {
    for(int i = 0; i < current_const_macros; i++) {
        if (strcmp(yytext, macros_const_key[i]) == 0) {
            strcpy(value, macros_const_value[i]);
            return;
        }
    }
    strcpy(value, "");
}

struct ExpansionMacro find_func_key(char text[]) {
    for(int i = 0; i < current_func_macros; i++) {
        if (strcmp(macros_func_value[i].key, text) == 0) {
            return macros_func_value[i];
        }
    }
    struct ExpansionMacro nomacro;
    strcpy(nomacro.key, NO_FMACRO);
    return nomacro;
}

int main( int argc, char *argv[] ) {
    yyin = fopen(argv[1], "r");
    yyout = fopen(argv[2], "w");
    yylex();
    return 0;
}