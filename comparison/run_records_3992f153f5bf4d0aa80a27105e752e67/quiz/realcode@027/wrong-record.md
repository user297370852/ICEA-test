# 错题记录

## 2026-10-25 16:51:43 · Q001 · FAIL

判分(set_match)：缺失项: claims decoded_id_token request_params token ；多余/错拼项: params ；作答摘要：flow path options session params discovery
- 2026-10-25 16:51:51 复答 Q001 → PASS

## 2026-10-25 16:54:15 · Q008 · FAIL

判分(byte_equal)：第 201 字符起不一致：标准「
raw_sub=subject-123」vs 作答「」；作答摘要：uid=subject-123 name=Jane Doe email=jane@example.com nickname=jane first_name=Jane last_name=Doe gender=female image=https://cdn.example.com/jane.png phone=+1-555-0100 website=https://jane.example.com
- 2026-10-25 16:54:20 复答 Q008 → PASS

## 2026-10-25 16:54:56 · Q009 · FAIL

判分(byte_equal)：第 1 字符起不一致：标准「key_kind=jwk_set」vs 作答「algorithm=RS256
kid=1e9g」；作答摘要：algorithm=RS256 kid=1e9gdk7
- 2026-10-25 16:55:11 复答 Q009 → PASS

## 2026-10-25 16:55:45 · Q010 · FAIL

判分(keyword)：未命中的必要要点: code generated_32_hex client_id=1234 scope=openid nonce_length=32.；作答摘要：C002 (logout routing): if an `end_session_endpoint` is available (from discovery/options), the logout flow MUST redirect the user to the provider's logout page — output `status=302` and `logout_url=<e
- 2026-10-25 16:55:55 复答 Q010 → FAIL
- 2026-10-25 16:56:06 复答 Q010 → PASS

## 2026-10-25 16:56:13 · Q011 · FAIL

判分(keyword)：未命中的必要要点: logout_url=<endpoint> post_logout_redirect_uri=<uri> route=application.；作答摘要：C003 (callback state validation rule): on a `callback_request`, the `state` request param must match the session's stored `omniauth.state`. If it differs (or the session has no state), the callback fa
- 2026-10-25 16:56:21 复答 Q011 → FAIL
- 2026-10-25 16:56:29 复答 Q011 → PASS
