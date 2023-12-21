from functools import cached_property
from .flow import Flow
from .match import match_rules, format_match_result
from .unit import Unit
from tqdm import tqdm
from typing import Callable
import pandas as pd
from collections import Counter

class Flowmap:
    def __init__(
        self,
        source_flows: list[Flow],
        target_flows: list[Flow],
        rules: list[Callable[..., bool]] = None,
        nomatch_rules: list[Callable[..., bool]] = None,
        disable_progress: bool = False,
    ):
        self.disable_progress = disable_progress
        self.rules = rules if rules else match_rules()
        if nomatch_rules:
            self.source_flows = []
            self.source_flows_nomatch = []
            
            for flow in source_flows:
                matched = False
                for rule in nomatch_rules:
                    if rule(flow):
                        self.source_flows_nomatch.append(flow)
                        matched = True
                        break
                if not matched:
                    self.source_flows.append(flow)

            self.target_flows = []
            self.target_flows_nomatch = []

            for flow in target_flows:
                matched = False
                for rule in nomatch_rules:
                    if rule(flow):
                        self.target_flows_nomatch.append(flow)
                        matched = True
                        break
                if not matched:
                    self.target_flows.append(flow)
        else:
            self.source_flows = source_flows
            self.source_flows_nomatch = []
            self.target_flows = target_flows
            self.target_flows_nomatch = []

    @cached_property
    def mappings(self):
        all_mappings = []
        for s in tqdm(self.source_flows, disable=self.disable_progress):
            for t in self.target_flows:
                for rule in self.rules:
                    is_match = rule(s, t)
                    if is_match:
                        all_mappings.append(
                            {'from': s,
                             'to': t,
                             'conversion_factor': s.unit.conversion_factor(t.unit),
                             'match_rule': rule.__name__,
                             'match_rule_priority': self.rules.index(rule),
                             'info': is_match}
                        )
                        break
        result = []
        seen_sources = set()
        sorted_mappings = sorted(all_mappings, key=lambda x: (x['from'], x['match_rule_priority']))
        for mapping in sorted_mappings:
            if mapping['from'] not in seen_sources:
                result.append(mapping)
                seen_sources.add(mapping['from'])
        
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
        matched = Counter([flow.context.value for flow in self.matched_source])
        matched = pd.Series(matched).reset_index()
        matched.columns = ['context', 'matched']

        total = Counter([flow.context.value for flow in self.source_flows])
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
        matched = Counter([flow.context.value for flow in self.matched_target])
        matched = pd.Series(matched).reset_index()
        matched.columns = ['context', 'matched']

        total = Counter([flow.context.value for flow in self.target_flows])
        total = pd.Series(total).reset_index()
        total.columns = ['context', 'total']

        df = pd.merge(matched, total, on='context', how='outer')
        df = df.fillna(0).astype({'matched': 'int', 'total': 'int'})

        df['percent'] = df.matched / df.total
        result = df.sort_values('percent')
        return result

    def statistics(self):
        source_msg = (
            f"{len(self.source_flows)} source flows ({len(self.source_flows_nomatch)} excluded)..."
            if self.source_flows_nomatch
            else f"{len(self.source_flows)} source flows..."
        )
        print(source_msg)
        target_msg = (
            f"{len(self.target_flows)} target flows ({len(self.target_flows_nomatch)} excluded)..."
            if self.target_flows_nomatch
            else f"{len(self.target_flows)} target flows..."
        )
        print(target_msg)
        print(
            f"{len(self.mappings)} mappings ({len(self.matched_source) / len(self.source_flows):.2%} of total)."
        )
        cardinalities = dict(Counter([x['cardinality'] for x in self.cardinalities]))
        print(f"Mappings cardinalities: {str(cardinalities)}")

    @cached_property
    def cardinalities(self):
        mappings = [(mapentry['from'].id, mapentry['to'].id) for mapentry in self.mappings]
        lhs_counts = Counter([pair[0] for pair in mappings])
        rhs_counts = Counter([pair[1] for pair in mappings])

        result = []

        for lhs, rhs in mappings:
            lhs_count = lhs_counts[lhs]
            rhs_count = rhs_counts[rhs]
            if lhs_count == 1 and rhs_count == 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "1:1"})
            elif lhs_count == 1 and rhs_count > 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "N:1"})
            elif lhs_count > 1 and rhs_count == 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "1:N"})
            elif lhs_count > 1 and rhs_count > 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "N:M"})

        return sorted(result, key = lambda x: x['from'])

    def to_randonneur(self):
        result = [
            format_match_result(map_entry['from'], 
                                map_entry['to'],
                                map_entry['conversion_factor'],
                                map_entry['info']) 
            for map_entry in self.mappings
        ]
        return result

    def to_glad(self, ensure_id: bool = False):
        data = []
        for map_entry in self.mappings:
            source_flow_id = map_entry['from'].uuid if map_entry['from'].uuid or not ensure_id else map_entry['from'].id
            row = {
                    'SourceFlowName': map_entry['from'].name_raw_value,
                    'SourceFlowUUID': source_flow_id,
                    'SourceFlowContext': '/'.join(map_entry['from'].context_raw_value),
                    'SourceUnit': map_entry['from'].unit_raw_value,
                    'MatchCondition': '',
                    'ConversionFactor': map_entry['conversion_factor'],
                    'TargetFlowName': map_entry['to'].name_raw_value,
                    'TargetFlowUUID': map_entry['to'].uuid,
                    'TargetFlowContext': map_entry['to'].context.raw_value,
                    'TargetUnit': map_entry['to'].unit.raw_value,
                    'MemoMapper': map_entry['info'].get('comment')
                }
            data.append(row)

        return pd.DataFrame(data)        
