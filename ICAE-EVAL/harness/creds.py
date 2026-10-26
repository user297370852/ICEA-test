"""Runtime credential resolution from the local (gitignored) models.json.

models.json is the user's canonical credential store at the repo root. The two
git-tracked config files (model_list.json / user_agent/user_model.json) ship
sanitized placeholders, so at runtime we override their endpoint/token fields
from models.json when the corresponding section exists. Nothing here ever
prints or persists secrets; it only rewrites values in memory.

models.json format (INI-ish, sections as `Name:[ ... ];`):

    AI_Core:[
    base-url:https://svip.xty.app/v1
    api-key:sk-...
    model-id: gpt-6.1-sol
    ];
    Zcode:[
    api-id:...
    api-key:...
    <protocol documentation lines with https URLs>
    ];
    ark_code:[
    base-url-openai:https://ark.cn-beijing.volces.com/api/plan/v3
    base-url-anthropic:https://ark.cn-beijing.volces.com/api/plan
    api-key:ark-...
    model-id:glm-5.3-flash
    ];

Priority: explicit ICAE_* environment variables > models.json section >
whatever the tracked config file already carries (possibly a placeholder).
"""
import os
import re
from pathlib import Path


def _models_json_path() -> Path | None:
    v = os.environ.get("ICAE_MODELS_JSON")
    if v:
        p = Path(v).expanduser()
        return p if p.is_file() else None
    # default: repo root (parent of this harness/ dir) / models.json
    p = Path(__file__).resolve().parent.parent.parent / "models.json"
    return p if p.is_file() else None


def _parse_sections(text: str) -> dict[str, dict]:
    """Parse the top-level `Section:[ key:value ... ];` blocks into dicts.

    Tolerant: skips documentation lines, ignores unknown keys, strips whitespace.
    """
    sections: dict[str, dict] = {}
    for m in re.finditer(r"(\w+)\s*:\s*\[(.*?)\]", text, re.S):
        name, body = m.group(1), m.group(2)
        fields: dict[str, str] = {}
        for line in body.splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, _, val = line.partition(":")
            key = key.strip().lower()
            val = val.strip()
            if not val:
                continue
            fields[key] = val
        sections[name.lower()] = fields
    return sections


_CACHE: dict | None = None


def load_sections() -> dict[str, dict]:
    """Parsed models.json sections ({} when the file is absent). Cached."""
    global _CACHE
    if _CACHE is None:
        p = _models_json_path()
        _CACHE = _parse_sections(p.read_text(encoding="utf-8")) if p else {}
    return _CACHE


def _placeholder(v: str | None) -> bool:
    return not v or v.strip().startswith("<") or "YOUR" in (v or "").upper()


def ark_anthropic() -> dict:
    """{base_url, token, model} for the ark anthropic-compatible endpoint.

    Env override first (ICAE_ARK_BASE_URL / ICAE_ARK_TOKEN), then models.json
    ark_code. Returns {} when neither is available (caller keeps file values).
    """
    out: dict = {}
    env_base = os.environ.get("ICAE_ARK_BASE_URL")
    env_tok = os.environ.get("ICAE_ARK_TOKEN")
    sec = load_sections().get("ark_code", {})
    base = env_base or (sec.get("base-url-anthropic") or None)
    tok = env_tok or (sec.get("api-key") or None)
    model = sec.get("model-id") or "glm-5.3-flash"
    if base and tok:
        out = {"base_url": base, "token": tok, "model": model}
    return out


def ai_core() -> dict:
    """{base_url, api_key, model} for the AI_Core OpenAI-compatible endpoint."""
    sec = load_sections().get("ai_core", {})
    base = sec.get("base-url")
    key = sec.get("api-key")
    model = sec.get("model-id") or "gpt-6.1-sol"
    if base and key and not _placeholder(key):
        return {"base_url": base, "api_key": key, "model": model}
    return {}


def zcode_openai() -> dict:
    """{base_url, api_key, model} for the Zcode OpenAI-compatible endpoint.

    The Zcode section documents several protocol URLs in free text; the OpenAI
    Chat Completion one is used here (judge fallback only).
    """
    p = _models_json_path()
    text = p.read_text(encoding="utf-8") if p else ""
    m = re.search(r"[Zz]code\s*:\s*\[(.*?)\]", text, re.S)
    if not m:
        return {}
    body = m.group(1)
    key = None
    for line in body.splitlines():
        k, _, v = line.strip().partition(":")
        if k.strip().lower() == "api-key" and v.strip():
            key = v.strip()
            break
    url = None
    um = re.search(r"(https://[^\s]+)", body)
    if um and "bigmodel" in um.group(1):
        url = um.group(1)
    elif um:
        url = um.group(1)
    # prefer the documented OpenAI Chat Completion URL when present
    cm = re.search(r"https://\S*bigmodel\S*/api/coding/paas/v4", body)
    if cm:
        url = cm.group(0)
    if key and url and not _placeholder(key):
        return {"base_url": url, "api_key": key, "model": "glm-5.3-flash"}
    return {}


def zcode_anthropic() -> dict:
    """{base_url, token, model} for the Zcode bigmodel anthropic-compatible
    endpoint — same glm-5.3-flash model, independent quota channel. Used as
    the fallback endpoint in the SUT/Oracle endpoint pools."""
    p = _models_json_path()
    text = p.read_text(encoding="utf-8") if p else ""
    m = re.search(r"[Zz]code\s*:\s*\[(.*?)\]", text, re.S)
    if not m:
        return {}
    key = None
    for line in m.group(1).splitlines():
        k, _, v = line.strip().partition(":")
        if k.strip().lower() == "api-key" and v.strip():
            key = v.strip()
            break
    if not key or _placeholder(key):
        return {}
    return {"base_url": "https://open.bigmodel.cn/api/anthropic",
            "token": key, "model": "glm-5.3-flash"}


def _channel_env(channel: dict) -> dict:
    return {"ANTHROPIC_MODEL": channel["model"],
            "ANTHROPIC_BASE_URL": channel["base_url"],
            "ANTHROPIC_AUTH_TOKEN": channel["token"]}


def override_model_list(entries: dict) -> dict:
    """Build a multi-channel SUT/Critic endpoint pool per model.

    Pool order: ark (primary) + zcode bigmodel (fallback, same glm-5.3-flash,
    independent quota). The harness rotates endpoints on 429/infra errors
    (_run_with_backoff / CriticPool), so a single channel's quota exhaustion
    only costs one failed attempt per repo; the run stops only when ALL
    channels are exhausted. Tracked config files stay untouched.
    """
    channels = [c for c in (ark_anthropic(), zcode_anthropic()) if c]
    if not channels:
        return entries
    for section in ("Tested Model", "Critic Model"):
        table = entries.get(section)
        if not isinstance(table, dict):
            continue
        for name, entry in table.items():
            # Only poolify anthropic-routed claude-code entries; preserve any
            # openhands variants as-is.
            variants = entry if isinstance(entry, list) else [entry]
            kept = [e for e in variants if isinstance(e, dict)
                    and "OPENHANDS_MODEL" in e]
            pool = [dict(_channel_env(c)) for c in channels]
            table[name] = (kept + pool) if kept else pool
    return entries


def override_user_models(models: dict) -> dict:
    """Build the Oracle backend pool per model: ark primary + zcode fallback.

    user_agent's own round-robin (skip-on-failure, 60s) handles channel
    failover per request."""
    channels = [c for c in (ark_anthropic(), zcode_anthropic()) if c]
    if not channels:
        return models
    for name, entry in models.items():
        if not isinstance(entry, list):
            continue
        backends = [e for e in entry if isinstance(e, dict)
                    and e.get("api_type", "anthropic") != "anthropic"]
        for c in channels:
            backends.append({"api_type": "anthropic",
                             "model_name": c["model"],
                             "base_url": c["base_url"],
                             "auth_token": c["token"]})
        models[name] = backends
    return models


def write_judge_config(path: Path) -> Path | None:
    """Write the gitignored judge endpoint config consumed by the plugin's
    judge_llm.py (AI_Core gpt-6.1-sol primary, Zcode glm fallback).

    The file lives under results/ (already gitignored) and holds real keys, so
    it must never be committed or copied elsewhere.
    """
    primary = ai_core()
    fallback = zcode_openai()
    if not primary and not fallback:
        return None
    import json
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "primary": primary or None,
        "fallback": fallback or None,
        "timeout_s": 60,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
