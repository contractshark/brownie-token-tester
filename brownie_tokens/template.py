from brownie import Contract, compile_source
from pathlib import Path
from typing import Union

RETURN_TYPE = {
    True: " -> bool",
    False: " -> bool",
    None: "",
}

RETURN_STATEMENT = {
    True: "return True",
    False: "return False",
    None: "return",
}

FAIL_STATEMENT = {
    "revert": "raise",
    True: "return True",
    False: "return False",
    None: "return",
}

with Path(__file__).parent.joinpath("token-template.vy").open() as fp:
    TEMPLATE = fp.read()


def ERC20(
    name: str = "Test Token",
    symbol: str = "TST",
    decimals: int = 18,
    success: Union[bool, None] = True,
    fail: Union[bool, str, None] = "revert",
) -> Contract:
    if success not in RETURN_STATEMENT:
        valid_keys = [str(i) for i in RETURN_STATEMENT.keys()]
        raise ValueError(f"Invalid value for `success`, valid options are: {', '.join(valid_keys)}")
    if fail not in FAIL_STATEMENT:
        valid_keys = [str(i) for i in FAIL_STATEMENT.keys()]
        raise ValueError(f"Invalid value for `fail`, valid options are: {', '.join(valid_keys)}")

    source = TEMPLATE.format(
        return_type=RETURN_TYPE[success],
        return_statement=RETURN_STATEMENT[success],
        fail_statement=FAIL_STATEMENT[fail],
    )
    deployer = compile_source(source).Vyper

    return deployer.deploy(
        name,
        symbol,
        decimals,
        {"from": "0x0000000000000000000000000000000000001337", "silent": True},
    )