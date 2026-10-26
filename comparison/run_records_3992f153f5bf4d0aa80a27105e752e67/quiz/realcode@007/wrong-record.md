# 错题记录

## 2026-10-24 18:49:23 · Q003 · FAIL

判分(byte_equal)：第 2 字符起不一致：标准「}」vs 作答「"records": []}」；作答摘要：{"records": []}
- 2026-10-24 18:49:31 复答 Q003 → PASS

## 2026-10-24 18:49:43 · Q004 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「[{"device":"/dev/disk1",」vs 作答「{"device": "/dev/disk1",」；作答摘要：{"device": "/dev/disk1", "description": "Macintosh HD", "size": "249.8 GB", "mountpoint": "/"}
- 2026-10-24 18:49:50 复答 Q004 → PASS

## 2026-10-24 18:50:08 · Q008 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「error=unsupported_platfo」vs 作答「{"error":"unsupported pl」；作答摘要：{"error":"unsupported platform: foobar"}
- 2026-10-24 18:50:23 复答 Q008 → FAIL
- 2026-10-24 18:50:25 复答 Q008 → PASS

## 2026-10-24 18:51:43 · Q007 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「[{"device":"/dev/sda","d」vs 作答「platform=linux
routine=l」；作答摘要：platform=linux routine=lsblk device=/dev/sda description=My drive size=15 GB mountpoint=/mnt/drive
- 2026-10-24 18:52:04 复答 Q007 → PASS

## 2026-10-24 18:52:30 · Q010 · FAIL

判分(keyword)：未命中的必要要点: where platform=<name>；作答摘要：C007: If the dispatcher's routing field `action` equals "list" and the `platform` value is NOT one of the supported platforms (e.g. "linux"), the dispatcher must NOT raise an exception; instead it pri
- 2026-10-24 18:52:39 复答 Q010 → PASS

## 2026-10-24 18:52:48 · Q009 · FAIL

判分(keyword)：未命中的必要要点: nothing to report a list with no items []；作答摘要：C001: When parsing a line of raw key/value text, split each line on the first ":" separator. Where the line contains a separator and a proper value, record it as key=value with the value trimmed, surr
- 2026-10-24 18:52:58 复答 Q009 → PASS

## 2026-10-24 19:05:29 · Q010 · FAIL

判分(keyword)：未命中的必要要点: where；作答摘要：C007: Where the requested platform is unsupported, the dispatcher fails gracefully with a machine-readable error instead of raising: it prints `error=unsupported_platform` followed by a line `platform
- 2026-10-24 19:07:31 复答 Q010 → PASS
