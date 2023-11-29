from functools import cached_property
from .flow import Flow
from .match import match_rules, format_match_result
from tqdm import tqdm
from typing import Callable

class Flowmap:
    def __init__(self, source_flows: list[Flow], target_flows: list[Flow], rules: list[Callable[..., bool]] = None):
        self.source_flows = source_flows
        self.source_flows_dict = {flow.id:flow for flow in source_flows}
        self.source_flows_count = len(source_flows)
        self.source_flows_unique_count = len(self.source_flows)
        self.target_flows = target_flows
        self.target_flows_dict = {flow.id:flow for flow in target_flows}
        self.target_flows_count = len(target_flows)
        self.target_flows_unique_count = len(self.target_flows)
        self.mappings_count = 0
        self.mapped_source_flows = 0
        self.mappings: list = []
        self.rules = rules if rules else match_rules()
    
    def match(self):
        result = []
        for s in tqdm(self.source_flows):
            for t in self.target_flows:
                for rule in self.rules:
                    is_match = rule(s, t)
                    if is_match:
                        result.append(
                            {'from': s,
                             'to': t,
                             'info': is_match}
                        )
                        break
        self.mappings = result
        self.mappings_count = len(result)
        self.mapped_source_flows = len({link['from'].id for link in result})
        self.statistics()
    
    def statistics(self):
        print(f'{self.source_flows_unique_count} unique source flows...')
        print(f'{self.target_flows_unique_count} unique target flows...')
        print(f'{self.mappings_count} mappings of {self.mapped_source_flows} unique source flows ({self.mapped_source_flows / self.source_flows_unique_count:.2%} of total).')

    def to_randonneur(self):
        result = [
            format_match_result(map_entry['from'], 
                                map_entry['to'],
                                map_entry['info']) 
            for map_entry in self.mappings
        ]
        return result
