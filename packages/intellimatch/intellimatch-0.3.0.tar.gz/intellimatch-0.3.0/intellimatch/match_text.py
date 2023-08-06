import re
from itertools import product
from difflib import SequenceMatcher


def compare_pattern_similarity(pattern1, pattern2):
	return SequenceMatcher(None, pattern1, pattern2).ratio()


def get_closest_match(item_to_match, challengers):
    leader = None
    leading_score = 0
    for challenger in challengers:
        similarity_score = compare_pattern_similarity(item_to_match, challenger)
        if similarity_score > leading_score:
            leader = challenger
            leading_score = similarity_score
    return leader
