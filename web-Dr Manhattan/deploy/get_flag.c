#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define _GNU_SOURCE

int main() {
	FILE *fptr ;
	char flag[100];

	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	fptr = fopen("/flag.txt","r");
	fscanf(fptr,"%s",flag);
	printf("%s\n",flag);
	fclose(fptr);

	return 0; 
}
