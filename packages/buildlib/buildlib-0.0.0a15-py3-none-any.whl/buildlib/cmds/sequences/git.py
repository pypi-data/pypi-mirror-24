import prmt
from typing import Union, List, Optional, NamedTuple
from headlines import h3
from cmdinter import CmdFuncResult
from buildlib.utils.yaml import load_yaml
from buildlib.cmds import git
from buildlib.cmds.git.prompt import prompt_commit_msg, prompt_branch
from buildlib.utils.semver.prompt import prompt_semver_num_by_choice, prompt_semver_num_manually
from buildlib.cmds.build import update_version_num_in_cfg_yaml


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
    confirm_status: Union[bool, str] = False,
    confirm_diff: Union[bool, str] = False,
    run_update_version: Union[bool, str] = False,
    run_add_all: Union[bool, str] = False,
    run_commit: Union[bool, str] = False,
    run_tag: Union[bool, str] = False,
    run_push: Union[bool, str] = False,
    cfg_file: Optional[str] = None,
    cur_version: Optional[str] = None,
    new_version: Optional[str] = None,
    branch: Optional[str] = None,
    commit_msg: Optional[str] = None
) -> dict:
    """
    Set "True": Option will be run without user confirmation.
    Set "False": Option will not be run and nothing will be asked/confirmed.
    Set "string" (e.g: "y", "n", ""): User will asked with the string as a default value.
    """

    if type(run_any) == str:
        run_any: bool = prmt.confirm(
            question='Run ANY GIT COMMANDS?\n',
            default=run_any
        )

    if run_any and type(confirm_status) == str:
        print(h3('Git Status'))
        git.status()

        run_any: bool = prmt.confirm(
            question='GIT STATUS ok?\n',
            default=confirm_status,
            margin=(1, 1))

    if run_any and type(confirm_diff) == str:
        print(h3('Git Diff'))
        git.diff()

        run_any: bool = prmt.confirm(
            question='GIT DIFF ok?\n',
            default=confirm_diff,
            margin=(1, 1)
        )

    if run_any and type(run_update_version) == str:
        run_update_version: bool = prmt.confirm(
            question='BUMP VERSION number?\n',
            default=run_update_version
        )

        if run_update_version and not new_version:
            cur_version = cur_version or _get_cur_version(cfg_file)
            new_version = _get_new_version(cur_version)

    if run_any and type(run_add_all) == str:
        run_add_all: bool = prmt.confirm(
            question='Run GIT ADD ALL ("git add --all")?\n',
            default=run_add_all
        )

    if run_any and type(run_commit) == str:
        run_commit: bool = prmt.confirm(
            question='Run GIT COMMIT?\n',
            default=run_commit
        )

        if run_commit and not commit_msg:
            commit_msg: str = prompt_commit_msg()

    if run_any and type(run_tag) == str:
        run_tag: bool = prmt.confirm(
            question='Run GIT TAG?\n',
            default='y' if new_version else 'n'
        )

        if run_tag and not new_version:
            cur_version: str = cur_version or _get_cur_version(cfg_file)
            new_version: str = _get_new_version(cur_version)

        if run_tag and not branch:
            branch: str = prompt_branch()

    if run_any and type(run_push) == str:
        run_push: bool = prmt.confirm(
            question='GIT PUSH to GITHUB?\n',
            default=run_push if type(run_push) == str else ''
        )

        if run_push and not branch:
            branch = branch or prompt_branch(),

    return {
        'run_any': run_any,
        'run_update_version': run_update_version,
        'run_add_all': run_add_all,
        'run_commit': run_commit,
        'run_tag': run_tag,
        'run_push': run_push,
        'cfg_file': cfg_file,
        'version': new_version,
        'commit_msg': commit_msg,
        'branch': branch
    }


def run_seq(
    run_any: bool = True,
    run_update_version: bool = False,
    run_add_all: bool = False,
    run_commit: bool = False,
    run_tag: bool = False,
    run_push: bool = False,
    cfg_file: Optional[str] = None,
    version: Optional[str] = None,
    commit_msg: Optional[str] = None,
    branch: Optional[str] = None,
) -> List[CmdFuncResult]:
    """"""
    results = []

    if not run_any:
        return results

    if run_update_version:
        results.append(update_version_num_in_cfg_yaml(cfg_file, version))

    if run_add_all:
        results.append(git.add_all())

    if run_commit:
        results.append(git.commit(commit_msg))

    if run_tag:
        results.append(git.tag(version, branch))

    if run_push:
        results.append(git.push(branch))

    return results


def run_seq_interactively(
    run_any: Union[bool, str] = False,
    show_status: Union[bool, str] = False,
    show_diff: Union[bool, str] = False,
    run_update_version: Union[bool, str] = False,
    run_add_all: Union[bool, str] = False,
    run_commit: Union[bool, str] = False,
    run_tag: Union[bool, str] = False,
    run_push: Union[bool, str] = False,
    cfg_file: Optional[str] = None,
    cur_version: Optional[str] = None,
    new_version: Optional[str] = None,
    branch: Optional[str] = None,
) -> List[CmdFuncResult]:
    """
    Set "True": Option will be run without user confirmation.
    Set "False": Option will not be run and nothing will be asked/confirmed.
    Set "string" (e.g: "y", "n", ""): User will asked with the string as a default value.
    """

    seq_args: dict = get_args_interactively(**locals())

    return run_seq(**seq_args)
