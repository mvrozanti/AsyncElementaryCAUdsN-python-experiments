#!/usr/bin/env node
	
try {
    COLUMNS = process.stdout.columns 
    LINES = process.stdout.rows
}catch(e){
    COLUMNS = 30
    LINES = 30
}

function get_rule_transitions(rule){ 
    rts = (rule >>> 0).toString(2)
    rts = "00000000".substr(rts.length) + rts
    return rts.split('').map(Number)
}

function get_transition_ix(ln,mn,rn){ return 7 - ((ln << 2) + (mn << 1) + rn) } 

function get_neighbors(ci, space){ 
    w = space.length
    return [ci == 0 ? space[w-1] : space[ci-1], 
	space[ci], 
	ci == w - 1 ? space[0] : space[ci+1]] 
}

function gen_mid_space(w){
    space = Array.from({ length: w }).fill(0)
    space[Math.floor(w/2)-1] = 1
    return space
}

function print_spacetime(spacetime, zero, one){
    for(i=0; i < spacetime.length; i++){
	space = spacetime[i]
	for(j=0; j < space.length; j++)
	    process.stdout.write(space[j]+"")
	console.log()
    }
}

function run_syn(rule, t, w){
    space = gen_mid_space(w)
    rule_transitions = get_rule_transitions(rule)
    spacetime = []
    for(timestep=0; timestep < t; timestep++){
	future_space = space.slice()
	for(ci=0; ci < w; ci++){
	    neighbors = get_neighbors(ci, space)	
	    ix_transition = get_transition_ix.apply(null, neighbors)
	    future_space[ci] = rule_transitions[ix_transition]  
	}
	space = future_space.slice()
	spacetime.push(future_space)
    }
    return spacetime
}

function main(){
    var stdio = require('stdio')
    var args = stdio.getopt({
	'rule': {
	    key: 'r', args: 1, 
	    description: 'rule in the Wolfram classification scheme', 
	    default: 30
	    // mandatory:true
	},
	'scheme': { key: 's', args: '*', description: 'async scheme to run (-s 2 1 1 1 1 1 1 1)' },
	'one': { key:'1', args: 1, description: 'replace ones by ARG1' },
	'zero': { key: '0', args: 1, description: 'replace zeroes by ARG1' },
	'width': { key: 'w', args: 1, description: 'space width', default: COLUMNS },
	'timesteps': { key: 't', args: 1, description: 'timesteps to run', default: LINES },
    })
    spacetime = run_syn(args.rule, args.timesteps, args.width)
    // console.log(spacetime)
    print_spacetime(spacetime, '0', '1')
}

if (require.main === module) { main(); }
