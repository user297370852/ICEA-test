# 错题记录

## 2026-10-25 04:46:55 · Q003 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「reference=v1.8.0」vs 作答「version=1.8.0」；作答摘要：version=1.8.0
- 2026-10-25 04:47:14 复答 Q003 → PASS

## 2026-10-25 04:47:31 · Q006 · FAIL

判分(byte_equal)：第 7 字符起不一致：标准「could_not_clone
version=」vs 作答「Version not found
versio」；作答摘要：error=Version not found version=INVALID_VERSION
- 2026-10-25 04:47:37 复答 Q006 → PASS

## 2026-10-25 04:48:05 · Q004 · FAIL

判分(byte_equal)：第 8 字符起不一致：标准「present
v1.9.6=present
v」vs 作答「true
v1.9.6=true
v1.10.5」；作答摘要：v1.8.0=true v1.9.6=true v1.10.5=true v1.9.1+hotfix.4=true
- 2026-10-25 04:48:14 复答 Q004 → PASS

## 2026-10-25 04:51:51 · Q002 · FAIL

判分(set_match)：缺失项: action install_requires_version ；多余/错拼项: install_version ；作答摘要：resolve_version catalog_contains check_install fetch_version install_version tool_version
- 2026-10-25 04:51:59 复答 Q002 → FAIL
- 2026-10-25 04:52:04 复答 Q002 → PASS

## 2026-10-25 04:52:12 · Q009 · FAIL

判分(keyword)：未命中的必要要点: 1.8.0 prefix is prepended (e.g. ) and checked again. If the prefixed form is found, prefix (e.g. ) resolve to themselves unchanged. Channel names (；作答摘要：C001: the version reference is first matched exactly against the upstream release catalog; if the exact match fails, the tool retries the slightly modified form (adding or removing the leading "v" pre

## 2026-10-25 04:52:26 · Q010 · FAIL

判分(keyword)：未命中的必要要点: error=invalid_version\n version=<the rejected reference>\n reference=<canonical identifier>\n reference=<canonical；作答摘要：C005: when a reference cannot be matched in the upstream catalog (neither as-given nor with the "v" prefix), the output is exactly "error=invalid_version" followed by "version=<the rejected reference>
- 2026-10-25 04:52:35 复答 Q010 → PASS
- 2026-10-25 04:52:48 复答 Q009 → PASS
