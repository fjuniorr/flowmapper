import typer
from typing_extensions import Annotated
from pathlib import Path
import logging
from typing import Optional
from typing_extensions import Annotated
import importlib.metadata
import logging
import json
from pathlib import Path
from enum import Enum
from .flow import Flow
from .utils import read_field_mapping, read_flowlist
from .flowmap import Flowmap
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

logger = logging.getLogger(__name__)

app = typer.Typer()

def version_callback(value: bool):
    if value:
        print(f"flowmapper, version {importlib.metadata.version('flowmapper')}")
        raise typer.Exit()

class OutputFormat(str, Enum):
    all = 'all'
    glad = 'glad'
    randonneur = 'randonneur'

@app.callback()
def main(version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,):
    """
    Generate mappings between elementary flows lists
    """

@app.command()
def map(
    source: Annotated[Path, typer.Argument(help='Path to source flowlist')],
    target: Annotated[Path, typer.Argument(help='Path to target flowlist')],
    fields: Annotated[Path, typer.Option(help='Relationship between fields in source and target flowlists')],
    matched: Annotated[bool, typer.Option(help='Write original matched flows into separate file?')] = False,
    unmatched: Annotated[bool, typer.Option(help='Write original unmatched flows into separate file?')] = True,
    output_dir: Annotated[Path, typer.Option(help='Directory to save mapping and diagnostics files')] = Path('.'),
    format: Annotated[OutputFormat, typer.Option(help='Mapping file output format', case_sensitive=False)] = 'all'
):
    """
    Generate mappings between elementary flows lists
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    field_mapping = read_field_mapping(fields)
    source_flows = [Flow.from_dict(flow, field_mapping['source']) for flow in read_flowlist(source)]
    target_flows = [Flow.from_dict(flow, field_mapping['target']) for flow in read_flowlist(target)]

    flowmap = Flowmap(source_flows, target_flows)
    flowmap.match()

    stem = f'{source.stem}-{target.stem}'

    if matched:
        with open(output_dir / f'{stem}-matched.json', 'w') as fs:
            json.dump(flowmap.matched, fs, indent=True)

    if unmatched:
        with open(output_dir / f'{stem}-unmatched.json', 'w') as fs:
            json.dump(flowmap.unmatched, fs, indent=True)
    
    if format.value == 'randonneur':
        with open(output_dir / f'{stem}.json', 'w') as fs:
            json.dump(flowmap.to_randonneur(), fs, indent=2)
    elif format.value == 'glad':
        flowmap.to_glad().to_excel(output_dir / f'{stem}.xlsx', index = False)
    else:
        with open(output_dir / f'{stem}.json', 'w') as fs:
            json.dump(flowmap.to_randonneur(), fs, indent=2)
        flowmap.to_glad().to_excel(output_dir / f'{stem}.xlsx', index = False)
