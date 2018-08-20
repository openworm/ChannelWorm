(* ::Package:: *)

BeginPackage["IonChannelFitter`"]
ionChannelParameterFit::usage = "Extract parameters from given patch clamp experiment."
displayResults::usage = "Display simulation results."


Begin["`Private`"]
i[Gmax_, Vh_, k_, Vrev_, V_]:= (Gmax/(1 + Exp[(Vh - V)/k]))*(V- Vrev)


(*
	Helper functions for simulation
*)

generateSolutions[n_] := Reap[
	Do[Sow[{RandomReal[{.01,1}], RandomReal[{.1, .5}], RandomReal[{.01,5}], RandomReal[{10,40}]}], {n}]
	][[2,1]]

Clear[costFunc, calculateNorm];				
costFunc[m1_,m2_] := Norm[Flatten@m1 - Flatten@m2] / Length[m1]

(*
	Recall that dataRange is simply the list of x-coordinates from the
	digitized data.  calculateNorm applies the function i[Gmax_, Vh_, k_, Vrev_, V_]
	do this data by taking a candidate solution and appending to it the value
	of the x-coordinate.
*)

calculateNorm[params_, dataSeries_] := Block[{dataRange, testValues},
					dataRange = dataSeries[[All,1]];
					testValues = i@@Append[params, #]& /@ dataRange;
					costFunc[testValues, series[[All,2]]]
					]

(*
	Adaptive sampling:
	After 200 rounds, choose parameters by sampling a Gaussian distribution
	centered around the values of the best solution of the previous generation.
*)

floorShift[x_Real] := Abs[If[x==0,.01,x]]
randomGaussianDrift = Compile[{{x, _Real}}, RandomVariate[NormalDistribution[x, .05*x]]];

generateParameterSpace[pGen_, dataSeries_] := Module[{bestCandidate},
	bestCandidate = First @ (First @ SortBy[{#, calculateNorm[#, dataSeries]}& /@ pGen, Last]);
	Reap[Do[Sow[randomGaussianDrift[#]& /@ bestCandidate],{100}]][[2,1]]
]

(*
	Displaly progress of simulation	
*)
	
Clear[frameTicks];
frameTicks[min_, max_] := Join[
		Table[{i, Style[i, 12], {.04, 0}}, {i, 0,  Floor[max], Round[.1*max, 5]}], 
		{{$startAS, "\n\nBegin Adaptive Sampling", .1, Directive[Black,Thickness[0.003], Dashed]}}
		]

frame = {{True, False}, {True, False}};

Clear[makeGrid];
makeGrid[round_, normList_, current_] := Module[{simHistPlot},
	simHistPlot = ListPlot[normList, 
			ImageSize -> 400, 
			Frame -> frame, 
			FrameTicks -> {{Automatic, None}, {frameTicks[0, $numRounds], None}}, 
			FrameLabel -> {Style["Number of Generations", Larger], Style["Fitness of Best Solution", Larger]}
		];
		
	Grid[
		{
			{"Current Round: ", round},
			{"Current Best Norm: ", simHistPlot}
		},
		 Alignment -> Left,
		 Spacings -> {2,2}
		]
	]


(*
	Mutation Operators (randomGaussianDrift is defined above in adaptive sampling:
	1) Replace the parameter with a randomly sampled value from the entire parameter space
	2) Replace the parameter with a randomly sampled value from a Gaussian distribution centered
	on the value with a variance of 5% of the value.  From Gurkiewicz and Korngreen.  
*)
Clear[randomMutation, mutate];
randomMutation[x_Real, n_] := Switch[n[[2]],
	1, RandomReal[{.01,1}],
	2, RandomReal[{.1, .5}],
	3, RandomReal[{.01,5}],
	4, RandomReal[{10,40}]
	]

(* 
	Keep track of all of the mutations that accrue.
	trackMutations is initialized when the simulation begins	
*)

trm[] := AppendTo[$trackMutations, "Random Mutation"]
trgd[] := AppendTo[$trackMutations, "Random Gaussian Drift"]
trc[n_] := AppendTo[$trackMutations, "Crossover at "~~ToString[n]]

(* Toss a coin to determine which mutation operator to apply *)
mutate[x_Real, n_] := Module[{},
	bool = RandomReal[] < .01;
	If[bool,
		If[RandomChoice[{True, False}], trm[];randomMutation[x, n], trgd[];randomGaussianDrift[x]],
		x
	]
]

(* Crossover parameters between surviving organisms *)

onePointListSwap[{list1_, list2_, index_}] := Module[{tl1, tl2, ti},
	{tl1, tl2} = {list1, list2};
	ti = tl2[[index]];
	tl2[[index]] = tl1[[index]];
	tl1[[index]] = ti;
	{tl1, tl2}
]

crossover[{org1_, org2_}] := If[
	RandomReal[]<=0.5,
	With[{n=RandomChoice[Range[4]]}, trc[n];onePointListSwap[{org1, org2, n}]],
	{org1, org2}
	]


$runningTally = {};
$numRounds = 0;
$living = {};
$totalSolutions = 0;
$trackMutations = {};
(* When to start adaptive sampling *)
$startAS = 1000;
(* How far back to look to determine termination *)
$tWin = 1000;
$allOrgs = {};
$norms = {};

alert[] := If[$numRounds==($startAS+1), PrintTemporary["Adaptive Sampling . . ."]]

checkThreshold[] := Quiet @ Check[Variance[Take[$runningTally, -$tWin]], \[Infinity]]

Clear[ionChannelParameterFit];
ionChannelParameterFit[dataSeries_] := Block[{roundLength, newParameterSpace, normsAssoc, pair1, pair2, survivor1, survivor2},
	Monitor[
		While[checkThreshold[] > 10^-8,
			$numRounds++;
			(*
				1) Set the parameter space / "organisms" for the current round.
				2) Reset the list $living{} so that the current surviving organisms
				will be added to it.
				3) Calculate all the norms of the current set, sort, and retain the highest
				scoring individual.
				(*	New addition: Adaptive sampling *)  
			*)
			
			newParameterSpace = Which[
					$numRounds == 1, generateSolutions[100],
					2 <= $numRounds <= $startAS, $living,
					$numRounds > $startAS, alert[];generateParameterSpace[$living, dataSeries]
					];
	
			roundLength = Round[Length[newParameterSpace] / 2];
			$living = {};
			$norms = With[{tempNorms = {#, calculateNorm[#, dataSeries]}& /@ newParameterSpace},
				SortBy[tempNorms, Last]
				];
			AppendTo[$living, First[$norms][[1]]];
			AppendTo[$allOrgs, First[$norms][[1]]];
			AppendTo[$runningTally, First[$norms][[2]]];
			normsAssoc = Association[(First[#] -> {False, Last[#]})& /@ $norms];
			
			(* Begin inner loop *)
			For[n=1, n<=roundLength, n++,
				{pair1, pair2} = RandomChoice[Keys[normsAssoc], {2,2}];
				survivor1 = First[SortBy[pair1, First]];
				survivor2 = First[SortBy[pair2, First]];
				$living = Join[$living, crossover[{survivor1, survivor2}]];
			];
			(* End inner loop *)
			
			(* 
				Apply mutation operator to the entire population
			*)
			$living = MapIndexed[mutate, $living, {2}];
			$totalSolutions += Length[$living];

		],
		
	(* Summary grid for current round *)
	finalCandidate = First[$norms][[1]];
	makeGrid[$numRounds, $runningTally, finalCandidate]
	];	
]


(*
Summarize results of simulation
*)
Clear[displayResults];
displayResults[simNorms_] := Block[{iv, p2, finalPlot, simHistPlot},
	iv = Block[{Gmax, Vh, k, Vrev},
		Set@@@Transpose[{{Gmax, Vh, k, Vrev}, First@simNorms[[1]]}];
		(Gmax/(1 + Exp[(Vh - V)/k]))*(V- Vrev)
	];

	p2 = ListPlot[series];

	finalPlot = Show[
		Plot[iv,{V, -40, 80}], p2, 
		PlotLabel -> "I/V Curve for EGL-19 Voltage-Gated Calcium Channel\n", 
		AxesLabel -> {"Membrane Potential (mV)", "Current (pA)"}, ImageSize -> 500
		];
		
	simHistPlot = ListPlot[$runningTally, 
			ImageSize -> 400, 
			Frame -> {{True, False}, {True, False}}, 
			FrameTicks -> {{Automatic, None}, {frameTicks, None}}, 
			FrameLabel -> {Style["Number of Generations", Larger], Style["Fitness of Best Solution", Larger]}
		];	
	
	Grid[{
			{"Number of Rounds: ", $numRounds}, 
			{"Total # of Solutions Explored: ", $totalSolutions}, 
			{"Norm of Top Solution ", First[simNorms][[2]]},
			{"Simulation History: ", simHistPlot},
			{"IV Curve: ", finalPlot},
			{"Parameter Values: ", Grid[Transpose@{{"Gmax", "Vh", "k", "Vrev"}, First@simNorms[[1]]}, Frame->All]}
		},
	Frame -> All,
	Alignment -> Left
	]
]


End[]
EndPackage[]
