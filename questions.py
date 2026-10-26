"""
DSC401-6 Artificial Intelligence  |  Units I & II  |  Question bank (60 questions)

Single source of truth: the Streamlit app (app.py), the Question-Bank document and the
report are all generated from this file, so they can never disagree.

Question schema
---------------
id        : int
topic     : one of TOPICS
type      : one of FORMATS
level     : "Easy" | "Medium" | "Hard"
q         : question text (markdown)
code      : optional text shown in a code block (graphs, boards, tables)
options   : list[str]  (choice questions)
ans       : int index into options (choice) | list[int] (match: right-index for each left item)
accept    : list[str] accepted typed answers (text questions) -- compared after normalising
kind      : "text" | "num"      (typed questions only)
left/right: lists for Match-the-following
hint      : nudge that does not give the answer away
exp       : explanation shown as immediate feedback
follow    : (question, answer) -- the kind of follow-up the teacher may ask in the viva
real      : True if it is a real-world application / scenario question
search    : True if it is a search / state-space problem
"""

TOPICS = [
    "Foundations & Applications of AI",
    "Turing Test",
    "Agents & Rationality",
    "Nature of Environments",
    "Problems, Production Systems & Search Design",
    "Uninformed Search (BFS / DFS / IDS)",
    "Hill Climbing & Local Search",
    "Heuristic & Best-First Search",
    "Constraint Satisfaction (CSP)",
    "Means-End Analysis",
]
T1, T2, T3, T4, T5, T6, T7, T8, T9, T10 = TOPICS

TOPIC_SHORT = {T1: "Foundations", T2: "Turing Test", T3: "Agents", T4: "Environments",
               T5: "Problems & Prod. Systems", T6: "BFS / DFS / IDS", T7: "Hill Climbing",
               T8: "Heuristic Search", T9: "CSP", T10: "Means-End Analysis"}

FORMATS = ["MCQ", "True/False", "Assertion-Reason", "Fill in the Blank",
           "Match the Following", "Scenario", "Problem Solving"]

AR_OPTS = [
    "Both A and R are true, and R is the correct explanation of A",
    "Both A and R are true, but R is NOT the correct explanation of A",
    "A is true, but R is false",
    "A is false, but R is true",
]
TF_OPTS = ["True", "False"]

LEVEL_POINTS = {"Easy": 1, "Medium": 2, "Hard": 3}

G1_TREE = """\
        A
       / \\
      B   C
     / \\   \\
    D   E   F
        |
        G"""

QUESTIONS = [
    # ===================================================================== MCQ (15)
    dict(id=1, topic=T1, type="MCQ", level="Easy",
         q="A student builds a chatbot and judges it by whether human evaluators can tell its replies "
           "from a real person's. Which of the four classic approaches to AI is she following?",
         options=["Thinking humanly", "Thinking rationally", "Acting humanly", "Acting rationally"],
         ans=2,
         hint="She is judging external behaviour, and the yardstick is a human, not ideal logic.",
         exp="Judging a system by whether its behaviour is indistinguishable from a human's is the "
             "**acting humanly** approach (the Turing-Test approach). *Thinking humanly* would need a model of "
             "how the human mind works internally; *thinking rationally* uses laws of logic; *acting rationally* "
             "aims at the best action, not human-likeness.",
         follow=("How does 'acting rationally' differ from 'acting humanly'?",
                 "Acting rationally maximises expected performance given what the agent knows; it need not imitate "
                 "humans. This rational-agent view is the one this course follows.")),

    dict(id=2, topic=T1, type="MCQ", level="Medium",
         q="Which discipline gave AI the formal theory of utility and decision-making under uncertainty "
           "that rational agents use to choose between actions?",
         options=["Linguistics", "Neuroscience", "Economics", "Computer engineering"],
         ans=2,
         hint="Think of 'utility', 'preferences' and 'decision theory'.",
         exp="**Economics** formalised utility, decision theory and game theory. Linguistics contributed language "
             "structure, neuroscience the study of the brain, and computer engineering the hardware.",
         follow=("Name two other foundations of AI and what each contributed.",
                 "Philosophy: logic and reasoning; Mathematics: logic, probability, computation; Psychology: models of "
                 "human cognition; Control theory: feedback-based optimisation.")),

    dict(id=3, topic=T2, type="MCQ", level="Easy",
         q="In Turing's imitation game, why is the interrogator separated from the human and the machine and "
           "allowed to communicate only through a text terminal?",
         options=["To make the test finish faster",
                  "So that judgement is not influenced by physical appearance or voice, and only conversational "
                  "intelligence is tested",
                  "Because computers cannot yet produce speech",
                  "To stop the human from helping the machine"],
         ans=1,
         hint="What would a judge be biased by if they could see or hear the candidates?",
         exp="The screen/terminal removes physical cues so the test measures **intelligent behaviour in language**, "
             "not looks or voice.",
         follow=("Who proposed the test, and in which paper?",
                 "Alan Turing, 1950, 'Computing Machinery and Intelligence'.")),

    dict(id=4, topic=T2, type="MCQ", level="Medium",
         q="Which capability is required for the *Total* Turing Test but NOT for the standard Turing Test?",
         options=["Natural language processing", "Knowledge representation",
                  "Computer vision and robotics", "Machine learning"],
         ans=2,
         hint="The 'total' version adds a physical dimension: seeing and manipulating objects.",
         exp="The standard test needs **NLP, knowledge representation, automated reasoning and machine learning**. "
             "The Total Turing Test adds a video signal and physical objects, so it also needs "
             "**computer vision and robotics**.",
         follow=("List the four capabilities needed for the standard test.",
                 "Natural language processing, knowledge representation, automated reasoning, machine learning.")),

    dict(id=5, topic=T3, type="MCQ", level="Easy",
         q="Which statement best describes a *rational* agent?",
         options=["It always picks the action that turns out best, whatever it knew beforehand",
                  "It picks the action expected to maximise its performance measure, given its percepts "
                  "and built-in knowledge",
                  "It imitates human behaviour as closely as possible",
                  "It never makes a mistake"],
         ans=1,
         hint="Rationality is judged on what the agent knew, not on lucky outcomes.",
         exp="A rational agent maximises **expected** performance given the percept sequence and its knowledge. "
             "That is different from omniscience (knowing actual outcomes) or perfection.",
         follow=("Is a rational agent always successful?",
                 "No. Rationality maximises expected, not actual, performance; the agent can still be unlucky or "
                 "lack information.")),

    dict(id=6, topic=T3, type="MCQ", level="Medium",
         q="What is the minimum upgrade that lets a simple reflex agent cope with a *partially observable* "
           "environment?",
         options=["Maintaining an internal state / model of how the world evolves",
                  "Adding a utility function", "Adding a learning element", "Using a faster processor"],
         ans=0,
         hint="The agent must remember what it can no longer see.",
         exp="A **model-based reflex agent** keeps internal state (a model of how the world changes and how its own "
             "actions affect it) to track the unobserved parts. Utility and learning add other abilities but "
             "are not needed for partial observability.",
         follow=("Give an example where a simple reflex agent fails.",
                 "A car braking decision from a single camera frame cannot tell whether the car ahead is slowing "
                 "unless it remembers earlier frames.")),

    dict(id=7, topic=T4, type="MCQ", level="Easy",
         q="Which task is most naturally *episodic*?",
         options=["Playing a full game of chess", "Driving a taxi through a city",
                  "Inspecting items on a conveyor belt and tagging each defective one",
                  "Playing many hands of poker for money"],
         ans=2,
         hint="In an episodic task, today's decision does not affect tomorrow's.",
         exp="Each item is judged independently of earlier items, so the task is **episodic**. Chess, driving and "
             "poker are **sequential**: current decisions affect future ones.",
         follow=("Why is episodic easier for an agent?",
                 "The agent need not think ahead, because the current action does not affect later episodes.")),

    dict(id=8, topic=T5, type="MCQ", level="Easy",
         q="Which of the following is NOT part of the formal definition of a search problem?",
         options=["Initial state", "Actions (successor function)", "Goal test and path cost",
                  "A heuristic function h(n)"],
         ans=3,
         hint="Which item is extra knowledge used only by informed search?",
         exp="A problem is defined by the **initial state, actions/transition model, goal test and path cost**. "
             "A heuristic h(n) is additional knowledge that informed search uses to guide the search.",
         follow=("Formulate the 8-puzzle as a search problem.",
                 "State: tile positions; Initial: any configuration; Actions: slide blank up/down/left/right; "
                 "Goal: tiles in order; Path cost: 1 per move.")),

    dict(id=9, topic=T5, type="MCQ", level="Easy",
         q="In a production system, which component decides which rule to fire when several rules' conditions "
           "match the current state?",
         options=["The global database", "The set of production rules", "The control strategy",
                  "The goal test"],
         ans=2,
         hint="Rules say WHAT can be done; something else says WHICH to do.",
         exp="The **control strategy** chooses among applicable rules (conflict resolution) and decides when to stop. "
             "A good control strategy must cause motion and be systematic.",
         follow=("Name the three main parts of a production system.",
                 "A set of condition-action rules, a global database (working memory) and a control strategy.")),

    dict(id=10, topic=T5, type="MCQ", level="Medium",
         q="A planner can start from many different states but has only one goal state. Going backward from the "
           "goal has about 3 choices per state; going forward has about 30. Which direction should it search, and why?",
         options=["Forward, because there are many starting states",
                  "Backward from the goal, because the branching factor in that direction is far smaller",
                  "Forward, because 30 choices give more chances to find the goal",
                  "Direction never matters"],
         ans=1,
         hint="Compare the branching factors: smaller means a smaller tree.",
         exp="Search in the direction with the **smaller branching factor**; with one goal and many starts, "
             "**backward** search is also natural. Direction of search is one of the key design issues of "
             "search programs.",
         follow=("Name the four design issues of search programs.",
                 "Direction of search (forward/backward), selecting applicable rules (matching), representing nodes, "
                 "and tree versus graph (detecting repeated states).")),

    dict(id=11, topic=T6, type="MCQ", level="Easy",
         q="Which search algorithm needs memory only linear in the depth, O(b·m), making it attractive "
           "for huge state spaces?",
         options=["Breadth-first search", "Depth-first search", "Uniform-cost search", "Bidirectional search"],
         ans=1,
         hint="It only stores the current path and the unexplored siblings along it.",
         exp="**DFS** stores one path plus unexpanded siblings, so O(bm) memory. BFS keeps a whole level "
             "(O(b^d)).",
         follow=("Then why not always use DFS?",
                 "It is not complete in infinite or cyclic spaces and not optimal: it may find a deep, costly "
                 "goal first.")),

    dict(id=12, topic=T10, type="MCQ", level="Medium",
         q="Which description best fits *means-end analysis* (MEA)?",
         options=["Always expand the shallowest unexpanded node",
                  "Compare the current and goal states, pick the most important difference, choose an operator "
                  "that reduces it, and treat unmet preconditions as sub-goals",
                  "Accept worse moves with a probability that falls over time",
                  "Choose the variable with the fewest legal values"],
         ans=1,
         hint="The word 'difference' is the key.",
         exp="MEA (used in the **General Problem Solver**) repeatedly **reduces the difference** between current and "
             "goal state. When the chosen operator cannot yet be applied, its unmet preconditions become sub-goals. "
             "Option A is BFS, C is simulated annealing, D is the MRV heuristic.",
         follow=("How is MEA different from forward chaining?",
                 "Forward search only applies operators that are applicable now; MEA chooses by relevance to the "
                 "goal difference and can set up sub-goals to make an operator applicable.")),

    dict(id=13, topic=T7, type="MCQ", level="Medium",
         q="Which hill-climbing variant generates successors at random, one at a time, and moves to the first one "
           "that is better than the current state?",
         options=["Steepest-ascent hill climbing", "Stochastic hill climbing",
                  "First-choice hill climbing", "Random-restart hill climbing"],
         ans=2,
         hint="Its name tells you it takes the first improvement it finds.",
         exp="**First-choice** hill climbing is useful when a state has thousands of successors. Steepest-ascent "
             "examines all successors, stochastic picks randomly among uphill moves, random-restart repeats from "
             "new starts.",
         follow=("Which variant is complete (with probability 1)?",
                 "Random-restart hill climbing: a good start state will eventually be generated.")),

    dict(id=14, topic=T8, type="MCQ", level="Medium",
         q="Which of the following is an *admissible* heuristic for the sliding-tile (8-puzzle) problem?",
         options=["Sum of the Manhattan distances of all tiles from their goal positions",
                  "Twice the sum of Manhattan distances",
                  "Number of moves already made",
                  "Number of tiles that are already in the correct position"],
         ans=0,
         hint="Each move can shift one tile by only one square.",
         exp="Every move reduces the Manhattan distance of one tile by at most 1, so the sum never overestimates: "
             "**admissible**. Doubling may overestimate; moves made is g(n), not an estimate of the remaining cost; "
             "the count of correctly placed tiles gets *larger* as we approach the goal (wrong direction).",
         follow=("Which dominates, misplaced tiles or Manhattan distance?",
                 "Manhattan distance: h2(n) >= h1(n) for all n, so A* with h2 expands fewer nodes.")),

    dict(id=15, topic=T9, type="MCQ", level="Easy",
         q="Colouring a map of Indian states so that neighbouring states have different colours is a CSP. "
           "Which formulation is correct?",
         options=["Variables = states; domain = set of colours; constraint = neighbouring states get different colours",
                  "Variables = colours; domain = states; constraint = every colour used once",
                  "Variables = borders; domain = states; constraint = none",
                  "Variables = states; domain = borders; constraint = same colour for neighbours"],
         ans=0,
         hint="Variables are the things you assign values to.",
         exp="A CSP has **variables** (states), a **domain** of values for each (colours) and **constraints** "
             "(adjacent states must differ).",
         follow=("What is a consistent and a complete assignment?",
                 "Consistent: violates no constraint. Complete: every variable has a value. A solution is both.")),

    # ===================================================================== TRUE / FALSE (8)
    dict(id=16, topic=T2, type="True/False", level="Easy",
         q="A machine can pass the standard Turing Test only if it has a human-like physical body.",
         options=TF_OPTS, ans=1,
         hint="Recall why a text terminal was used.",
         exp="**False.** The standard test is conducted over text, so no body is needed. Only the *Total* Turing "
             "Test adds perception and physical manipulation.",
         follow=("Name one famous criticism of the Turing Test.",
                 "Searle's Chinese Room: symbol manipulation can look intelligent without understanding.")),

    dict(id=17, topic=T3, type="True/False", level="Medium",
         q="The agent function and the agent program are the same thing.",
         options=TF_OPTS, ans=1,
         hint="One is a mathematical description, the other is code running on a machine.",
         exp="**False.** The *agent function* is an abstract mapping from percept sequences to actions. The *agent "
             "program* is the concrete implementation that runs on the architecture and implements that function.",
         follow=("Why can't we just store the agent function as a table?",
                 "The table grows exponentially with the length of the percept sequence; compact programs "
                 "(rules, search, learning) are needed.")),

    dict(id=18, topic=T6, type="True/False", level="Medium",
         q="Breadth-first search always returns the cheapest (least-cost) path in a weighted graph.",
         options=TF_OPTS, ans=1,
         hint="BFS counts edges, not costs.",
         exp="**False.** BFS finds the path with the **fewest edges**, which is optimal only when all step costs "
             "are equal. For varying costs use uniform-cost search or A*.",
         follow=("Which algorithm fixes this?",
                 "Uniform-cost search: expand the node with the lowest path cost g(n).")),

    dict(id=19, topic=T6, type="True/False", level="Hard",
         q="Depth-first search with an explored set (graph search) is complete in a finite state space that "
           "contains cycles, whereas plain tree-search DFS can loop forever there.",
         options=TF_OPTS, ans=0,
         hint="What does the explored set prevent?",
         exp="**True.** Remembering explored states stops the search from circling in a cycle, and a finite space "
             "can then be exhausted. Without it DFS may repeat states forever.",
         follow=("What is the price of the explored set?",
                 "Extra memory: DFS loses its O(bm) space advantage.")),

    dict(id=20, topic=T5, type="True/False", level="Medium",
         q="In a monotonic production system, applying one rule never prevents the later application of another "
           "rule that was applicable at the time.",
         options=TF_OPTS, ans=0,
         hint="Monotonic means the set of facts only grows.",
         exp="**True.** That is the definition of a monotonic production system; theorem proving is an example. "
             "Chess is non-monotonic: a move can make other moves impossible.",
         follow=("Why do monotonic systems need less backtracking?",
                 "Because an applied rule never closes off other rules, so earlier steps can be ignored.")),

    dict(id=21, topic=T7, type="True/False", level="Easy",
         q="Simulated annealing sometimes accepts a move that makes the current state worse.",
         options=TF_OPTS, ans=0,
         hint="That is how it escapes local maxima.",
         exp="**True.** A bad move is accepted with probability e^(ΔE/T); the 'temperature' T decreases over time, "
             "so bad moves become rarer.",
         follow=("What happens as T → 0?",
                 "It behaves like ordinary hill climbing, since worse moves are practically never accepted.")),

    dict(id=22, topic=T9, type="True/False", level="Medium",
         q="In a constraint satisfaction problem, a constraint can involve only two variables at a time.",
         options=TF_OPTS, ans=1,
         hint="Think of the Alldiff constraint in Sudoku.",
         exp="**False.** Constraints may be unary, binary or involve many variables (global constraints, e.g. "
             "Alldiff over a Sudoku row).",
         follow=("Give an example of a unary constraint.",
                 "'Tamil Nadu ≠ green' restricts a single variable's domain.")),

    dict(id=23, topic=T5, type="True/False", level="Hard",
         q="Every arrangement of the eight tiles and the blank in the 8-puzzle can be reached from every other "
           "arrangement by sliding tiles.",
         options=TF_OPTS, ans=1,
         hint="Count reachable states: is it 9! or something smaller?",
         exp="**False.** Parity of inversions is invariant, so only half of the 9! = 362,880 arrangements "
             "(**181,440**) are reachable from a given state.",
         follow=("Why does this matter for search?",
                 "Before searching, check solvability; otherwise the search explores all 181,440 states and fails.")),

    # ===================================================================== ASSERTION–REASON (7)
    dict(id=24, topic=T3, type="Assertion-Reason", level="Medium",
         q="**Assertion (A):** A rational agent can make a mistake.\n\n"
           "**Reason (R):** Rationality requires the agent to know the actual outcome of every action in advance.",
         options=AR_OPTS, ans=2,
         hint="Does rationality demand omniscience?",
         exp="A is true: with incomplete information a rational agent can choose an action that turns out badly. "
             "R is false: rationality maximises *expected* performance; knowing outcomes in advance is omniscience.",
         follow=("Give a real example.",
                 "Crossing a road after looking both ways and still being hit by a speeding car: rational, not omniscient.")),

    dict(id=25, topic=T6, type="Assertion-Reason", level="Medium",
         q="**Assertion (A):** Depth-first search may fail to find a solution even though one exists, if the state "
           "space is infinite.\n\n"
           "**Reason (R):** DFS can keep descending along one infinitely long branch.",
         options=AR_OPTS, ans=0,
         hint="What happens if a branch never ends?",
         exp="Both true, and R explains A: DFS can get lost on an infinite branch and never backtrack to the "
             "branch containing the goal, so it is **incomplete**. Depth-limited search or IDS fixes this.",
         follow=("Name two fixes.",
                 "Depth-limited search with a cutoff, or iterative deepening.")),

    dict(id=26, topic=T8, type="Assertion-Reason", level="Hard",
         q="**Assertion (A):** A* tree search with an admissible heuristic returns an optimal solution.\n\n"
           "**Reason (R):** An admissible heuristic never overestimates the true cost to the goal, so no "
           "cheaper path can stay hidden behind a larger f-value.",
         options=AR_OPTS, ans=0,
         hint="Think about what would go wrong if h overestimated.",
         exp="Both true and R is the explanation. (For *graph* search A* also needs a **consistent** heuristic.)",
         follow=("State the consistency condition.",
                 "h(n) <= c(n, n') + h(n') for every successor n' of n; consistent implies admissible.")),

    dict(id=27, topic=T7, type="Assertion-Reason", level="Hard",
         q="**Assertion (A):** Hill climbing needs very little memory.\n\n"
           "**Reason (R):** Hill climbing is not guaranteed to find the global optimum.",
         options=AR_OPTS, ans=1,
         hint="Does incompleteness explain low memory use?",
         exp="Both true, but R does not explain A. Memory is small because hill climbing keeps only the **current "
             "state** (no search tree or frontier). Incompleteness is a separate property caused by local maxima, "
             "plateaus and ridges.",
         follow=("What is its space complexity?",
                 "O(1) beyond the current state and its neighbours.")),

    dict(id=28, topic=T8, type="Assertion-Reason", level="Medium",
         q="**Assertion (A):** Greedy best-first search always finds the cheapest path.\n\n"
           "**Reason (R):** Greedy best-first search always expands the node with the smallest h(n).",
         options=AR_OPTS, ans=3,
         hint="Is the cost already paid, g(n), part of its choice?",
         exp="A is false: greedy ignores g(n), so it can pick a path that looks close to the goal but is costly "
             "(it is neither optimal nor complete in general). R is a true description of the algorithm.",
         follow=("Which algorithm repairs this?",
                 "A*, with f(n) = g(n) + h(n).")),

    dict(id=29, topic=T4, type="Assertion-Reason", level="Hard",
         q="**Assertion (A):** Chess played with a clock is a *static* environment.\n\n"
           "**Reason (R):** In a static environment the world does not change while the agent is deliberating.",
         options=AR_OPTS, ans=3,
         hint="Does the passage of time change anything in chess with a clock?",
         exp="A is false: the environment itself does not change, but the agent's **score** does as the clock runs, "
             "so it is **semi-dynamic**. R is the correct definition of static.",
         follow=("Give a static and a dynamic example.",
                 "Static: crossword puzzle. Dynamic: taxi driving.")),

    dict(id=30, topic=T6, type="Assertion-Reason", level="Hard",
         q="**Assertion (A):** Iterative deepening has the same asymptotic time complexity, O(b^d), as "
           "breadth-first search even though it regenerates upper-level nodes.\n\n"
           "**Reason (R):** In a tree with branching factor b > 1, most nodes lie at the deepest level, so the "
           "repeated work on upper levels is small.",
         options=AR_OPTS, ans=0,
         hint="Where do most nodes of a bushy tree live?",
         exp="Both true and R explains A. For b = 10, d = 5: IDS generates 123,450 nodes versus 111,110 for "
             "BFS, only about **11% overhead**.",
         follow=("What do you gain for that overhead?",
                 "BFS's completeness and optimality (unit costs) with DFS-like O(bd) memory.")),

    # ===================================================================== FILL IN THE BLANK (7)
    dict(id=31, topic=T3, type="Fill in the Blank", level="Easy",
         q="For an automated taxi, the goals 'safe, fast, legal, comfortable trip, maximise profit' belong to the "
           "PEAS component called the ________.",
         accept=["performance measure", "performance measures", "performance"], kind="text",
         hint="P in PEAS.",
         exp="**Performance measure.** PEAS = Performance measure, Environment, Actuators, Sensors.",
         follow=("Give the E, A and S of the taxi.",
                 "E: roads, traffic, pedestrians; A: steering, accelerator, brake, horn; "
                 "S: cameras, GPS, speedometer, lidar.")),

    dict(id=32, topic=T8, type="Fill in the Blank", level="Easy",
         q="A heuristic h(n) that never overestimates the true cost from n to the goal is called an "
           "________ heuristic.",
         accept=["admissible", "admissible heuristic"], kind="text",
         hint="Starts with 'ad'. It is the property A* needs for optimality.",
         exp="**Admissible.** Example: straight-line distance in route finding.",
         follow=("Is every admissible heuristic consistent?",
                 "No. Every consistent heuristic is admissible, but not the other way round.")),

    dict(id=33, topic=T7, type="Fill in the Blank", level="Medium",
         q="To escape local maxima, ________ hill climbing runs a series of searches from randomly generated "
           "initial states.",
         accept=["random restart", "random-restart", "random restart hill climbing"], kind="text",
         hint="Two words: 'random ...'.",
         exp="**Random-restart** hill climbing. If each run succeeds with probability p, about 1/p restarts are "
             "needed.",
         follow=("For 8-queens steepest-ascent succeeds about 14% of the time. Expected runs?",
                 "About 1/0.14 ≈ 7 runs.")),

    dict(id=34, topic=T10, type="Fill in the Blank", level="Medium",
         q="Means-end analysis was introduced by Newell and Simon in a program called the ________ "
           "(three words or its abbreviation).",
         accept=["gps", "general problem solver"], kind="text",
         hint="Initials G-P-S.",
         exp="**General Problem Solver (GPS).**",
         follow=("What does GPS do first when given a problem?",
                 "It finds the difference between the current and goal states and picks an operator relevant to that difference.")),

    dict(id=35, topic=T9, type="Fill in the Blank", level="Medium",
         q="The CSP heuristic that picks next the variable with the fewest legal values left in its domain is "
           "called the ________ heuristic (name or abbreviation).",
         accept=["mrv", "minimum remaining values", "minimum remaining value", "most constrained variable"],
         kind="text",
         hint="Abbreviation MRV.",
         exp="**Minimum Remaining Values (MRV)**, also called the *most constrained variable* or *fail-first* "
             "heuristic.",
         follow=("What is the companion heuristic for choosing values?",
                 "Least-constraining value: pick the value that rules out the fewest choices for neighbours.")),

    dict(id=36, topic=T5, type="Fill in the Blank", level="Medium",
         q="Rich & Knight classify problems by whether steps can be undone: theorem-proving steps are ignorable, "
           "8-puzzle moves are ________, and chess moves are irrecoverable.",
         accept=["recoverable"], kind="text",
         hint="You can slide a tile back.",
         exp="**Recoverable**: a mistaken move can be undone by backtracking, at some cost. A chess move cannot be "
             "taken back (irrecoverable).",
         follow=("Which of the three needs the simplest control structure?",
                 "Ignorable: a step can be ignored if it did not help, so no backtracking is needed.")),

    dict(id=37, topic=T8, type="Fill in the Blank", level="Easy",
         q="In A* search the evaluation function is f(n) = g(n) + ________.",
         accept=["h(n)", "h", "heuristic", "heuristic function"], kind="text",
         hint="g is the cost so far; what is the other term?",
         exp="**h(n)**, the estimated cost from n to the goal. g(n) is the cost already paid to reach n.",
         follow=("What do you get if you drop g(n)? If you drop h(n)?",
                 "Drop g: greedy best-first search. Drop h: uniform-cost search.")),

    # ===================================================================== MATCH THE FOLLOWING (5)
    dict(id=38, topic=T4, type="Match the Following", level="Medium",
         q="Match each task with the environment description that fits it best.",
         left=["Poker", "Crossword puzzle", "Taxi driving", "Conveyor-belt defect inspection"],
         right=["Fully observable, deterministic, static, single-agent",
                "Partially observable (hidden cards), static, discrete, multi-agent",
                "Dynamic and continuous: the world changes while you decide",
                "Episodic: each decision is independent of earlier ones",
                "Semi-dynamic: the score depends on elapsed time"],
         ans=[1, 0, 2, 3],
         hint="Start with the one that has hidden information.",
         exp="Poker -> hidden cards, multi-agent. Crossword -> fully observable, deterministic, static. Taxi -> "
             "dynamic, continuous. Inspection -> episodic. The 'semi-dynamic' option describes chess with a clock.",
         follow=("Classify chess with a clock.",
                 "Fully observable, deterministic, sequential, semi-dynamic, discrete, multi-agent.")),

    dict(id=39, topic=T6, type="Match the Following", level="Medium",
         q="Match each search algorithm with its frontier / ordering rule.",
         left=["Breadth-first search", "Depth-first search", "Greedy best-first search", "A* search"],
         right=["FIFO queue", "LIFO stack (or recursion)", "Priority queue ordered by h(n)",
                "Priority queue ordered by g(n) + h(n)", "Priority queue ordered by g(n) only"],
         ans=[0, 1, 2, 3],
         hint="Only one option is left over: it is the ordering of uniform-cost search.",
         exp="BFS = FIFO queue; DFS = LIFO stack; Greedy = lowest h; A* = lowest g + h. "
             "Ordering by g(n) alone is uniform-cost search.",
         follow=("What changes if you swap the queue for a stack in BFS?",
                 "You get DFS.")),

    dict(id=40, topic=T7, type="Match the Following", level="Medium",
         q="Match each hill-climbing difficulty or remedy with its description.",
         left=["Local maximum", "Plateau", "Ridge", "Sideways move"],
         right=["A flat area where all neighbours have equal value",
                "A state better than all its neighbours but worse than the best state overall",
                "A sequence of local maxima that single-step moves cannot follow",
                "Moving to an equal-valued neighbour (with a limit) to cross a flat area",
                "Accepting a worse move with a probability that decreases over time"],
         ans=[1, 0, 2, 3],
         hint="The last option describes a different algorithm altogether (simulated annealing).",
         exp="Local maximum -> better than neighbours only; Plateau -> flat; Ridge -> chain of local maxima; "
             "Sideways move -> allow equal moves. The unused option is simulated annealing.",
         follow=("How do you handle a ridge?",
                 "Use moves in several directions at once, or random restarts / simulated annealing.")),

    dict(id=41, topic=T3, type="Match the Following", level="Easy",
         q="Match each agent type with the example that best illustrates it.",
         left=["Simple reflex agent", "Model-based reflex agent", "Goal-based agent", "Utility-based agent",
               "Learning agent"],
         right=["An automatic door that opens when its sensor sees a person",
                "A robot vacuum that remembers which rooms it has already cleaned",
                "A navigation app that finds a route to the destination you chose",
                "A ride-hailing dispatcher trading off fare, waiting time and driver distance",
                "A spam filter that improves from 'report spam' clicks"],
         ans=[0, 1, 2, 3, 4],
         hint="Ask: does it use only the current percept, remember, pursue a goal, weigh trade-offs, or improve?",
         exp="Simple reflex uses condition-action rules on the current percept; model-based keeps state; goal-based "
             "searches for action sequences reaching a goal; utility-based weighs trade-offs; a learning agent "
             "improves with experience.",
         follow=("What is the difference between goal-based and utility-based?",
                 "Goals give a yes/no distinction; utility gives a degree of 'happiness', so it can choose among "
                 "several ways to reach the goal.")),

    dict(id=42, topic=T5, type="Match the Following", level="Hard",
         q="Match each problem characteristic with the example that illustrates it.",
         left=["Ignorable steps", "Recoverable steps", "Irrecoverable steps", "Best-path (not any-path) solution"],
         right=["Proving a theorem: a useless step can simply be ignored",
                "Solving the 8-puzzle: a move can be undone by a reverse move",
                "Playing chess: a move cannot be taken back",
                "Travelling salesperson: only the shortest tour is acceptable",
                "Understanding a sentence: any reasonable interpretation will do"],
         ans=[0, 1, 2, 3],
         hint="The last option is an 'any-path' problem.",
         exp="These are Rich & Knight's problem characteristics. Understanding a sentence is the "
             "**any-path** example, which is why it is left over.",
         follow=("Which of Rich & Knight's characteristics is 'is the universe predictable?' about?",
                 "Certain-outcome (8-puzzle) versus uncertain-outcome (card games, robot navigation) problems.")),

    # ===================================================================== SCENARIO / APPLICATION (10)
    dict(id=43, topic=T3, type="Scenario", level="Medium", real=True,
         q="A robot vacuum is rewarded one point for every unit of dirt it sucks up. Engineers notice it cleans a "
           "spot, dumps the dirt back on the floor, and cleans it again. What does this show, and how should it "
           "be fixed?",
         options=["The sensors are faulty; replace them",
                  "The performance measure was badly designed; reward the state of the environment instead "
                  "(for example +1 per clean square per time step)",
                  "The agent is irrational and needs more memory",
                  "The environment is stochastic, so nothing can be done"],
         ans=1,
         hint="The agent is doing exactly what it was rewarded for.",
         exp="Design the performance measure according to **what you want in the environment**, not how you think "
             "the agent should behave. Rewarding dirt collected can be gamed; rewarding clean squares cannot.",
         follow=("What is this problem called in general?",
                 "A mis-specified objective (reward hacking / specification gaming).")),

    dict(id=44, topic=T1, type="Scenario", level="Easy", real=True,
         q="Which of the following is the LEAST likely to be called an AI application?",
         options=["A voice assistant that understands spoken requests",
                  "A spam filter that learns from users' reports",
                  "A payroll program that multiplies hours worked by a fixed hourly rate",
                  "A game agent that plans its moves using search"],
         ans=2,
         hint="Which one involves no perception, learning, reasoning or search?",
         exp="The payroll program applies a fixed formula. The others involve perception/language, learning or "
             "search, typical AI techniques.",
         follow=("Name two real-world AI applications and the technique behind them.",
                 "Chess/Go engines (search + learning); medical image diagnosis (machine learning); "
                 "route planners (A* search).")),

    dict(id=45, topic=T2, type="Scenario", level="Hard", real=True,
         q="A customer-support chatbot convinces 40% of judges in 5-minute text chats that it is human, yet it "
           "only matches patterns and has no real understanding of language. Which classical argument says that "
           "passing such a test still does not show genuine understanding?",
         options=["The Church–Turing thesis", "Searle's Chinese Room argument", "The halting problem",
                  "Moore's law"],
         ans=1,
         hint="A person in a room follows rules to shuffle Chinese symbols without understanding Chinese.",
         exp="**Searle's Chinese Room** argues that manipulating symbols by rule (syntax) is not the same as "
             "understanding (semantics), so behaviour alone is not enough.",
         follow=("What reply do AI researchers give?",
                 "The 'systems reply': the whole system (person + rules + room) may understand even if the part does not.")),

    dict(id=46, topic=T3, type="Scenario", level="Hard", real=True,
         q="An e-mail spam filter improves whenever users click 'Report spam'. In the learning-agent architecture, "
           "that click is mainly feedback to which component?",
         options=["The performance element", "The critic", "The learning element", "The problem generator"],
         ans=1,
         hint="Which component tells the learner how well the agent is doing?",
         exp="The **critic** compares behaviour with the performance standard and tells the **learning element** how "
             "well the agent is doing. The performance element chooses the actions (classify as spam or not); the "
             "problem generator suggests exploratory actions.",
         follow=("Which component suggests trying something new?",
                 "The problem generator, e.g. occasionally letting a borderline mail through to learn from the reaction.")),

    dict(id=47, topic=T8, type="Scenario", level="Medium", real=True,
         q="A navigation app runs A* with the straight-line distance to the destination as h(n). Why is this "
           "heuristic admissible?",
         options=["Because the road network is always a straight line",
                  "Because no road route can be shorter than the straight line, so h never overestimates",
                  "Because A* only works with straight lines",
                  "Because it equals g(n)"],
         ans=1,
         hint="Compare any real road with the straight line between its ends.",
         exp="The shortest possible path between two points is the straight line, so the true road distance is "
             "always >= h(n). It is also consistent (triangle inequality).",
         follow=("What would happen if the app used 1.5 × straight-line distance?",
                 "It could overestimate, so A* might return a non-optimal route (faster but not guaranteed shortest).")),

    dict(id=48, topic=T9, type="Scenario", level="Medium", real=True,
         q="A college must schedule 6 exams into 3 time slots so that no student has two exams at the same time. "
           "How is this modelled as a CSP?",
         options=["Variables = time slots; domain = exams; constraint = at most one exam per slot",
                  "Variables = exams; domain = {slot 1, slot 2, slot 3}; constraint = two exams that share a "
                  "student must get different slots",
                  "Variables = students; domain = exams; constraint = none",
                  "It cannot be modelled as a CSP"],
         ans=1,
         hint="What are you assigning, and to what?",
         exp="Assign a **slot (value)** to each **exam (variable)**; the **binary constraint** is that exams sharing "
             "a student must differ. This is graph colouring.",
         follow=("Which graph problem is this equivalent to?",
                 "Graph colouring: exams are nodes, shared students are edges, slots are colours.")),

    dict(id=49, topic=T10, type="Scenario", level="Hard", real=True,
         q="A warehouse robot in Room A holds a box that must reach Room B. Means-end analysis finds the "
           "difference 'location: A vs B' and selects the operator Carry(A→B), whose precondition 'door is open' "
           "is false. What does MEA do next?",
         options=["Discards the operator and picks one at random",
                  "Sets 'door open' as a new sub-goal, applies an operator (OpenDoor) that removes that "
                  "difference, then resumes Carry",
                  "Restarts from the initial state with a different goal",
                  "Declares that no solution exists"],
         ans=1,
         hint="Unmet preconditions are handled recursively.",
         exp="MEA turns an unmet precondition into a **sub-goal** and recursively applies the same difference-"
             "reduction process; once the door is open, Carry can be applied.",
         follow=("What if two differences exist?",
                 "MEA picks the most important one first, using a difference-ordering table.")),

    dict(id=50, topic=T7, type="Scenario", level="Easy", real=True,
         q="A courier improves a delivery route by repeatedly swapping two stops whenever the swap shortens the "
           "route. It stops when no single swap helps, but a much shorter route exists. What has happened?",
         options=["It reached the global optimum",
                  "It is trapped in a local optimum, a classic hill-climbing limitation; random restarts or "
                  "simulated annealing can help",
                  "The heuristic was not admissible",
                  "BFS failed to expand enough nodes"],
         ans=1,
         hint="No neighbouring route is better, but a better route exists somewhere else.",
         exp="No single swap improves the route, so the state is a **local optimum**. Random restarts or "
             "simulated annealing can escape.",
         follow=("What are the 'neighbours' in this problem?",
                 "All routes obtainable from the current one by swapping two stops (2-swap neighbourhood).")),

    dict(id=51, topic=T5, type="Scenario", level="Medium", real=True,
         q="A medical expert system has two rules.\n\n"
           "R1: IF fever AND cough THEN suspect flu.\n"
           "R2: IF fever AND cough AND loss-of-smell THEN suspect COVID-19.\n\n"
           "A patient has all three symptoms, so both rules match. Which production-system mechanism selects "
           "R2 if the system prefers the more specific rule?",
         options=["Conflict resolution by the control strategy", "The goal test", "Backtracking",
                  "Heuristic admissibility"],
         ans=0,
         hint="Several rules are applicable at once.",
         exp="Choosing among several applicable rules is **conflict resolution**, part of the control strategy. "
             "Preferring the most specific rule is a common strategy.",
         follow=("Name two other conflict-resolution strategies.",
                 "Most recently added fact first; first rule in the list; highest priority/certainty.")),

    dict(id=52, topic=T6, type="Scenario", level="Hard", real=True,
         q="A mobile game's character must find the nearest exit in a huge maze. All steps cost the same, the "
           "depth of the nearest exit is unknown, and the phone has very little memory. Which strategy is the "
           "best fit?",
         options=["Breadth-first search", "Depth-first search", "Iterative-deepening depth-first search",
                  "Greedy best-first search"],
         ans=2,
         hint="You want BFS's guarantee with DFS's memory.",
         exp="**IDS** finds the shallowest exit (optimal for equal costs), is complete, and needs only O(bd) "
             "memory. BFS needs O(b^d) memory; DFS may find a far-away exit or loop; greedy is not optimal.",
         follow=("If you also had a good heuristic, what would you use?",
                 "IDA*: iterative deepening on f = g + h.")),

    # ===================================================================== PROBLEM SOLVING (8)
    dict(id=53, topic=T6, type="Problem Solving", level="Medium", search=True,
         q="Breadth-first search starts at A and visits children left to right. Type the order in which the "
           "nodes are visited (letters only; spaces or arrows are fine).",
         code=G1_TREE, accept=["abcdefg"], kind="text",
         hint="Visit level by level.",
         exp="Level 0: A. Level 1: B, C. Level 2: D, E, F. Level 3: G. So **A B C D E F G**. "
             "Queue trace: [A] → [B,C] → [C,D,E] → [D,E,F] → [E,F] → [F,G] → [G].",
         follow=("How many nodes does BFS visit before G? And DFS?",
                 "BFS: 6 before G (G is the 7th). DFS (A B D E G): 4 before G (G is the 5th).")),

    dict(id=54, topic=T6, type="Problem Solving", level="Hard", search=True,
         q="Depth-first search with an explored set starts at S and stops when G is visited. Neighbours are taken "
           "in alphabetical order. Type the order in which nodes are visited.",
         code="Edges (undirected):  S–A, S–B, A–C, B–D, C–D, D–G\n\n"
              "S ─ A ─ C\n│       │\nB ───── D ─ G",
         accept=["sacdbg"], kind="text",
         hint="From D, B comes before C and G alphabetically.",
         exp="S → A → C → D → (neighbours of D in order: B, C, G) B is unvisited so visit **B**; B has no new "
             "neighbour, so backtrack to D; C is already visited; then **G**. Order: **S A C D B G**. "
             "(BFS would give S A B C D G.)",
         follow=("What if there were no explored set?",
                 "DFS might revisit nodes and loop around the cycle S–A–C–D–B–S.")),

    dict(id=55, topic=T6, type="Problem Solving", level="Hard", search=True,
         q="Run iterative-deepening DFS from A looking for G in the tree below (depth limits 0, 1, 2, 3, … and "
           "children left to right). Count a node every time it is visited, repeats included, and stop the "
           "moment G is visited. How many visits in total?",
         code=G1_TREE, accept=["15"], kind="num",
         hint="Count visits for each limit separately and add them up.",
         exp="Limit 0: A = 1.  Limit 1: A, B, C = 3.  Limit 2: A, B, D, E, C, F = 6.  Limit 3: A, B, D, E, G = 5 "
             "(stops at G).  Total = 1 + 3 + 6 + 5 = **15**.",
         follow=("Compare with plain DFS and BFS on the same tree.",
                 "DFS visits 5 nodes, BFS 7; IDS 15, but with O(bd) memory and a guarantee of the shallowest goal.")),

    dict(id=56, topic=T7, type="Problem Solving", level="Medium", search=True,
         q="Steepest-ascent hill climbing starts at index 1 of the landscape below (higher value = better). "
           "At each step it moves to the better neighbour (left or right) and stops when neither neighbour is "
           "better. Where does it stop?",
         code="index: 0  1  2  3  4  5  6  7  8\nvalue: 2  4  6  5  3  7  9  8  1",
         options=["Index 2 (value 6), a local maximum", "Index 6 (value 9), the global maximum",
                  "Index 1 (value 4); it never moves", "Index 4 (value 3), a plateau"],
         ans=0,
         hint="From index 1 compare the values at indices 0 and 2.",
         exp="Index 1 (4) → index 2 (6) since 6 > 2. At index 2 the neighbours are 4 and 5, both lower, so it stops "
             "at a **local maximum**, missing the global maximum 9 at index 6.",
         follow=("Start at index 4 instead. Where does it end?",
                 "4 → 5 (7) → 6 (9): the global maximum. The result depends on the start state, which is why "
                 "random restart helps.")),

    dict(id=57, topic=T8, type="Problem Solving", level="Hard", search=True,
         q="Run greedy best-first search (f = h) and A* (f = g + h) from S to G on the graph below. "
           "How much MORE expensive is the path found by greedy search than the optimal path found by A*? "
           "(Enter a number.)",
         code="Edge costs:  S→A 2,  S→B 3,  A→G 9,  B→C 2,  C→G 3\n"
              "Heuristic h:  S=4,  A=2,  B=4,  C=3,  G=0",
         accept=["3"], kind="num",
         hint="Greedy follows the smallest h; A* adds the cost so far.",
         exp="Greedy: S→A (h=2) → G: path S-A-G, cost 2 + 9 = **11**. A* expands S, A (f=4), B (f=7), C (f=8), "
             "then G via C (f=8) beating G via A (f=11): path S-B-C-G, cost **8**. Difference = 11 − 8 = **3**. "
             "(h is admissible and consistent.)",
         follow=("Give A*'s order of expansion.",
                 "S, A, B, C, G (5 expansions); greedy expands only S, A, G.")),

    dict(id=58, topic=T5, type="Problem Solving", level="Hard", search=True,
         q="You have a 4-litre jug and a 3-litre jug and unlimited water. Allowed operations: fill a jug, empty a "
           "jug, or pour one jug into the other until the target is full or the source is empty. What is the "
           "minimum number of operations needed to get exactly 2 litres in the 4-litre jug?",
         code="State = (x, y) where x = litres in the 4 L jug, y = litres in the 3 L jug.\nStart (0,0).  "
              "Goal: x = 2.",
         accept=["6"], kind="num",
         hint="Run BFS over the (x, y) states.",
         exp="One shortest path: (0,0) → (0,3) → (3,0) → (3,3) → (4,2) → (0,2) → **(2,0)**: 6 operations. "
             "Another is (0,0) → (4,0) → (1,3) → (1,0) → (0,1) → (4,1) → (2,3). BFS confirms nothing shorter "
             "exists (the answer is 4 if '2 L in either jug' were the goal).",
         follow=("How big is this state space?",
                 "At most 5 × 4 = 20 states (x = 0..4, y = 0..3).")),

    dict(id=59, topic=T9, type="Problem Solving", level="Hard", search=True,
         q="Four regions A, B, C, D are to be coloured with 3 colours. A, B and C are mutually adjacent; D is "
           "adjacent only to C. How many valid colourings exist?",
         code="A ── B\n \\  /\n  C ── D", accept=["12"], kind="num",
         hint="Colour the triangle first, then D.",
         exp="Triangle A, B, C needs 3 different colours: 3 × 2 × 1 = 6 ways. D must differ from C only: 2 choices. "
             "Total 6 × 2 = **12**.",
         follow=("How many colours does the triangle need at minimum?",
                 "3 (chromatic number of a triangle). With 2 colours there would be 0 solutions.")),

    dict(id=60, topic=T8, type="Problem Solving", level="Medium", search=True,
         q="For the 8-puzzle board below, let h1 = number of misplaced tiles (blank excluded) and "
           "h2 = sum of Manhattan distances. Type h1 and h2 separated by a comma.",
         code=" 1 2 3        Goal:  1 2 3\n 4 _ 8               4 5 6\n 7 6 5               7 8 _",
         accept=["36", "h13h26", "3and6"], kind="text",
         hint="Only tiles 8, 6 and 5 are out of place.",
         exp="Tiles 8, 6 and 5 are misplaced → **h1 = 3**. Each is 2 squares from its goal square "
             "(8: (1,2)→(2,1); 6: (2,1)→(1,2); 5: (2,2)→(1,1)) → **h2 = 6**. Both are admissible, and the true "
             "optimal solution needs 6 moves.",
         follow=("Which heuristic would make A* expand fewer nodes?",
                 "h2, because it dominates h1 (h2 >= h1) while remaining admissible.")),
]

# ----------------------------------------------------------------------- helpers
import re


def norm(s: str) -> str:
    """Lower-case and keep letters/digits only (so 'A -> B', 'a,b' and 'AB' compare equal)."""
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def check_text(q: dict, user: str) -> bool:
    if q["kind"] == "num":
        m = re.findall(r"-?\d+(?:\.\d+)?", str(user))
        if len(m) != 1:
            return False
        return any(abs(float(m[0]) - float(a)) < 1e-9 for a in q["accept"])
    return norm(user) in {norm(a) for a in q["accept"]}


def input_mode(q: dict) -> str:
    if q["type"] == "Match the Following":
        return "match"
    return "choice" if "options" in q else "text"


SHOW = {31: "performance measure", 32: "admissible", 33: "random-restart", 34: "General Problem Solver (GPS)",
        35: "Minimum Remaining Values (MRV)", 36: "recoverable", 37: "h(n)", 53: "A B C D E F G",
        54: "S A C D B G", 55: "15", 57: "3", 58: "6", 59: "12", 60: "h1 = 3, h2 = 6"}


def correct_text(q: dict) -> str:
    """Human-readable correct answer."""
    m = input_mode(q)
    if m == "choice":
        return q["options"][q["ans"]]
    if m == "match":
        return "; ".join(f"{l} \u2192 {q['right'][r]}" for l, r in zip(q["left"], q["ans"]))
    return SHOW.get(q["id"], q["accept"][0])


def time_limit(q: dict) -> int:
    base = {"Easy": 30, "Medium": 45, "Hard": 60}[q["level"]]
    extra = {"Problem Solving": 60, "Match the Following": 30, "Scenario": 20,
             "Assertion-Reason": 20, "Fill in the Blank": 0, "MCQ": 0, "True/False": -10}[q["type"]]
    return max(20, base + extra)


if __name__ == "__main__":
    from collections import Counter
    print("total", len(QUESTIONS))
    print(Counter(q["type"] for q in QUESTIONS))
    print(Counter(q["level"] for q in QUESTIONS))
    for t in TOPICS:
        print(f"{sum(q['topic']==t for q in QUESTIONS):2d}  {t}")
    print("real-world:", sum(bool(q.get("real")) for q in QUESTIONS),
          "| search:", sum(bool(q.get("search")) for q in QUESTIONS))
