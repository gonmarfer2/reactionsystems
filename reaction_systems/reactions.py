class Reaction():
    def __init__(self,reactant,inhibitor,product,name=None) -> None:
        assert isinstance(reactant,set), f'The reactant set must be of type set, {type(reactant)} was introduced.'
        assert isinstance(inhibitor,set), f'The inhibitor set must be of type set, {type(reactant)} was introduced.'
        assert isinstance(product,set), f'The product set must be of type set, {type(reactant)} was introduced.'
        
        self.reactant = reactant
        self.inhibitor = inhibitor
        self.product = product
        if name:
            self.name = str(name)

    def get_full_definition(self):
        return str((self.reactant,self.inhibitor,self.product))

    def __str__(self) -> str:
        return self.get_full_definition()
    
    def __repr__(self) -> str:
        if self.name:
            return str(self.name)
        else:
            return self.get_full_definition()
    
    def __hash__(self) -> int:
        return hash(str(self.reactant)+str(self.inhibitor)+str(self.product))
    
    def __eq__(self, __value: object) -> bool:
        same_reactant = self.reactant == __value.reactant
        same_inhibitor = self.inhibitor == __value.inhibitor
        same_product = self.product == __value.product
        return same_reactant and same_inhibitor and same_product
    
    def get_reactant(self):
        return self.reactant
    
    def get_inhibitor(self):
        return self.inhibitor
    
    def get_product(self):
        return self.product
    
    def set_reactant(self,reactant):
        assert isinstance(reactant,set), f'The reactant set must be of type set, {type(reactant)} was introduced.'
        self.reactant = reactant
    
    def set_inhibitor(self,inhibitor):
        assert isinstance(inhibitor,set), f'The inhibitor set must be of type set, {type(inhibitor)} was introduced.'
        self.inhibitor = inhibitor
    
    def set_product(self,product):
        assert isinstance(product,set), f'The product set must be of type set, {type(product)} was introduced.'
        self.product = product

    def is_enabled_by(self,T):
        return self.reactant.issubset(T) and len(self.inhibitor.intersection(T)) == 0

    def get_result(self,T):
        return self.product if self.is_enabled_by(T) else set()
    
    def get_elements(self):
        elements = set().union(self.get_reactant(),self.get_inhibitor(),self.get_product())
        return elements


class ReactionSet():
    def __init__(self, reactions):
        assert isinstance(reactions,set), f'ReactionSet needs a set of reactions but {type(reactions)} was introduced.'
        for reaction in reactions:
            assert isinstance(reaction,Reaction), f'All the elements of the reaction set must be of Reaction type but {reaction} is of type {type(reaction)}'
        self.reactions = reactions

    def __str__(self) -> str:
        return str(self.reactions)
    
    def get_activity(self,T):
        return set([reaction for reaction in self.reactions if reaction.is_enabled_by(T)])

    def get_result(self,T):
        result = set()
        for reaction in self.reactions:
            result.update(reaction.get_result(T))
        return result
    
    def is_consistent(self):
        union_of_reactants = set()
        union_of_inhibitors = set()
        for reaction in self.reactions:
            union_of_reactants.update(reaction.get_reactant())
            union_of_inhibitors.update(reaction.get_inhibitor())
        return len(union_of_reactants.intersection(union_of_inhibitors)) == 0
    
    def get_elements(self):
        elements = set()
        for reaction in self.reactions:
            elements = elements.union(reaction.get_elements())
        return elements
    
    def get_reactions(self):
        return self.reactions
    
    def union(self,__value):
        assert isinstance(__value,ReactionSet), f'Union can only occur between instances of ReactionSet.'
        return ReactionSet(self.get_reactions().union(__value.get_reactions()))
    
class ReactionSystem():
    def __init__(self,backgroundset,reactionset) -> None:
        assert reactionset.get_elements().issubset(backgroundset), f'All the elements from the reaction set must be present in the background set.'
        self.backgroundset = backgroundset
        self.reactionset = reactionset

    def get_activity(self,T):
        return self.reactionset.get_activity(T)
    
    def is_active(self,T):
        return len(self.get_activity(T)) > 0
    
    def get_elements(self):
        return self.backgroundset
    
    def get_result(self,T):
        return self.reactionset.get_result(T)
    
    def get_background_set(self):
        return self.backgroundset
    
    def get_reaction_set(self):
        return self.reactionset
    
    def __str__(self) -> str:
        return f'(S={self.backgroundset},A={self.reactionset})'
    
    def union(self,__value):
        assert isinstance(__value,ReactionSystem), f'Union can only occur between instances of ReactionSystem.'
        return ReactionSystem(self.get_background_set().union(__value.get_background_set()),
                              self.get_reaction_set().union(__value.get_reaction_set()))
    
    def get_interactive_process(self,context_sequence):
        return InteractiveProcess(self,context_sequence)

    
class InteractiveProcess():
    def __init__(self,reaction_system,context_sequence,result_sequence=[]) -> None:
        assert isinstance(reaction_system,ReactionSystem), f'reaction_system must be of ReactionSystem type but {type(reaction_system)} was found.'
        assert isinstance(context_sequence,list), f'The initial context must be of type list but {type(context_sequence)} was found.'
        assert len(context_sequence) > 0, f'The context sequence must contain at least one set of elements'
        for context in context_sequence:
            assert isinstance(context,set), f'The context sets must be of set type, but {type(context)} was found.'
            assert context.issubset(reaction_system.get_background_set()), f'The context sequence must be a subset of the background set.'

        self.reaction_system = reaction_system
        self.context_sequence = context_sequence
        self.result_sequence = result_sequence

    def generate_process(self,n=1):
        assert n >= 1, f'n must be a number of steps greater or equal than 1.'
        this_context_sequence = [context_set for context_set in self.context_sequence[:n]]
        if len(this_context_sequence) <= n:
            this_context_sequence.extend([set() for i in range(n-len(this_context_sequence)+1)])
        result_sequence = [set()]
        for i in range(n):
            new_result = self.reaction_system.get_result(this_context_sequence[i].union(result_sequence[i]))
            result_sequence.append(new_result)
        return InteractiveProcess(self.reaction_system,this_context_sequence,result_sequence)

    def get_state_sequence(self):
        state_sequence = []
        if len(self.result_sequence) != len(self.context_sequence):
            return state_sequence
        for c,d in zip(self.context_sequence,self.result_sequence):
            state_sequence.append(c.union(d))
        return state_sequence
    
    def get_context_sequence(self):
        return self.context_sequence
    
    def get_result_sequence(self,n=1):
        return self.result_sequence
    
    def extend_process(self,n=1,extra_context_sequence=None):
        assert n >= 1, f'n must be a number of steps greater or equal than 1.'
        this_context_sequence = [context_set for context_set in self.context_sequence]
        context_before_length = len(this_context_sequence)
        if extra_context_sequence:
            this_context_sequence.extend(extra_context_sequence)
            this_context_sequence = this_context_sequence[:context_before_length+n]
        if len(this_context_sequence) <= context_before_length+n:
            this_context_sequence.extend([set() for i in range(context_before_length+n-len(this_context_sequence))])
        result_sequence = [result_set for result_set in self.result_sequence]
        for i in range(context_before_length-1,len(this_context_sequence)-1):
            new_result = self.reaction_system.get_result(this_context_sequence[i].union(result_sequence[i]))
            result_sequence.append(new_result)
        return InteractiveProcess(self.reaction_system,this_context_sequence,result_sequence)

class ExtendedReactionSystem(ReactionSystem):
    def __init__(self, backgroundset, reactionset, binary_relation=lambda x,y: (x != None and y != None)) -> None:
        '''
        binary_relation is a function that compares two states and returns True if both states are related.
        '''
        super().__init__(backgroundset, reactionset)
        assert callable(binary_relation), "binary_relation must be a function that compares two states and returns True if both states are related."
        self.binary_relation = binary_relation

    def __str__(self) -> str:
        return f'(S={self.backgroundset},A={self.reactionset},R={self.binary_relation})'
    
    def union(self,__value):
        assert isinstance(__value,ExtendedReactionSystem), f'Union can only occur between instances of ExtendedReactionSystem.'
        return ExtendedReactionSystem(self.get_background_set().union(__value.get_background_set()),
                              self.get_reaction_set().union(__value.get_reaction_set()),
                              self.binary_relation or __value.binary_relation) # Might not work that well
    
    def get_interactive_process(self,context_sequence):
        return ExtendedInteractiveProcess(self,context_sequence)
    
    def get_periodic_elements(self):    #TODO
        pass

class ExtendedInteractiveProcess(InteractiveProcess):
    def __init__(self, extended_reaction_system, context_sequence, result_sequence=[]) -> None:
        super().__init__(extended_reaction_system, context_sequence, result_sequence)

    def generate_process(self,n=1):
        '''
        Generates a sequence of length n.
        Will yield None if the following state is not related by the binary_relation
        '''
        assert n >= 1, f'n must be a number of steps greater or equal than 1.'
        this_context_sequence = [context_set for context_set in self.context_sequence[:n]]
        if len(this_context_sequence) <= n:
            this_context_sequence.extend([set() for i in range(n-len(this_context_sequence)+1)])
        result_sequence = [set()]
        for i in range(n):
            new_result = self.reaction_system.get_result(this_context_sequence[i].union(result_sequence[i]))
            if self.reaction_system.binary_relation(
                result_sequence[i].union(this_context_sequence[i]),
                new_result.union(this_context_sequence[i+1])):
                result_sequence.append(new_result)
            else:
                return None
        return ExtendedInteractiveProcess(self.reaction_system,this_context_sequence,result_sequence)

    def extend_process(self,n=1,extra_context_sequence=None):
        '''
        Will yield None if the following state is not related by the binary_relation
        '''
        assert n >= 1, f'n must be a number of steps greater or equal than 1.'
        this_context_sequence = [context_set for context_set in self.context_sequence]
        context_before_length = len(this_context_sequence)
        if extra_context_sequence:
            this_context_sequence.extend(extra_context_sequence)
            this_context_sequence = this_context_sequence[:context_before_length+n]
        if len(this_context_sequence) <= context_before_length+n:
            this_context_sequence.extend([set() for i in range(context_before_length+n-len(this_context_sequence))])
        result_sequence = [result_set for result_set in self.result_sequence]
        for i in range(context_before_length-1,len(this_context_sequence)-1):
            new_result = self.reaction_system.get_result(this_context_sequence[i].union(result_sequence[i]))
            if self.reaction_system.binary_relation(
                result_sequence[i].union(this_context_sequence[i]),
                new_result.union(this_context_sequence[i+1])):
                result_sequence.append(new_result)
            else:
                return None
        return InteractiveProcess(self.reaction_system,this_context_sequence,result_sequence)