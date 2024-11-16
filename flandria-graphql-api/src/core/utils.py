import os
import sysconfig


def get_semaphore_limit() -> int:
    cpu_count = os.cpu_count()
    semaphore_limit = cpu_count if cpu_count is not None else 1
    if "SEMAPHORE_LIMIT" in os.environ:
        semaphore_limit = int(os.environ["SEMAPHORE_LIMIT"])

    return semaphore_limit


def run_ruff(path: str, *args: str):
    # https://github.com/astral-sh/ruff/issues/659#issuecomment-1385998994
    ruff = os.path.join(sysconfig.get_path("scripts"), "ruff")
    os.spawnv(os.P_WAIT, ruff, [ruff, "format", path, *args])
