#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main () {
   setuid(0);
   //I've made a dumb mistake and forgot to rm -rf /tmp/* in this suid, that's why there was file persistence
   system("pkill -u butcher");

   return(0);
} 
