# 错题记录

## 2026-10-24 18:28:52 · Q002 · FAIL

判分(set_match)：缺失项: compare_standard page_number_adapter ；多余/错拼项: optimized_records ；作答摘要：mode optimized_sql optimized_records missing_boundary_error backend_adapter

## 2026-10-24 18:29:06 · Q003 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「sql_count=2
sql=SELECT "」vs 作答「{"id_sql": "SELECT id FR」；作答摘要：{"id_sql": "SELECT id FROM users LIMIT 5", "full_sql": "SELECT * FROM users WHERE id IN (?) LIMIT 5"}

## 2026-10-24 18:29:14 · Q004 · FAIL

判分(byte_equal)：第 143 字符起不一致：标准「)
sql=SELECT "organizati」vs 作答「, ?, ?, ?, ?, ?, ?, ?, ?」；作答摘要：sql_count=3 sql=SELECT "users"."id" FROM "users" LIMIT ? sql=SELECT "users".* FROM "users" WHERE "users"."id" IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,

## 2026-10-24 18:29:23 · Q006 · FAIL

判分(byte_equal)：第 6 字符起不一致：标准「=missing_page_boundary
r」vs 作答「: no page boundary set」；作答摘要：error: no page boundary set

## 2026-10-24 18:29:30 · Q008 · FAIL

判分(byte_equal)：第 90 字符起不一致：标准「 OFFSET ?
sql=SELECT "us」vs 作答「
sql=SELECT "users".* FR」；作答摘要：sql_count=3 sql=SELECT COUNT(*) FROM "users" sql=SELECT "users"."id" FROM "users" LIMIT ? sql=SELECT "users".* FROM "users" WHERE "users"."id" IN (?, ?, ?, ?, ?)
- 2026-10-24 18:30:03 复答 Q002 → PASS
- 2026-10-24 18:30:04 复答 Q003 → PASS
- 2026-10-24 18:30:06 复答 Q004 → PASS
- 2026-10-24 18:30:07 复答 Q006 → PASS
- 2026-10-24 18:30:09 复答 Q008 → FAIL
- 2026-10-24 18:32:02 复答 Q008 → PASS
