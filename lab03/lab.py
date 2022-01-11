#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).  See the following page for more
# information: https://py.mit.edu/fall21/notes/style


def transform_data(raw_data):
    """
    Given a list of tubles (id1, id2, movid), returns a dictionary
    where the key is the actor id and the value is another dictionary
    of the form: { 'actors': set of all idx, 'actor-movie': set of all
    tuples (idx, movid), 'movies': set of all movid}, where idx acted 
    with actor id on movie movid. 
    """
    def create_actor_dict():
        return {
            'actors': set(),
            'actor-movie': set(),
            'movies': set()
        }

    def add_data(actor_dict, selfid, other_actor_id, movid):
        if selfid == other_actor_id:
            return
        actor_dict['actors'].add(other_actor_id)
        actor_dict['actor-movie'].add((other_actor_id, movid))
        actor_dict['movies'].add(movid)

    transformed_data = {}
    for id1, id2, movid in raw_data:
        if not transformed_data.get(id1):
            transformed_data[id1] = create_actor_dict()
        if not transformed_data.get(id2):
            transformed_data[id2] = create_actor_dict()
        add_data(transformed_data[id1], id1, id2, movid)
        add_data(transformed_data[id2], id2, id1, movid)
    return transformed_data


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Given the transformed data, and two actor ids, return True if
    both actors acted together. False otherwise.
    """
    if actor_id_1 == actor_id_2:
        return True
    actor_dict = transformed_data.get(actor_id_1)
    if actor_dict:
        return actor_id_2 in (transformed_data.get(actor_id_1, set())['actors'])
    return False


def actors_with_bacon_number(transformed_data, n):
    """
    Given a transformed data object, and an integer n, returns the
    set of actors with Bacon number n.
    """
    actors = {4724}
    # Start with Kevin Bacon as the only node
    nodes = {4724}
    previous = {4724}
    while n:
        actors = set()
        if not nodes:
            break
        for node in nodes:
            for actor in transformed_data[node]["actors"]:
                if not actor in previous:
                    actors.add(actor)
                    previous.add(actor)
        n -= 1
        # Set of actors becomes new set of nodes
        nodes = actors
    return actors


def bacon_path(transformed_data, actor_id):
    """
    Given a transformed data structure and an actor id, returns the
    shortest path between Kevin Bacon (4724) and actor_id as a list
    of actor ids between them (including Kevin Bacon id and actor_id).
    """
    return actor_to_actor_path(transformed_data, 4724, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Given a transformed data structure, and two actor ids, returns 
    the shortest path, as a list, from the first actor to the second.
    """
    path_list = [[actor_id_1]]
    path_index = 0
    previous_nodes = {actor_id_1}
    if actor_id_1 == actor_id_2:
        return path_list[0]
    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = transformed_data[last_node]["actors"]
        if actor_id_2 in next_nodes:
            current_path.append(actor_id_2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        path_index += 1
    # No path is found
    return None


def movie_path(transformed_data, actor1, actor2):
    """
    Given a transformed data structure, and two actor ids, returns a 
    list of movie ids that connect the first actor to the second.
    """
    actor_path = actor_to_actor_path(transformed_data, actor1, actor2)
    print(actor_path)
    movie_ids = []
    for actor1, actor2 in zip(actor_path[:-1], actor_path[1:]):
        _, movie_id = next(filter(
            lambda actor_movie: actor_movie[0] == actor2, transformed_data[actor1]["actor-movie"]))
        movie_ids.append(movie_id)
    return movie_ids


def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == '__main__':
    import os
    current_dir = os.path.dirname(__file__)
    filename = os.path.join(current_dir, 'resources', 'large.pickle')
    with open(filename, 'rb') as f:
        db = pickle.load(f)
    # print(db)
    transformed_data = transform_data(db)
    # actors_with_bacon_number(transformed_data, 2)
    print(movie_path(transformed_data, 4724, 1204))
    # Actor to actor path question
    # filename = os.path.join(current_dir, 'resources', 'large.pickle')
    # with open(filename, 'rb') as f:
    #     db = pickle.load(f)
    # with open('resources/names.pickle', 'rb') as f:
    #     names = pickle.load(f)
    # codes = {}
    # for key, value in names.items():
    #     codes[value] = key
    # transformed_data = transform_data(db)
    # path = actor_to_actor_path(
    #     transformed_data, names["Nancy Alexander"], names["John Aquino"])
    # print([codes[actor] for actor in path])
    #['Nancy Alexander', 'Michael Weaver', 'Wes Deitrick', 'David DeCoteau', 'Karen Russell', 'Barry Levinson', 'John Aquino']
    # Acted together questions
    # with open('resources/names.pickle', 'rb') as f:
    #    names = pickle.load(f)
    # actor1 = names["James Caan"]
    # actor2 = names["David Stevens"]
    # print(acted_together(transformed_data, actor1, actor2))
    # actor1 = names["Natascha McElhone"]
    # actor2 = names["Rose Byrne"]
    # print(acted_together(transformed_data, actor1, actor2))
    # Bacon Number question
    # current_dir = os.path.dirname(__file__)
    #filename = os.path.join(current_dir, 'resources', 'large.pickle')
    # with open(filename, 'rb') as f:
    #    db = pickle.load(f)
    # with open('resources/names.pickle', 'rb') as f:
    #     names = pickle.load(f)
    # codes = {}
    # for key, value in names.items():
    #     codes[value] = key
    # transformed_data = transform_data(db)
    # actor_ids = actors_with_bacon_number(transformed_data, 6)
    # print(actor_ids)  # {1367972, 1345461, 1345462, 1338716}
    # actor_names = [codes[actor_id] for actor_id in actor_ids]
    # print(actor_names)
    # ['Vjeran Tin Turk', 'Anton Radacic', 'Iva Ilakovac', 'Sven Batinic']
    """ with open('resources/names.pickle', 'rb') as f:
        codes: dict = pickle.load(f)
    codes['Jose Antonio Donato'] # 1223511
    names = {}
    for key, value in codes.items():
        names[value] = key
    names[31705] # Sam Edwards """

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
