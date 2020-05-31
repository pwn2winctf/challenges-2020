#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "emojinet.h"


int main(){
	int c=0;
	int j;


	char *flag="CTF-BR{Tr4nsc3ndence_R3bell10n_wiLl_W1n}";
	while (1){
	    for (int i=0;flag[i]!='\0';i++){
	      c=printTranslate(flag[i],160);

	      usleep(10); 
	    }



	      printf("\n");
	      for(j=0;j<30;j++){
	        printf("-");
	      }
	      printf(" End of transmission ");
	      for(j=0;j<30;j++){
	        printf("-");
	      }
	      printf("\n");


	    
	  usleep(5000);
	}
	return c;
        

}

