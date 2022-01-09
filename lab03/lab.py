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
        actor_dict['actors'].add(selfid)
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
    raise NotImplementedError("Implement me!")


def actors_with_bacon_number(transformed_data, n):
    raise NotImplementedError("Implement me!")


def bacon_path(transformed_data, actor_id):
    raise NotImplementedError("Implement me!")


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == '__main__':
    with open('resources/tiny.pickle', 'rb') as f:
        smalldb = pickle.load(f)
    print(smalldb)
    print(transform_data(smalldb))
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
