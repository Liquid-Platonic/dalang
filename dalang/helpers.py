import collections
import functools
import operator
from operator import itemgetter
from typing import Dict, List


def get_top_dict_items(dictionary: Dict, n=5) -> Dict:
    """This can be used to take the top n tags from a given tag prediction."""
    return dict(
        sorted(dictionary.items(), key=itemgetter(1), reverse=True)[:n]
    )


def merge_list_of_dicts_by_average(
    dict_list: List[Dict[str, float]]
) -> Dict[str, float]:
    """This can be used to average the scores across multiple tag predictions."""
    if not dict_list:
        return {}
    aggregated_dict_keys = dict(
        functools.reduce(operator.add, map(collections.Counter, dict_list))
    )
    key_occurences = collections.Counter(
        [key for dict_ in dict_list for key in dict_.keys()]
    )

    return {k: v / key_occurences[k] for k, v in aggregated_dict_keys.items()}


def map_dict_keys(dict: Dict, mapping: Dict) -> Dict:
    """This can be used to map different tags to the Cyanite ones given a tag prediction."""
    return {(mapping[k] if k in mapping else k): v for k, v in dict.items()}


def is_result_dict_valid(dict: Dict, threshold: float = 0.6) -> bool:
    """This can be used to check whether we can rely on a tag prediction given a threshold."""
    return any(value > threshold for value in dict.values())


def merge_dicts(dicts: List[Dict]) -> Dict:
    """This can be used to merge multiple dictionaries."""
    merged_dict = {}
    for dict_ in dicts:
        merged_dict.update(dict_)
    return merged_dict


def get_sorted_dict_str(d: Dict) -> str:
    output_str = ""
    for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):
        output_str += f"{k}: {v:.2}\n"

    return output_str
