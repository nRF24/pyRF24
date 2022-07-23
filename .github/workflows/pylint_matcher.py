"""Parse output from clang-tidy's stdout"""
import argparse
import pathlib
import json
from typing import Dict, Union, List
import logging

log_commander = logging.getLogger("PylintMatcher")
log_commander.setLevel(logging.DEBUG)  # be sure that log commands are output
console_handler = logging.StreamHandler()  # Create special stdout stream handler
console_handler.setFormatter(logging.Formatter("%(message)s"))  # no formatted log cmds
log_commander.addHandler(console_handler)  # Use special handler for log_commander
log_commander.propagate = False  # prevent duplicate messages in the parent logger obj


def annotate_pylint_note(obj: Dict[str, Union[int, str]]) -> str:
    """Translate a 1 notification from pylint to github's checks API.

    :param dict obj: The JSON object output by pylint (for 1 notification).
        A typical JSON object output from pylint looks like:

        .. code-block:: json

            {
                "type": "error",
                "module": "basic_test",
                "obj": "",
                "line": 3,
                "column": 19,
                "path": "tests/basic_test.py",
                "symbol": "syntax-error",
                "message": "invalid syntax (<unknown>, line 3)",
                "message-id": "E0001"
            }

    :Returns:
        A `str` that can be used by github's workflow log commands.
    """
    priority = {
        "convention": "notice",
        "refactor": "notice",
        "warning": "warning",
        "error": "error",
        "fatal": "error",
    }
    return (
        "::{level} file={path},line={line},title={path}:{line}:{col} {symbol} [{code}]"
        "::{msg}".format(
            level=priority[obj["type"]],
            path=obj["path"],
            line=obj["line"],
            col=obj["column"],
            symbol=obj["symbol"],
            code=obj["message-id"],
            msg=obj["message"],
        )
    )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("json_output", type=pathlib.Path)
    args = arg_parser.parse_args()

    pylint_result: List[Dict[str, Union[int, str]]] = json.loads(
        pathlib.Path(args.json_output).read_text(encoding="utf-8")
    )
    for note in pylint_result:
        log_commander.info(annotate_pylint_note(note))
