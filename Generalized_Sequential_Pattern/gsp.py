import os
import collections
import ast
from rich import print
from utils import *
os.system('cls')


class GSP:
    def __init__(self, database, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {}
        self.database = database
        self.rules = None

    def generate_size_1_candidates(self):
        frequency = {}

        for transaction in self.database:
            prev_found = ""
            for element in transaction:
                for event in element:
                    if event in prev_found:
                        continue

                    if event not in frequency:
                        frequency[event] = 1
                    else:
                        frequency[event] += 1

                    prev_found += event

        return frequency

    def get_frequency(self, candidates):
        for candidate in candidates:
            for transaction in self.database:
                if self.is_subsequence(ast.literal_eval(candidate), transaction):
                    candidates[candidate] += 1

        return candidates

    def generate_size_2_candidates(self, frequent_1):
        candidates = {}

        for i in range(len(frequent_1)):
            event_1 = list(frequent_1.keys())[i]
            candidates.update({str([event_1, event_1]): 0})

            for j in range(i + 1, len(frequent_1)):
                event_2 = list(frequent_1.keys())[j]
                candidates.update({str([event_1, event_2]): 0})
                candidates.update({str([event_2, event_1]): 0})
                candidates.update({str([event_1 + event_2]): 0})

        for candidate in candidates:
            for transaction in self.database:
                if self.is_subsequence(ast.literal_eval(candidate), transaction):
                    candidates[candidate] += 1

        return candidates

    # This function is poetically beautiful
    def generate_size_k_candidates(self, frequent_prev):
        candidates = {}

        for i in range(len(frequent_prev)):
            for j in range(len(frequent_prev)):
                # same if we remove the first from the first and
                # the last from the second

                item_1 = ast.literal_eval(list(frequent_prev.keys())[i])
                item_2 = ast.literal_eval(list(frequent_prev.keys())[j])
                item_1_remained = None
                item_1_last = None
                item_2_remained = None
                item_2_last = None

                if item_1 == item_2:
                    continue

                if len(item_1[0]) == 1:
                    item_1_remained = list(item_1[1:])
                else:
                    item_1_remained = list(item_1[0][1:]) + list(item_1[1:])
                item_1_last = list(item_1[-1])

                # whether the removed event was part of an element or an element itself
                removed_event_was_joined = False
                if len(item_2[-1]) == 1:
                    item_2_remained = list(item_2[:-1])
                    item_2_last = list(item_2[-1])
                else:
                    item_2_remained = item_2[:-1] + \
                        list(item_2[-1][:-1])
                    item_2_last = item_2[-1][-1]
                    removed_event_was_joined = True

                if item_1_remained == item_2_remained:
                    new_candidate = None
                    if removed_event_was_joined:
                        item_1_last[0] += item_2_last[0]
                        new_candidate = \
                            list(item_1[:-1]) + item_1_last
                    else:
                        new_candidate = \
                            item_1 + item_2_last

                    candidates.update({str(new_candidate): 0})

        return self.get_frequency(candidates)

    def prune(self, candidates):
        return collections.OrderedDict(sorted({
            k: v for k, v in candidates.items() if v >= self.min_support}.items()))

    def is_subsequence(self, subsequence, sequence):
        for i in range(len(subsequence)):
            subsequence_found = False
            for j in range(len(sequence)):
                if substr(subsequence[i], sequence[j]):
                    if len(sequence) > 1:
                        sequence = sequence[j + 1:]
                    else:
                        sequence = []

                    subsequence_found = True
                    break

            if not subsequence_found:
                return False

        return True

    def fit(self):
        candidates_1 = self.generate_size_1_candidates()
        frequent_1 = self.prune(candidates_1)
        self.frequent_itemsets.update(frequent_1)

        if (len(frequent_1) == 0):
            return

        candidates_2 = self.generate_size_2_candidates(frequent_1)
        frequent_2 = self.prune(candidates_2)
        self.frequent_itemsets.update(frequent_2)

        if (len(frequent_2) == 0):
            return

        candidates_k = self.generate_size_k_candidates(frequent_2)
        frequent_k = self.prune(candidates_k)
        self.frequent_itemsets.update(frequent_k)

        while len(frequent_k) != 0:
            candidates_k = self.generate_size_k_candidates(frequent_k)
            frequent_k = self.prune(candidates_k)
            self.frequent_itemsets.update(frequent_k)


# print(model.is_subsequence(["2", "36", "8"], ["24", "356", "8", ]))
# print(model.is_subsequence(["2", "8"], ["24", "356", "8", ]))
# print(model.is_subsequence(["1", "2"], ["12", "34"]))
# print(model.is_subsequence(["2", "4"], ["24", "24", "25"]))

database = [["bd", "c", "b"],
            ["bf", "ce", "b"],
            ["ag", "b"],
            ["be", "ce"],
            ["a", "bd", "b", "c", "b"]]

model = GSP(database, min_support=2, min_confidence=0.5)
model.fit()

print(model.frequent_itemsets)
