#include<ctype.h>
#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h> 
#include<math.h>
#include<assert.h>
#include<unistd.h>
#include<string.h>

bool* get_rule_transitions(int rule){
    bool* rule_transitions = malloc(8);
    for(int i = 8,k; i >= 0; i--)
        rule_transitions[7-i] = (rule >> i) & 1;
    return rule_transitions;
}

bool* get_neighbors(int x, bool* space, int w){
    bool* neighbors = malloc(3);
    neighbors[0] = x == 0 ? space[w-1] : space[x-1];
    neighbors[1] = space[x];
    neighbors[2] = x == w - 1 ? space[0] : space[(x+1)%w];
    return neighbors;
}

int get_transition_index(bool* neighbors){
    return 7 - ((neighbors[0] << 2) + (neighbors[1] << 1) + neighbors[2]);
}

int quantize_energy(bool* space, int w){
    int energy = 0;
    for(int i=0; i < w; i++)
        energy += space[i];
    return energy;
}

bool is_spacetime_conservative(bool** spacetime, int w, int t){
    int init_energy = quantize_energy(spacetime[0], w);
    for(int i=1; i < t; i++)
        if(quantize_energy(spacetime[i], w) != init_energy)
            return false;
    return true;
}

bool** gen_space_combo(int w){
    bool** space_combo = malloc(pow(2,w));
    for(int i=0; i < pow(2,w); i++){
        bool* space = malloc(8);
        for (int j = 0, z = w; j < 8; j++, z <<= 1)
            space[j] = (w & (1U << 7)) ? 1 : 0;
        space_combo[i] = space;
    }
    return space_combo;
}

bool** run_async(int rule, int t, int w, int* ranks, bool* init_space){
    bool* rule_transitions = get_rule_transitions(rule);
    bool* space = malloc(w);
    bool** spacetime = malloc(t*sizeof(bool*));
    space = memcpy(space, init_space, w);
    for(int ti=0; ti < t; ti++){
        bool* future_space = malloc(w);
        future_space = memcpy(space, init_space, w);
        for(int p=1; p <= 8; p++){
            for(int x=0; x < w; x++){
                bool* neighbors = get_neighbors(x, space, w);
                int ix = get_transition_index(neighbors);
                for(int i=0; i < 8; i++){
                    if(ranks[ix] == p){
                        future_space[x] = rule_transitions[ix];
                    }
                }
            }
            space = future_space;
        }
        spacetime[ti] = future_space;
    }
    return spacetime;
}

bool is_rule_conservative(int rule, int t, int w, int* ranks){
    bool** init_spaces = gen_space_combo(w);
    for(int i=0; i < pow(2,w); i++){
        bool** final_spacetime = run_async(rule, t, w, ranks, init_spaces[i]);
        if(!is_spacetime_conservative(final_spacetime, w, t))
            return false;
    }
    return true;
}

void usage(){
    fprintf(stderr, "Usage: aeca -r ID -w WIDTH -t TIMESTEPS -s <FILE|SCHEME>\n");
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {
    int r = -1, w = -1, t = -1;
    bool check_conservation, single_scheme = true;
    int *ranks;
    for(int opt; (opt = getopt(argc, argv, "r:w:t:s:h")) != -1;){
        switch (opt) {
            case 'r': r = atoi(optarg); break;
            case 'w': w = atoi(optarg); break;
            case 't': t = atoi(optarg); break;
            case 'c': check_conservation = true; break;
            case 's': 
                      ranks = malloc(4*8);
                      if(sscanf(optarg, "(%d,%d,%d,%d,%d,%d,%d,%d)", \
                                  ranks, ranks+1, ranks+2, ranks+3, ranks+4, ranks+5, ranks+6, ranks+7) != 8){
                          ranks = realloc(ranks, 4*8*4683);
                          single_scheme = false;
                          FILE *fp = fopen(optarg, "r");
                          for(int i=0, ch; (ch = fgetc(fp)) != EOF;)
                              if(isdigit(ch))
                                  ranks[i++] = ch - '0';
                          fclose(fp);
                      }
                      break;
            case 'h':
            default:
                      usage();
        }
    }
    if(r == -1 || w == -1 || t == -1 || !ranks)
        usage();
    for(int i=0; i < single_scheme ? 1 : 4683; i++){
        printf("Rule %d is", r);
        if(!is_rule_conservative(r, t, w, ranks+(i*8)))
            printf(" not");
        printf(" conservative for scheme (%d,%d,%d,%d,%d,%d,%d,%d)\n", \
                ranks[0], ranks[1], ranks[2], ranks[3], ranks[4], ranks[5], ranks[6], ranks[7]);
    }
    exit(EXIT_SUCCESS);
}
