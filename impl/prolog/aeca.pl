#!/usr/bin/swipl -q 

gen_space_time(N, L) :- 
	length(L, N), 
	nth0(M1, L, 1),
	M1 is div(N,2), 
	maplist(between(0,1), L), 
	!.
 
run_sync(0, _) :- !.
run_sync(N, I) :- 
	maplist(writ, I), nl,
	single_step(I, Next),
	succ(N1, N),
	run_sync(N1, Next).
 
r(0,0,0,0). 
r(0,0,1,1). 
r(0,1,0,1). 
r(0,1,1,1). 
r(1,0,0,1). 
r(1,0,1,0). 
r(1,1,0,0). 
r(1,1,1,0).
 
single_step(In, Out) :-
	step1st(In, First),
	Out = [First|_],
	step(In, First, First, Out).
 
step1st([A,B|T], A1) :-                            last([A,B|T], Last), r(Last,A,B,A1).
step([A,B], Prev, First, [Prev, This]) :-          r(A,B,First,This).
step([A,B,C|T], Prev, First, [Prev,This|Rest]) :-  r(A,B,C,This), step([B,C|T], This, First, [This|Rest]).
 
writ(0) :- write(0).
writ(1) :- write(1).

main:-
	tty_size(R,C), R1 is R - 1, gen_space_time(C, S), run_sync(R1, S).
