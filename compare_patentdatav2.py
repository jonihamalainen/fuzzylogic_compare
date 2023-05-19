import pandas as pd
import re
from rapidfuzz import process, fuzz

lista1 = ["Kissa", "Koira", "Kani"]

lista2 = ["Kissaa", "Koria", "Kuni"]

def fuzzymatcher(list1, list2, score):
    checked = 0
    matched_rows = []
    total = len(list1)
    for list1item in list1:
        matches = process.extract(list1item, list2, scorer=fuzz.ratio, limit=10, score_cutoff=score)
        for match in matches:
            space_index = match[0].find(" ")
            list2item_string_parts = match[0].split(" ", 1)
            list1item_string_parts = list1item.split(" ", 1)
            if space_index != -1 and len(list1item_string_parts) > 1:
                first_score = fuzz.ratio(list1item_string_parts[0], list2item_string_parts[0])
                second_score = fuzz.ratio(list1item_string_parts[1], list2item_string_parts[1])
                if (len(list2item_string_parts[0]) <= 3 or len(
                        list1item_string_parts[0]) <= 3) and first_score == 100 and second_score >= score:
                    matched_rows.append({'list1item': list1item, 'list2item': match[0], 'Score': match[1]})
                elif (3 < len(list2item_string_parts[0]) <= 6 or 3 < len(
                        list1item_string_parts[0]) <= 6) and first_score >= score and second_score >= score:
                    matched_rows.append({'list1item': list1item, 'list2item': match[0], 'Score': match[1]})
                elif (len(list2item_string_parts[0]) > 6 or len(
                        list1item_string_parts[0]) > 6) and first_score >= score and second_score >= score:
                    matched_rows.append({'list1item': list1item, 'list2item': match[0], 'Score': match[1]})
                else:
                    continue
            elif len(match[0]) <= 3 and match[1] == 100:
                matched_rows.append({'list1item': list1item, 'list2item': match[0], 'Score': match[1]})
            else:
                matched_rows.append({'list1item': list1item, 'list2item': match[0], 'Score': match[1]})

        checked += 1
        if checked % 1000 == 0:
            percentage_completed = checked / total * 100
            print(f"{checked} list1 objects have been checked. {percentage_completed:.2f}% completed.")

    matched_df = pd.DataFrame(matched_rows)
    return matched_df


compared_data = fuzzymatcher(lista1, lista2, 90)

with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(compared_data)
