from functools import partial
from typing import Dict

import pytest

from ethereum.exceptions import InvalidBlock
from tests.helpers.load_state_tests import (
    Load,
    fetch_state_test_files,
    idfn,
    run_blockchain_st_test,
)

fetch_constantinople_tests = partial(
    fetch_state_test_files, network="ConstantinopleFix"
)

FIXTURES_LOADER = Load("ConstantinopleFix", "constantinople")

run_constantinople_blockchain_st_tests = partial(
    run_blockchain_st_test, load=FIXTURES_LOADER
)

# Run legacy general state tests
test_dir = (
    "tests/fixtures/LegacyTests/Constantinople/BlockchainTests/"
    "GeneralStateTests/"
)


# These are tests that are considered to be incorrect,
# Please provide an explanation when adding entries
INCORRECT_UPSTREAM_STATE_TESTS = (
    # The test considers a scenario that cannot be reached by following the
    # rules of consensus. For more details, read:
    # https://github.com/ethereum/py-evm/pull/1224#issuecomment-418775512
    "stRevertTest/RevertInCreateInInit_d0g0v0.json",
    # The test considers a scenario that cannot be reached by following the
    # rules of consensus.
    "stCreate2/RevertInCreateInInitCreate2_d0g0v0.json",
    # The test considers a scenario that cannot be reached by following the
    # rules of consensus.
    "stSStoreTest/InitCollision_d0g0v0.json",
    # The test considers a scenario that cannot be reached by following the
    # rules of consensus.
    "stSStoreTest/InitCollision_d1g0v0.json",
    # The test considers a scenario that cannot be reached by following the
    # rules of consensus.
    "stSStoreTest/InitCollision_d2g0v0.json",
    # The test considers a scenario that cannot be reached by following the
    # rules of consensus.
    "stSStoreTest/InitCollision_d3g0v0.json",
)

# All tests that recursively create a large number of frames (50000)
BIG_MEMORY_TESTS = ("50000_",)


@pytest.mark.parametrize(
    "test_case",
    fetch_constantinople_tests(
        test_dir,
        ignore_list=INCORRECT_UPSTREAM_STATE_TESTS,
        big_memory_list=BIG_MEMORY_TESTS,
    ),
    ids=idfn,
)
def test_general_state_tests(test_case: Dict) -> None:
    try:
        run_constantinople_blockchain_st_tests(test_case)
    except KeyError:
        # FIXME: Handle tests that don't have post state
        pytest.xfail(f"{test_case} doesn't have post state")


# Run legacy valid block tests
test_dir = (
    "tests/fixtures/LegacyTests/Constantinople/BlockchainTests/ValidBlocks/"
)

IGNORE_LIST = (
    "bcForkStressTest/ForkStressTest.json",
    "bcGasPricerTest/RPC_API_Test.json",
    "bcMultiChainTest",
    "bcTotalDifficultyTest",
)

# Every test below takes more than  60s to run and
# hence they've been marked as slow
SLOW_TESTS = ("bcExploitTest/DelegateCallSpam.json",)

BIG_MEMORY_TESTS = ("randomStatetest94_",)


@pytest.mark.parametrize(
    "test_case",
    fetch_constantinople_tests(
        test_dir,
        ignore_list=IGNORE_LIST,
        slow_list=SLOW_TESTS,
        big_memory_list=BIG_MEMORY_TESTS,
    ),
    ids=idfn,
)
def test_valid_block_tests(test_case: Dict) -> None:
    try:
        run_constantinople_blockchain_st_tests(test_case)
    except KeyError:
        # FIXME: Handle tests that don't have post state
        pytest.xfail(f"{test_case} doesn't have post state")


# Run legacy invalid block tests
test_dir = (
    "tests/fixtures/LegacyTests/Constantinople/BlockchainTests/InvalidBlocks"
)

xfail_candidates = ("GasLimitHigherThan2p63m1_ConstantinopleFix",)


@pytest.mark.parametrize(
    "test_case",
    fetch_constantinople_tests(test_dir),
    ids=idfn,
)
def test_invalid_block_tests(test_case: Dict) -> None:
    try:
        # Ideally correct.json should not have been in the InvalidBlocks folder
        if test_case["test_key"] == "correct_ConstantinopleFix":
            run_constantinople_blockchain_st_tests(test_case)
        elif test_case["test_key"] in xfail_candidates:
            # Unclear where this failed requirement comes from
            pytest.xfail()
        else:
            with pytest.raises(InvalidBlock):
                run_constantinople_blockchain_st_tests(test_case)
    except KeyError:
        # FIXME: Handle tests that don't have post state
        pytest.xfail(
            "{} doesn't have post state".format(test_case["test_key"])
        )


# Run Non-Legacy GeneralStateTests
test_dir = "tests/fixtures/BlockchainTests/GeneralStateTests/"

non_legacy_only_in = (
    "stCreateTest/CREATE_HighNonce.json",
    "stCreateTest/CREATE_HighNonceMinus1.json",
)


@pytest.mark.parametrize(
    "test_case",
    fetch_constantinople_tests(test_dir, only_in=non_legacy_only_in),
    ids=idfn,
)
def test_general_state_tests_new(test_case: Dict) -> None:
    run_constantinople_blockchain_st_tests(test_case)
