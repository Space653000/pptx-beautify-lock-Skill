from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import importlib.util
import json
import os
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request

UPDATE_REPO = "Space653000/pptx-beautify-lock-Skill"
UPDATE_BRANCH = "fix/separate-skill-exe-backup-v062"
UPDATE_MANIFEST_PATH = "launcher/update_manifest.json"
DEFAULT_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True)
class UpdateSelection:
    engine_path: Path | None
    engine_version: str
    status: str
    commit_sha: str | None = None


def _version_tuple(value: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", value or "")
    return tuple(int(p) for p in parts[:4]) or (0,)


def _cache_root() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    base = Path(local) if local else Path.home() / "AppData" / "Local"
    root = base / "PPTXBeautifyOffline" / "engine_updates"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _request_bytes(url: str, timeout: float) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "PPTX-Beautify-Offline-Updater/0.7.1"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _request_json(url: str, timeout: float) -> dict:
    return json.loads(_request_bytes(url, timeout).decode("utf-8"))


def _cached_best(local_version: str) -> tuple[Path | None, str]:
    best_path: Path | None = None
    best_version = local_version
    for path in _cache_root().glob("pptx_offline_engine-*.py"):
        version = path.stem.removeprefix("pptx_offline_engine-")
        if _version_tuple(version) > _version_tuple(best_version):
            try:
                source = path.read_text(encoding="utf-8")
                compile(source, str(path), "exec")
            except Exception:
                continue
            best_path = path
            best_version = version
    return best_path, best_version


def check_for_engine_update(
    *,
    local_version: str,
    launcher_version: str,
    log=lambda _text: None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> UpdateSelection:
    cached_path, effective_version = _cached_best(local_version)
    selected = UpdateSelection(cached_path, effective_version, "cached" if cached_path else "bundled")

    encoded_branch = urllib.parse.quote(UPDATE_BRANCH, safe="")
    branch_url = f"https://api.github.com/repos/{UPDATE_REPO}/branches/{encoded_branch}"

    try:
        branch_data = _request_json(branch_url, timeout)
        commit_sha = branch_data["commit"]["sha"]
        manifest_url = (
            f"https://raw.githubusercontent.com/{UPDATE_REPO}/{commit_sha}/{UPDATE_MANIFEST_PATH}"
        )
        manifest = _request_json(manifest_url, timeout)
        remote_version = str(manifest["engine_version"])
        min_launcher = str(manifest.get("min_launcher_version", "0"))
        engine_path = str(manifest["engine_path"])
        log("UPDATE_CHECK=online")
        log(f"UPDATE_BRANCH={UPDATE_BRANCH}")
        log(f"UPDATE_COMMIT={commit_sha}")
        log(f"REMOTE_ENGINE_VERSION={remote_version}")

        if _version_tuple(min_launcher) > _version_tuple(launcher_version):
            log("UPDATE_STATUS=new_exe_required")
            log(f"MIN_LAUNCHER_VERSION={min_launcher}")
            return UpdateSelection(selected.engine_path, selected.engine_version, "new_exe_required", commit_sha)

        if _version_tuple(remote_version) <= _version_tuple(effective_version):
            log("UPDATE_STATUS=up_to_date")
            log(f"EFFECTIVE_ENGINE_VERSION={effective_version}")
            return UpdateSelection(selected.engine_path, selected.engine_version, "up_to_date", commit_sha)

        raw_url = f"https://raw.githubusercontent.com/{UPDATE_REPO}/{commit_sha}/{engine_path}"
        payload = _request_bytes(raw_url, timeout)
        source = payload.decode("utf-8")
        if "def beautify_pptx" not in source or "STYLE_PRESETS" not in source:
            raise ValueError("remote engine failed contract validation")
        compile(source, raw_url, "exec")

        root = _cache_root()
        target = root / f"pptx_offline_engine-{remote_version}.py"
        fd, temp_name = tempfile.mkstemp(prefix="engine-update-", suffix=".py", dir=root)
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            temp_path.write_bytes(payload)
            os.replace(temp_path, target)
        finally:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

        log("UPDATE_STATUS=updated")
        log(f"EFFECTIVE_ENGINE_VERSION={remote_version}")
        return UpdateSelection(target, remote_version, "updated", commit_sha)

    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        log("UPDATE_CHECK=offline_skip")
        log(f"UPDATE_DETAIL={type(exc).__name__}")
        log(f"EFFECTIVE_ENGINE_VERSION={selected.engine_version}")
        return UpdateSelection(selected.engine_path, selected.engine_version, "offline_skip", None)
    except Exception as exc:
        log("UPDATE_CHECK=failed_safe_fallback")
        log(f"UPDATE_DETAIL={type(exc).__name__}: {exc}")
        log(f"EFFECTIVE_ENGINE_VERSION={selected.engine_version}")
        return UpdateSelection(selected.engine_path, selected.engine_version, "failed_safe_fallback", None)


def load_engine_module(selection: UpdateSelection, bundled_module, log=lambda _text: None):
    if selection.engine_path is None:
        return bundled_module
    try:
        name = f"pptx_offline_engine_update_{selection.engine_version.replace('.', '_')}"
        spec = importlib.util.spec_from_file_location(name, selection.engine_path)
        if spec is None or spec.loader is None:
            raise ImportError("cannot create module spec")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "beautify_pptx") or not hasattr(module, "STYLE_PRESETS"):
            raise ImportError("updated engine contract missing")
        log(f"ENGINE_SOURCE=cache:{selection.engine_path}")
        return module
    except Exception as exc:
        log(f"UPDATE_LOAD_FAIL={type(exc).__name__}: {exc}")
        log("ENGINE_SOURCE=bundled_fallback")
        return bundled_module
