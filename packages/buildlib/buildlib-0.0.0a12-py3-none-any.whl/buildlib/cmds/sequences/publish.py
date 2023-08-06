import prmt
from cmdinter import CmdFuncResult
from typing import Union, List, Optional
from buildlib.utils.yaml import load_yaml
from buildlib.utils.semver.prompt import prompt_semver_num_by_choice, prompt_semver_num_manually
from buildlib.cmds import build
from buildlib.utils.semver import convert_semver_to_wheelver, get_python_wheel_name_from_semver_num


def _load_cfg(path):
    try:
        return load_yaml(path, keep_order=True)
    except:
        return None


def _get_cur_version(cfg_file):
    cfg = _load_cfg(cfg_file)
    cur_version: str = cfg and cfg.get('version')

    return cur_version


def _get_new_version(cur_version):
    if cur_version:
        return prompt_semver_num_by_choice(cur_version)
    else:
        return prompt_semver_num_manually()


def get_args_interactively(
    run_any: Union[bool, str] = True,
    run_update_version: Union[bool, str] = False,
    run_build_file: Union[bool, str] = False,
    run_push_gemfury: Union[bool, str] = False,
    run_push_pypi: Union[bool, str] = False,
    cfg_file: Optional[str] = None,
    build_file: Optional[str] = None,
    wheel_dir: Optional[str] = None,
    cur_version: Optional[str] = None,
    new_version: Optional[str] = None,
) -> dict:
    """"""

    if type(run_any) == str:
        run_any: bool = prmt.confirm(
            question='Run ANY GIT COMMANDS?\n',
            default=run_any
        )

    if run_any and type(run_update_version) == str:
        run_update_version: bool = prmt.confirm(
            question='Do you want to update the VERSION NUMBER before publishing?\n',
            default=run_update_version
        )

        if run_update_version and not new_version:
            cur_version = cur_version or _get_cur_version(cfg_file)
            new_version = _get_new_version(cur_version)

    if run_any and type(run_build_file) == str:
        run_build_file: bool = prmt.confirm(
            question='Do you want to RUN BUILD FILE before publishing?\n',
            default=run_build_file
        )

    if run_any and type(run_push_gemfury) == str:
        run_push_gemfury: bool = prmt.confirm(
            question='Do you want to PUSH the new version to GEMFURY?\n',
            default=run_push_gemfury
        )

        if run_update_version and not new_version:
            cur_version = cur_version or _get_cur_version(cfg_file)
            new_version = _get_new_version(cur_version)

    if run_any and type(run_push_pypi) == str:
        run_push_pypi: bool = prmt.confirm(
            question='Do you want to PUSH the new version to PYPI?\n',
            default=run_push_pypi
        )

        if run_update_version and not new_version:
            cur_version = cur_version or _get_cur_version(cfg_file)
            new_version = _get_new_version(cur_version)

    return {
        'run_any': run_any,
        'run_update_version': run_update_version,
        'run_build_file': run_build_file,
        'run_push_gemfury': run_push_gemfury,
        'run_push_pypi': run_push_pypi,
        'cfg_file': cfg_file,
        'build_file': build_file,
        'wheel_dir': wheel_dir,
        'version': new_version,
    }


def run_seq(
    run_any: bool = True,
    run_update_version: bool = False,
    run_build_file: bool = False,
    run_push_gemfury: bool = False,
    run_push_pypi: bool = False,
    cfg_file: Optional[str] = None,
    build_file: Optional[str] = None,
    wheel_dir: Optional[str] = None,
    version: Optional[str] = None,
) -> List[CmdFuncResult]:
    """"""
    results = []

    if not run_any:
        return results

    if run_update_version:
        results.append(build.update_version_num_in_cfg_yaml(cfg_file, version))

    if run_build_file:
        results.append(build.run_build_file(build_file))

    if run_push_gemfury:
        wheel_version: str = convert_semver_to_wheelver(version)
        wheel_name: str = get_python_wheel_name_from_semver_num(wheel_version, wheel_dir)

        if not wheel_name:
            print('There is no build for requested version.')
            return results

        wheel_file = wheel_dir + '/' + wheel_name
        results.append(build.push_python_wheel_to_gemfury(wheel_file))

    if run_push_pypi:
        results.append(build.push_python_wheel_to_pypi())

    return results


def run_seq_interactively(
    run_update_version: Union[bool, str] = False,
    run_build_file: Union[bool, str] = False,
    run_push_gemfury: Union[bool, str] = False,
    run_push_pypi: Union[bool, str] = False,
    cfg_file: Optional[str] = None,
    build_file: Optional[str] = None,
    wheel_dir: Optional[str] = None,
    cur_version: Optional[str] = None,
    new_version: Optional[str] = None,
) -> List[CmdFuncResult]:
    """"""
    seq_args: dict = get_args_interactively(**locals())

    return run_seq(**seq_args)
