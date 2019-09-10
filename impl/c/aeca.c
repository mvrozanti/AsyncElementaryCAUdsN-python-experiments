#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h> 
#include<math.h>

const unsigned int W = 10;
const unsigned int T = 10;
const unsigned int R = 110;

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
    int energy = quantize_energy(spacetime[0], w);
    for(int i=1; i < t; i++)
        if(quantize_energy(spacetime[i], w) != energy)
            return false;
    return true;
}

bool** gen_space_combo(int w){
    unsigned int mask = 1U << 7;
    bool** space_combo = malloc(pow(2,w));
    for(int i=0; i < pow(2,w); i++){
        bool* space = malloc(8);
        int z = w;
        for (int j = 0; j < 8; j++) {
            space[j] = (w & mask) ? 1 : 0;
            z <<= 1;
        }
        space_combo[i] = space;
    }
    return space_combo;
}

bool is_rule_conservative(int rule, int t, int w, int* ranks){


}

bool** run_async(int rule, int t, int w, int* ranks, bool* init_space){

}

int main() {
    return 0;
}
