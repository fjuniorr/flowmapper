from functools import cached_property
from .flow import Flow
from .match import match_rules, format_match_result, get_conversion_factor
from tqdm import tqdm
from typing import Callable
import pandas as pd
from collections import Counter

class Flowmap:
    def __init__(self, source_flows: list[Flow], target_flows: list[Flow], rules: list[Callable[..., bool]] = None, disable_progress: bool = False):
        self.disable_progress = disable_progress
        self.source_flows = source_flows
        self.target_flows = target_flows
        self.rules = rules if rules else match_rules()
    
    @cached_property
    def mappings(self):
        result = []
        for s in tqdm(self.source_flows, disable=self.disable_progress):
            for t in self.target_flows:
                for rule in self.rules:
                    is_match = rule(s, t)
                    if is_match:
                        result.append(
                            {'from': s,
                             'to': t,
                             'conversion_factor': get_conversion_factor(s, t),
                             'info': is_match}
                        )
                        break
        return result

    @cached_property
    def matched_source_flows_ids(self):
        return {map_entry['from'].id for map_entry in self.mappings}

    @cached_property
    def matched_target_flows_ids(self):
        return {map_entry['to'].id for map_entry in self.mappings}

    @cached_property
    def matched_source(self):
        result = [
            flow
            for flow in self.source_flows 
            if flow.id in self.matched_source_flows_ids
        ]
        return result

    @cached_property
    def unmatched_source(self):
        result = [
            flow 
            for flow in self.source_flows 
            if flow.id not in self.matched_source_flows_ids
        ]
        return result

    @cached_property
    def matched_source_statistics(self):
        matched = Counter([flow.context.full for flow in self.matched_source])
        matched = pd.Series(matched).reset_index()
        matched.columns = ['context', 'matched']

        total = Counter([flow.context.full for flow in self.source_flows])
        total = pd.Series(total).reset_index()
        total.columns = ['context', 'total']

        df = pd.merge(matched, total, on='context', how='outer')
        df = df.fillna(0).astype({'matched': 'int', 'total': 'int'})

        df['percent'] = df.matched / df.total
        result = df.sort_values('percent')
        return result

    @cached_property
    def matched_target(self):
        result = [
            flow
            for flow in self.target_flows 
            if flow.id in self.matched_target_flows_ids
        ]
        return result

    @cached_property
    def unmatched_target(self):
        result = [
            flow
            for flow in self.target_flows 
            if flow.id not in self.matched_target_flows_ids
        ]
        return result

    @cached_property
    def matched_target_statistics(self):
        matched = Counter([flow.context.full for flow in self.matched_target])
        matched = pd.Series(matched).reset_index()
        matched.columns = ['context', 'matched']

        total = Counter([flow.context.full for flow in self.target_flows])
        total = pd.Series(total).reset_index()
        total.columns = ['context', 'total']

        df = pd.merge(matched, total, on='context', how='outer')
        df = df.fillna(0).astype({'matched': 'int', 'total': 'int'})

        df['percent'] = df.matched / df.total
        result = df.sort_values('percent')
        return result

    def statistics(self):
        print(f'{len(self.source_flows)} source flows...')
        print(f'{len(self.target_flows)} target flows...')
        print(f'{len(self.mappings)} mappings ({len(self.matched_source) / len(self.source_flows):.2%} of total).')

    def to_randonneur(self):
        result = [
            format_match_result(map_entry['from'], 
                                map_entry['to'],
                                map_entry['conversion_factor'],
                                map_entry['info']) 
            for map_entry in self.mappings
        ]
        return result

    def to_glad(self):
        data = []
        for map_entry in self.mappings:
            row = {
                    'SourceFlowName': map_entry['from'].name,
                    'SourceFlowUUID': map_entry['from'].uuid,
                    'SourceFlowContext': map_entry['from'].context.full,
                    'SourceUnit': map_entry['from'].unit,
                    'MatchCondition': '',
                    'ConversionFactor': map_entry['conversion_factor'],
                    'TargetFlowName': map_entry['to'].name,
                    'TargetFlowUUID': map_entry['to'].uuid,
                    'TargetFlowContext': map_entry['to'].context.full,
                    'TargetUnit': map_entry['to'].unit,
                    'MemoMapper': map_entry['info'].get('comment')
                }
            data.append(row)

        return pd.DataFrame(data)        
