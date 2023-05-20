# def fire_transition(petri_net, transition):
#     # Update the marking by subtracting tokens from input places and adding tokens to output places
#     for input_place, weight in petri_net['flows'][transition]['input'].items():
#         petri_net['marking'][input_place] -= weight
#     for output_place, weight in petri_net['flows'][transition]['output'].items():
#         petri_net['marking'][output_place] += weight

# def is_transition_enabled(petri_net, transition):
#     # Check if the transition is enabled by comparing the tokens in input places with the required weights
#     for input_place, weight in petri_net['flows'][transition]['input'].items():
#         if petri_net['marking'][input_place] < weight:
#             return False
#     return True

# def print_marking(petri_net):
#     # Print the current marking of places
#     print("Current marking:")
#     for place, tokens in petri_net['marking'].items():
#         print(f"{place}: {tokens}")

# def is_sound(petri_net):
#     # Perform a reachability analysis to check for deadlock
#     reachable_places = set(petri_net['marking'].keys())
#     enabled_transitions = set(petri_net['transitions'])

#     while enabled_transitions:
#         transition = enabled_transitions.pop()
#         for input_place, weight in petri_net['flows'][transition]['input'].items():
#             if petri_net['marking'][input_place] < weight:
#                 return False
#             petri_net['marking'][input_place] -= weight
#         for output_place, weight in petri_net['flows'][transition]['output'].items():
#             petri_net['marking'][output_place] += weight
#             if output_place not in reachable_places:
#                 enabled_transitions.add(output_place)
#                 reachable_places.add(output_place)
#     return True

# # Example usage
# petri_net = {
#     'places': {'P1', 'P2'},
#     'transitions': {'T1', 'T2'},
#     'flows': {
#         'T1': {'input': {'P1': 1}, 'output': {'P2': 1}},
#         'T2': {'input': {'P2': 1}, 'output': {'P1': 1}}
#     },
#     'marking': {'P1': 1, 'P2': 0}
# }

# print_marking(petri_net)
# if is_sound(petri_net):
#     print("The Petri net is sound.")
# else:
#     print("The Petri net is not sound.")

def fire_transition(petri_net, transition):
    # Update the marking by subtracting tokens from input places and adding tokens to output places
    for input_place, weight in petri_net['flows'][transition]['input'].items():
        petri_net['marking'][input_place] -= weight
    for output_place, weight in petri_net['flows'][transition]['output'].items():
        petri_net['marking'][output_place] += weight

def is_transition_enabled(petri_net, transition):
    # Check if the transition is enabled by comparing the tokens in input places with the required weights
    for input_place, weight in petri_net['flows'][transition]['input'].items():
        if petri_net['marking'][input_place] < weight:
            return False
    return True

def print_marking(petri_net):
    # Print the current marking of places
    print("Current marking:")
    for place, tokens in petri_net['marking'].items():
        print(f"{place}: {tokens}")

def is_sound(petri_net):
    # Perform a reachability analysis to check for deadlock
    reachable_places = set(petri_net['marking'].keys())
    enabled_transitions = set(petri_net['transitions'])

    while enabled_transitions:
        transition = enabled_transitions.pop()
        for input_place, weight in petri_net['flows'][transition]['input'].items():
            if petri_net['marking'][input_place] < weight:
                return False
            petri_net['marking'][input_place] -= weight
        for output_place, weight in petri_net['flows'][transition]['output'].items():
            petri_net['marking'][output_place] += weight
            if output_place not in reachable_places:
                enabled_transitions.add(output_place)
                reachable_places.add(output_place)
    return True

# Take Petri net details as dynamic inputs
places = input("Enter the set of places (separated by spaces): ").split()
transitions = input("Enter the set of transitions (separated by spaces): ").split()

flows = {}
for transition in transitions:
    input_places = input(f"Enter the input places for transition '{transition}' (in the format 'place1:weight1 place2:weight2'): ")
    output_places = input(f"Enter the output places for transition '{transition}' (in the format 'place1:weight1 place2:weight2'): ")

    input_dict = {}
    for pair in input_places.split():
        place, weight = pair.split(':')
        input_dict[place] = int(weight)

    output_dict = {}
    for pair in output_places.split():
        place, weight = pair.split(':')
        output_dict[place] = int(weight)

    flows[transition] = {'input': input_dict, 'output': output_dict}

initial_marking = {}
for place in places:
    tokens = int(input(f"Enter the number of tokens for place '{place}': "))
    initial_marking[place] = tokens

petri_net = {
    'places': places,
    'transitions': transitions,
    'flows': flows,
    'marking': initial_marking
}

print_marking(petri_net)
if is_sound(petri_net):
    print("The Petri net is sound.")
else:
    print("The Petri net is not sound.")
