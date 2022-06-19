from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import List, Tuple

from jinja2 import Template

template_path = Path(__file__).parent / "template.py.jinja2"
output_path = Path(__file__).parent.parent / "db_model/sql/_select.py"


@dataclass
class Arg:
    name: str
    annotation: str


ITERS = 3


def main() -> None:
    signatures: List[Tuple[List[Arg], List[str]]] = []
    for total_args in range(1, ITERS + 1):
        arg_types_tuples = product(("column", "model", "value"), repeat=total_args)
        for arg_type_tuple in arg_types_tuples:
            args: List[Arg] = []
            return_types: List[str] = []
            for i, arg_type in enumerate(arg_type_tuple):
                t_type = f"_TVal_{i}"
                if arg_type == "column":
                    t_var = f"ColumnClause[TypeEngine[{t_type}]]"
                    arg = Arg(name=f"column_{i}", annotation=t_var)
                elif arg_type == "model":
                    t_var = f"type[{t_type}]"
                    arg = Arg(name=f"entity_{i}", annotation=t_var)
                else:
                    t_var = t_type
                    arg = Arg(name=f"value_{i}", annotation=t_var)
                args.append(arg)
                return_types.append(t_type)
            signatures.append((args, return_types))

    template: Template = Template(template_path.read_text())
    result = template.render(
        number_of_types=ITERS,
        signatures=signatures,
    )
    output_path.write_text(result)


if __name__ == "__main__":
    main()
