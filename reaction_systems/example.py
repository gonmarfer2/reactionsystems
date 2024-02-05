import reactions

if __name__ == '__main__':
    S = set([1,2,3,4,5])
    A = reactions.ReactionSet(set([
        reactions.Reaction(set([1]),set([2]),set([2]),'a1'),
        reactions.Reaction(set([2]),set([1]),set([1]),'a2'),
        reactions.Reaction(set([3]),set([4]),set([3]),'a3'),
        reactions.Reaction(set([4]),set([3]),set([4]),'a4'),
    ]))
    R = lambda x,y : ((1 in x) == (2 in y and (1 not in y)) and ((2 in x) == (1 in y and (2 not in y))))

    ers = reactions.ExtendedReactionSystem(S,A,R)
    ip = ers.get_interactive_process([set([1])]).generate_process(10)
    if ip:
        print(ip.get_state_sequence())

    C1 = [set([1,3])]
    C1process = ers.get_interactive_process(C1).generate_process(3)
    if C1process:
        print('C1: ' + str(C1process.get_state_sequence()))

    C2 = [set([1,3]),set([1])]
    C2process = ers.get_interactive_process(C2).generate_process(3)
    if C2process:
        print('C2: ' + str(C2process.get_state_sequence()))

    C3 = [set([1,3]),set([4]),set(),set([4]),set()]
    C3process = ers.get_interactive_process(C3).generate_process(4)
    if C3process:
        print('C3: ' + str(C3process.get_state_sequence()))

    C4 = [set([1,3]),set([1,4]),set([1,3]),set([1,4]),set()]
    C4process = ers.get_interactive_process(C4).generate_process(4)
    if C4process:
        print('C4: ' + str(C4process.get_state_sequence()))

    C5 = [set([1,3]),set([1,4]),set(),set([1,2,3,4]),set()]
    C5process = ers.get_interactive_process(C5).generate_process(4)
    if C5process:
        print('C5: ' + str(C5process.get_state_sequence()))

    C6 = [set([3]),set(),set([4]),set([4]),set()]
    C6process = ers.get_interactive_process(C6).generate_process(4)
    if C6process:
        print('C6: ' + str(C6process.get_state_sequence()))