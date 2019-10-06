# Jamar Fraction
# CPTS 315
# PA2

import numpy as np
from numpy import linalg

from itertools import combinations

# Global variables. Could be used as config params
IN_FILE = "./data/ratings.csv"
OUT_FILE = "./output.txt"


# Read in the file
def read_input():
    with open(IN_FILE, "r") as text_file:
        all_lines = text_file.readlines()

    return all_lines

def structure_data(input):

    user_ratings = {}

    for line in input[1:]:
        line_as_list = line.split(",")

        #  Assign the indicies of the list
        user = line_as_list[0]
        movie = line_as_list[1]
        rating = line_as_list[2]

        # Push a user key if it doesn't already exist
        if user_ratings.get(user) is None:
            user_ratings[user] = {}

        # Assign the user's rating of the movie
        user_ratings[user][movie] = rating

    return user_ratings

def create_item_profiles(input):
    
    item_profiles = {}

    for line in input[1:]:
        line_as_list = line.split(",")

        movie = line_as_list[1]
        rating = line_as_list[2]

        # Push a user key if it doesn't already exist
        if item_profiles.get(movie) is None:
            item_profiles[movie] = []
        
        item_profiles[movie].append(rating)
    
    return item_profiles

def create_matrix(input):

    highest_user = 0
    highest_movie = 0

    # Determine the number of users and movies
    for line in input[1:]:
        line_as_list = line.split(",")

        user = int(line_as_list[0])
        movie = int(line_as_list[1])

        if user > highest_user:
            highest_user = user
        
        if movie > highest_movie:
            highest_movie = movie
    
    # Create the matrix of size [highest_user, highest_movie] filled with zeros 
    value_matrix = np.zeros((highest_user, highest_movie), dtype=float)

    # Fill the value matrix with user ratings for each movie
    for line in input[1:]:
        line_as_list = line.split(",")

        user = int(line_as_list[0])
        movie = int(line_as_list[1])
        rating = float(line_as_list[2])

        value_matrix[user - 1][movie - 1] = rating

    return value_matrix

def center_matrix(matrix):

    return np.apply_along_axis(center_row, 1, matrix)

def center_row(row):

    mean = row.mean()

    return np.subtract(row, mean)

def compute_similarity_scores(matrix):
    
    similarity_scores = {}

    #TODO: Change back to check full data set
    # combos = combinations([i for i in range(matrix.shape[1])], 2)

    # testing for only the first 50 movies
    combos = combinations([i for i in range(50)], 2)


    for pair in combos:

        vector_1 = matrix[:,pair[0]]
        vector_2 = matrix[:,pair[1]]

        similarity_scores[pair] = np.dot(vector_1, vector_2)/(linalg.norm(vector_1)*linalg.norm(vector_2))
    
    return similarity_scores

    


# file dumping
def dump_output(pairs_results, triples_results):
    with open(OUT_FILE, "w") as text_file:
        
        # Write the pairs + association
        text_file.write("OUTPUT A\n")
        for result in pairs_results:
            text_file.write(f"{result[0][0]} {result[0][1]} {result[1]}\n")
        
        # Write the triples + association
        text_file.write("OUTPUT B\n")
        for result in triples_results:
            text_file.write(f"{result[0][0]} {result[0][1]} {result[0][2]} {result[1]}\n")

    return


def main():

    # Read the input file
    all_lines = read_input()

    value_matrix = create_matrix(all_lines)
    
    centered_matrix = center_matrix(value_matrix)

    similarity_scores = compute_similarity_scores(centered_matrix)

    print("Deez")
    


if __name__ == '__main__':
    main()
