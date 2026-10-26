# 错题记录

## 2026-10-24 18:28:11 · Q002 · FAIL

判分(set_match)：缺失项: nested passthru with_return ；多余/错拼项: borrow proxy reentrant ；作答摘要：action borrow reuse proxy respond_to timeout reentrant

## 2026-10-24 18:28:21 · Q001 · FAIL

判分(set_match)：缺失项: increment ops ；多余/错拼项: args method raise ；作答摘要：action size iterations timeout hold names method args raise

## 2026-10-24 18:28:43 · Q004 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「count=10
unique=1」vs 作答「true」；作答摘要：true

## 2026-10-24 18:29:01 · Q007 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「error=timeout
recovered=」vs 作答「timeout=true
error=Timeo」；作答摘要：timeout=true error=TimeoutError message=Timeout waiting for a connection
- 2026-10-24 18:29:06 复答 Q007 → PASS
- 2026-10-24 18:29:09 复答 Q002 → PASS
- 2026-10-24 18:29:11 复答 Q001 → PASS

## 2026-10-24 18:32:50 · Q003 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「value=1」vs 作答「returned=true
reused=tru」；作答摘要：returned=true reused=true
- 2026-10-24 18:32:58 复答 Q003 → PASS

## 2026-10-24 18:33:00 · Q005 · FAIL

判分(byte_equal)：第 7 字符起不一致：标准「1
value=2
value=5
value=」vs 作答「3」；作答摘要：value=3

## 2026-10-24 18:33:29 · Q008 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「calls=inner,outer,other」vs 作答「same=true」；作答摘要：same=true
- 2026-10-24 18:33:38 复答 Q008 → PASS
- 2026-10-24 18:33:40 复答 Q005 → PASS

## 2026-10-24 18:40:31 · Q009 · FAIL

判分(keyword)：未命中的必要要点: wrap；作答摘要：ConnectionPool.new(size:, timeout:) ConnectionPool#with { |conn| ... } ConnectionPool#checkout ConnectionPool#checkin ConnectionPool#available ConnectionPool::TimeoutError ConnectionPool::Wrapper#with
- 2026-10-24 18:40:40 复答 Q009 → PASS
