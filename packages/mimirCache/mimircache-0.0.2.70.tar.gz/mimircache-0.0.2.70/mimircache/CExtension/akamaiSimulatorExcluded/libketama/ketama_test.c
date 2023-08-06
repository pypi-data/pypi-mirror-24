/*
 * Using a known ketama.servers file, and a fixed set of keys
 * print and hash the output of this program using your modified
 * libketama, compare the hash of the output to the known correct
 * hash in the test harness.
 *
 */

#include <ketama.h>
#include <stdio.h>
#include <stdlib.h>

int main_old(int argc, char **argv)
{
    if(argc==1){
    printf("Usage: %s <ketama.servers file>\n", *argv);
    return 1;
    }

    ketama_continuum c;
    ketama_roll( &c, *++argv );

    printf( "%s\n", ketama_error() );

    int i;
    ketama_print_continuum(c); 


    for ( i = 0; i < 10; i++ )
    {
        char k[10];
        sprintf( k, "%d", i );
        unsigned int kh = ketama_hashi( k );
        mcs* m = ketama_get_server( k, c );

        printf( "%u %u %s\n", kh, m->point, m->ip );
    }
    ketama_smoke(c);
    return 0;
}

int main(int argc, char **argv){

    ketama_continuum c; 

    int num_servers = atoi(argv[1]); 
    double * weight = (double*) malloc(sizeof(double) * num_servers); 
    if (argc > 2){
        if (argc != 2 + num_servers) {
            printf("weight info incorrect\n"); 
            exit(1); 
        }
        for (int i=0; i<num_servers; i++)
            weight[i] = atoi(argv[2+i]); 
    }
    else
        for (int i=0; i<num_servers; i++)
            weight[i] = 1; 

    weight = NULL; 
    if (ketama_build_hashring( &c, num_servers, weight, 1 ) == 0)
        printf("%s\n", ketama_error()); 


    ketama_print_continuum(c); 


    for ( int i = 0; i < 20; i++ )
    {
        char k[10];
        sprintf( k, "%d", i );
        unsigned int kh = ketama_hashi( k );
        int order = ketama_get_server_index(c, k); 

        printf( "%u %d\n", kh, order );
    }
    ketama_smoke(c);
    free(weight); 


    return 0; 
}
