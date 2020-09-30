import random


def get_paginated_data(req, all_data, step):
    """
    A function that returns a specific chunk of a query data
    :param req: the request object offered by flask
    :param all_data: the query returned from getting all the data in a database
    :param step: the step of your pagination
    :return: the serialized data in a specific page (the page is in the req object as a params)
    """

    # Getting the page passes as params in the url
    page = req.args.get('page', 1, type=int)
    # Forming the start and the end of data to send
    start = (page - 1) * step
    end = start + step
    # Getting the raw data to send
    items_in_page = all_data[start: end]
    # Serializing the data if it exists
    items_in_page_serialized = None
    if items_in_page:
        items_in_page_serialized = [item.format() for item in items_in_page]
    return items_in_page_serialized


def get_all_categories_map(categories_query):
    """
    A function that returns all the categories available as a map object ex: {id1: type1, id2: type2, ....}
    :param categories_query: the query object from querying all the categories
    :return: a map of the available categories where keys are categories ids and values are categories types
    """
    categories_map = {}
    for category in categories_query:
        categories_map[f'{category.id}'] = category.type
    return categories_map


def get_next_question(previous_questions_ids, questions_in_the_quiz_category):
    """
    A function that returns the next question that is in
     'questions_in_the_quiz_category' and not in 'previous_questions_ids'
    :param previous_questions_ids: a list of previous questions ids
    :param questions_in_the_quiz_category: a query containing all the questions in a given category
    :return: a serialized question in 'questions_in_the_quiz_category and not in 'previous_questions_ids'
    """
    # Shuffling the array to get different question every game
    random.shuffle(questions_in_the_quiz_category)
    # Getting a question from the shuffled array
    for question in questions_in_the_quiz_category:
        if question.id not in previous_questions_ids:
            return question.format()
    # No question was found (all questions in that category has been already displayed)
    return None
