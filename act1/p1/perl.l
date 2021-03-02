%option nounput
%option noinput

%{
#define KEY_NULL		    0
#define KEY___FILE__		1
#define KEY___LINE__		2
#define KEY___PACKAGE__		3
#define KEY___DATA__		4
#define KEY___END__		    5
#define KEY___SUB__		    6
#define KEY_AUTOLOAD		7
#define KEY_BEGIN		    8
#define KEY_UNITCHECK		9
#define KEY_DESTROY		    10
#define KEY_END			    11
#define KEY_INIT		    12
#define KEY_CHECK		    13
#define KEY_abs			    14
#define KEY_accept		    15
#define KEY_alarm		    16
#define KEY_and			17
#define KEY_atan2		18
#define KEY_bind		19
#define KEY_binmode		20
#define KEY_bless		21
#define KEY_break		22
#define KEY_caller		23
#define KEY_catch		24
#define KEY_chdir		25
#define KEY_chmod		26
#define KEY_chomp		27
#define KEY_chop		28
#define KEY_chown		29
#define KEY_chr			30
#define KEY_chroot		31
#define KEY_close		32
#define KEY_closedir		33
#define KEY_cmp			34
#define KEY_connect		35
#define KEY_continue		36
#define KEY_cos			37
#define KEY_crypt		38
#define KEY_dbmclose		39
#define KEY_dbmopen		40
#define KEY_default		41
#define KEY_defined		42
#define KEY_delete		43
#define KEY_die			44
#define KEY_do			45
#define KEY_dump		46
#define KEY_each		47
#define KEY_else		48
#define KEY_elsif		49
#define KEY_endgrent		50
#define KEY_endhostent		51
#define KEY_endnetent		52
#define KEY_endprotoent		53
#define KEY_endpwent		54
#define KEY_endservent		55
#define KEY_eof			56
#define KEY_eq			57
#define KEY_eval		58
#define KEY_evalbytes		59
#define KEY_exec		60
#define KEY_exists		61
#define KEY_exit		62
#define KEY_exp			63
#define KEY_fc			64
#define KEY_fcntl		65
#define KEY_fileno		66
#define KEY_flock		67
#define KEY_for			68
#define KEY_foreach		69
#define KEY_fork		70
#define KEY_format		71
#define KEY_formline		72
#define KEY_ge			73
#define KEY_getc		74
#define KEY_getgrent		75
#define KEY_getgrgid		76
#define KEY_getgrnam		77
#define KEY_gethostbyaddr	78
#define KEY_gethostbyname	79
#define KEY_gethostent		80
#define KEY_getlogin		81
#define KEY_getnetbyaddr	82
#define KEY_getnetbyname	83
#define KEY_getnetent		84
#define KEY_getpeername		85
#define KEY_getpgrp		86
#define KEY_getppid		87
#define KEY_getpriority		88
#define KEY_getprotobyname	89
#define KEY_getprotobynumber	90
#define KEY_getprotoent		91
#define KEY_getpwent		92
#define KEY_getpwnam		93
#define KEY_getpwuid		94
#define KEY_getservbyname	95
#define KEY_getservbyport	96
#define KEY_getservent		97
#define KEY_getsockname		98
#define KEY_getsockopt		99
#define KEY_given		100
#define KEY_glob		101
#define KEY_gmtime		102
#define KEY_goto		103
#define KEY_grep		104
#define KEY_gt			105
#define KEY_hex			106
#define KEY_if			107
%}

KEY_NULL NULL
KEY___FILE__ __FILE__
KEY___LINE__ __LINE__
KEY___PACKAGE__ __PACKAGE__
KEY___DATA__ __DATA__
KEY___END__ __END__
KEY___SUB__ __SUB__
KEY_AUTOLOAD AUTOLOAD
KEY_BEGIN BEGIN
KEY_UNITCHECK UNITCHECK
KEY_DESTROY DESTROY
KEY_END END
KEY_INIT INIT
KEY_CHECK CHECK
KEY_abs abs
KEY_accept accept
KEY_alarm alarm
KEY_and and
KEY_atan2 atan2
KEY_bind bind
KEY_binmode binmode
KEY_bless bless
KEY_break break
KEY_caller caller
KEY_catch catch
KEY_chdir chdir
KEY_chmod chmod
KEY_chomp chomp
KEY_chop chop
KEY_chown chown
KEY_chr chr
KEY_chroot chroot
KEY_close close
KEY_closedir closedir
KEY_cmp cmp
KEY_connect connect
KEY_continue continue
KEY_cos cos
KEY_crypt crypt
KEY_dbmclose dbmclose
KEY_dbmopen dbmopen
KEY_default default
KEY_defined defined
KEY_delete delete
KEY_die die
KEY_do do
KEY_dump dump
KEY_each each
KEY_else else
KEY_elsif elsif
KEY_endgrent endgrent
KEY_endhostent endhostent
KEY_endnetent endnetent
KEY_endprotoent endprotoent
KEY_endpwent endpwent
KEY_endservent endservent
KEY_eof eof
KEY_eq eq
KEY_eval eval
KEY_evalbytes evalbytes
KEY_exec exec
KEY_exists exists
KEY_exit exit
KEY_exp exp
KEY_fc fc
KEY_fcntl fcntl
KEY_fileno fileno
KEY_flock flock
KEY_for for
KEY_foreach foreach
KEY_fork fork
KEY_format format
KEY_formline formline
KEY_ge ge
KEY_getc getc
KEY_getgrent getgrent
KEY_getgrgid getgrgid
KEY_getgrnam getgrnam
KEY_gethostbyaddr gethostbyaddr
KEY_gethostbyname gethostbyname
KEY_gethostent gethostent
KEY_getlogin getlogin
KEY_getnetbyaddr getnetbyaddr
KEY_getnetbyname getnetbyname
KEY_getnetent getnetent
KEY_getpeername getpeername
KEY_getpgrp getpgrp
KEY_getppid getppid
KEY_getpriority getpriority
KEY_getprotobyname getprotobyname
KEY_getprotobynumber getprotobynumber
KEY_getprotoent getprotoent
KEY_getpwent getpwent
KEY_getpwnam getpwnam
KEY_getpwuid getpwuid
KEY_getservbyname getservbyname
KEY_getservbyport getservbyport
KEY_getservent getservent
KEY_getsockname getsockname
KEY_getsockopt getsockopt
KEY_given given
KEY_glob glob
KEY_gmtime gmtime
KEY_goto goto
KEY_grep grep
KEY_gt gt
KEY_hex hex
KEY_if if


%%

{KEY_NULL}      printf("NULL");
%%

#include <stdio.h>

int main(){
  yylex();
}

