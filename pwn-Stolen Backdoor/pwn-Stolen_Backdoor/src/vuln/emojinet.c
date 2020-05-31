#include <stdio.h>
#include <wchar.h>
#include <locale.h>
#include "emojis.h"


int printTranslate(char text,unsigned granularity){

	wchar_t wordp;	
	unsigned translated=(unsigned)(text-'-');
	if (text<'-' || text > '}'){
	  return -1;
	}
	if (  translated*granularity>LEN_LIB   ){
	  return -2;
	}
		
	
	wordp=emojiLib[translated * granularity];
	setlocale(LC_ALL, "en_US.utf8");
	printf("%lc",wordp);
	return 0;
}
wchar_t *getEmojis(){
	return emojiLib;
}
