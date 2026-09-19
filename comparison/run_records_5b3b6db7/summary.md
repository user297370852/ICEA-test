# ICAE-Bench — Per-Repo Results (GLM-5.3-Flash)

- **append_id**: `5b3b6db753be455aa9bc850574c68cd1`
- **Tested model**: GLM-5.3-Flash  |  **User model**: DeepSeek-V3.2  |  **Critic**: GLM-5.3-Flash
- **env_mode**: base  |  **prd_type**: fuzzy  |  **eval_mode**: lite  |  **query_count**: 16
- **repos evaluated**: 50
- **wall-clock**: 125.6 min (7534s)  |  **gen/repo**: mean 1835s, min 582s, max 5477s  |  **concurrency**: 4
- **finished_at**: 2026-09-19 17:13:51

## Scale & columns
- All metrics are on a **0-100 scale, one decimal**. **File Count %** and **LOC %** are generated/orig source files / LOC expressed as a percentage of the original (can exceed 100% when the generated tree is larger).
- **Test Cases Pass Rate** — `Overall` / `Public` / `Native` / `Enhanced` over `public_test_cases` / `test_cases` / `enhanced_test_cases`. **Overall** is the case-aggregated pass rate of Native+Enhanced: `(passed_native + passed_enhanced) / (total_native + total_enhanced)` — not a mean of the two rates, and not including Public. **A model-side failure (refusal, hang, or no `rcb_tests/test.sh`) scores 0% and stays in the average; infra/provisioning failures are excluded (retest-eligible).**
- **Agentic Evaluation** — three INDEPENDENT Critic scores (behavioral equivalence / public surface / engineering).
- **Structural Assessment** — generated vs golden original (in-scope subset).
- **Interaction Quality** — from the User Agent.
- **Error** — failure/missing-data cause (`no test.sh`, `build err`, `runtime err`, `mismatch`, `no output`, `docker timeout`, `gen error`, `no golden src` = structural skipped, golden source not cached). `—` = ran cleanly.

Sorted by repo index ascending.

|  |  |  | Test Cases Pass Rate |  |  |  | Agentic Evaluation |  |  | Structural Assessment |  |  |  | Interaction Quality |  |  |  |
| Repo | Source | Lang | Overall | Public | Native | Enhanced | Semantic Sim | API Sim | Design Quality | File Count % | LOC % | Class Sim | Method Sim | Constraint Cov | Fallback Rate | Budget Usage | Error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `realcode@001` | `dependents__node-dependency-tree` | JavaScript | 5.7 | 9.1 | 9.1 | 4.2 | 55.0 | 25.0 | 75.0 | 87.5 | 163.2 | 100.0 | 27.3 | 76.9 | 36.4 | 68.8 | mismatch/missing+mismatch |
| `realcode@002` | `developit__unfetch` | JavaScript | 97.4 | 100.0 | 100.0 | 94.4 | 50.0 | 45.0 | 65.0 | 233.3 | 326.7 | 100.0 | 75.0 | 70.8 | 23.1 | 81.2 | mismatch |
| `realcode@003` | `mperham__connection_pool` | Ruby | 0.0 | 0.0 | 0.0 | 0.0 | 75.0 | 65.0 | 78.0 | 37.5 | 85.2 | 100.0 | 71.4 | 100.0 | 75.0 | 100.0 | mismatch/missing+mismatch |
| `realcode@004` | `planetscale__fast_page` | Ruby | 50.0 | 100.0 | 77.8 | 33.3 | 45.0 | 10.0 | 65.0 | 81.8 | 164.5 | 0.0 | 0.0 | 80.0 | 33.3 | 93.8 | mismatch |
| `realcode@005` | `bmentges__django-cart` | Python | 60.0 | 100.0 | 100.0 | 53.8 | 45.0 | 25.0 | 78.0 | 142.9 | 171.4 | 12.5 | 16.0 | 83.3 | 12.5 | 50.0 | mismatch |
| `realcode@006` | `marp-team__marp-vscode` | TypeScript | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 65.0 | 60.0 | 100.0 | 142.9 | 100.0 | 21.4 | 81.8 | 26.7 | 93.8 | missing+mismatch |
| `realcode@007` | `balena-io-modules__drivelist` | C++ | 90.9 | 100.0 | 93.3 | 90.0 | 15.0 | 5.0 | 65.0 | 27.3 | 102.6 | 100.0 | 100.0 | 71.4 | 18.8 | 100.0 | mismatch |
| `realcode@008` | `danistefanovic__hooka` | JavaScript | 1.6 | 0.0 | 1.7 | 1.6 | 20.0 | 30.0 | 50.0 | 25.0 | 44.5 | 100.0 | 17.4 | 92.9 | 75.0 | 100.0 | mismatch |
| `realcode@009` | `dwyl__flutter-todo-list-tutorial` | Dart | 100.0 | 100.0 | 100.0 | 100.0 | 25.0 | 15.0 | 70.0 | 17.4 | 22.9 | 0.0 | 9.1 | 86.4 | 23.1 | 81.2 | — |
| `realcode@010` | `microsoft__DacFx` | C# | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 | 10.0 | 65.0 | 63.6 | 166.1 | 100.0 | 100.0 | 76.5 | 45.5 | 68.8 | no output |
| `realcode@011` | `nunomaduro__laravel-mojito` | PHP | 98.5 | 100.0 | 100.0 | 96.9 | 40.0 | 5.0 | 35.0 | 5.0 | 96.3 | 0.0 | 0.0 | 81.8 | 12.5 | 100.0 | mismatch |
| `realcode@012` | `Treblle__treblle-laravel` | PHP | 4.8 | 0.0 | 0.0 | 5.9 | 20.0 | 15.0 | 60.0 | 70.0 | 65.0 | 40.0 | 26.7 | 76.9 | 33.3 | 56.2 | missing+mismatch/partial missing |
| `realcode@013` | `aboutyou__dart_packages` | Dart | 100.0 | 100.0 | 100.0 | 100.0 | 10.0 | 5.0 | 50.0 | 4520.0 | 37068.2 | 0.0 | 16.7 | 81.2 | 30.0 | 62.5 | — |
| `realcode@014` | `ankane__distribute_reads` | Ruby | 79.0 | 82.6 | 75.0 | 82.4 | 30.0 | 15.0 | 40.0 | 18.2 | 48.2 | 50.0 | 0.0 | 46.2 | 6.2 | 100.0 | mismatch |
| `realcode@015` | `esanchezm__prometheus-qbittorrent-exporter` | Python | 0.0 | 0.0 | 0.0 | 0.0 | 25.0 | 10.0 | 70.0 | 225.0 | 55.9 | 0.0 | 7.1 | 84.0 | 46.2 | 81.2 | runtime err |
| `realcode@016` | `gemini-testing__looks-same` | JavaScript | 69.8 | 89.5 | 65.9 | 77.3 | 50.0 | 15.0 | 60.0 | 200.0 | 147.6 | 100.0 | 11.4 | 125.0 | 61.5 | 81.2 | mismatch |
| `realcode@017` | `justintaddei__v-wave` | TypeScript | 95.7 | 100.0 | 100.0 | 93.3 | 40.0 | 10.0 | 65.0 | 26.7 | 88.8 | 0.0 | 3.5 | 54.5 | 12.5 | 100.0 | mismatch |
| `realcode@018` | `atom__etch` | JavaScript | 89.3 | 100.0 | 93.8 | 87.5 | 55.0 | 5.0 | 60.0 | 18.8 | 73.7 | 0.0 | 4.3 | 82.8 | 21.4 | 87.5 | mismatch |
| `realcode@019` | `doctrine__deprecations` | PHP | 94.4 | 100.0 | 95.2 | 93.9 | 50.0 | 40.0 | 70.0 | 257.1 | 132.7 | 0.0 | 13.6 | 65.5 | 35.7 | 87.5 | mismatch |
| `realcode@020` | `shelljs__shx` | JavaScript | 0.0 | 0.0 | 0.0 | 0.0 | 15.0 | 10.0 | 70.0 | 75.0 | 148.0 | 100.0 | 0.0 | 84.6 | 20.0 | 93.8 | mismatch |
| `realcode@021` | `donovanglover__hyprnome` | Rust | 2.7 | 5.0 | 3.3 | 2.3 | 35.0 | 5.0 | 60.0 | 33.3 | 83.3 | 0.0 | 7.7 | 72.0 | 18.2 | 68.8 | partial missing |
| `realcode@022` | `jonbern__fetch-retry` | JavaScript | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 25.0 | 60.0 | 50.0 | 37.1 | 100.0 | 10.0 | 86.4 | 68.8 | 100.0 | missing+mismatch |
| `realcode@023` | `asakusarb__action_args` | Ruby | 100.0 | 100.0 | 100.0 | 100.0 | 20.0 | 5.0 | 80.0 | 40.9 | 37.1 | 0.0 | 0.0 | 75.0 | 18.8 | 100.0 | — |
| `realcode@024` | `patsplat__plist` | Ruby | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 40.0 | 70.0 | 8.3 | 43.7 | 5.3 | 2.7 | 6.9 | 6.2 | 100.0 | missing+mismatch |
| `realcode@025` | `dart-archive__ffi` | Dart | 32.7 | 33.3 | 27.3 | 40.9 | 5.0 | 10.0 | 10.0 | 5077.8 | 25164.9 | 60.0 | 16.7 | 31.2 | 6.2 | 100.0 | mismatch |
| `realcode@026` | `xnimorz__use-debounce` | TypeScript | 0.0 | 0.0 | 0.0 | 0.0 | 55.0 | 40.0 | 70.0 | 157.1 | 112.8 | 100.0 | 22.2 | 90.0 | 68.8 | 100.0 | mismatch |
| `realcode@027` | `omniauth__omniauth_openid_connect` | Ruby | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 15.0 | 75.0 | 45.5 | 108.0 | 0.0 | 8.6 | 0.0 | 0.0 | 75.0 | missing+mismatch |
| `realcode@028` | `lucascaton__enumerate_it` | Ruby | 0.0 | 0.0 | 0.0 | 0.0 | 40.0 | 40.0 | 60.0 | 15.4 | 32.0 | 66.7 | 22.9 | 107.1 | 75.0 | 100.0 | mismatch |
| `realcode@029` | `asgrim__ofxparser` | PHP | 77.0 | 100.0 | 89.3 | 69.6 | 60.0 | 40.0 | 75.0 | 83.3 | 101.7 | 40.0 | 14.3 | 79.2 | 25.0 | 100.0 | mismatch |
| `realcode@030` | `auth0__passport-auth0` | JavaScript | 84.8 | 100.0 | 100.0 | 64.1 | 25.0 | 25.0 | 35.0 | 85.7 | 67.6 | 100.0 | 20.0 | 73.3 | 6.2 | 100.0 | mismatch |
| `realcode@031` | `final-form__react-final-form-arrays` | TypeScript | 92.5 | 100.0 | 100.0 | 88.9 | 20.0 | 20.0 | 60.0 | 60.0 | 83.0 | 0.0 | 100.0 | 70.4 | 13.3 | 93.8 | mismatch |
| `realcode@032` | `cashapp__turbine` | Kotlin | 100.0 | 100.0 | 100.0 | 100.0 | 30.0 | 20.0 | 45.0 | 77.8 | 56.4 | 14.3 | 4.5 | 84.6 | 21.4 | 87.5 | — |
| `realcode@033` | `bmw-tech__lumberdash` | Dart | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 25.0 | 70.0 | 6.8 | 14.0 | 0.0 | 0.0 | 54.5 | 28.6 | 87.5 | missing+mismatch |
| `realcode@034` | `mjrussell__redux-auth-wrapper` | JavaScript | 81.8 | 90.0 | 90.0 | 69.2 | 30.0 | 10.0 | 70.0 | 25.9 | 72.4 | 0.0 | 0.0 | 60.0 | 0.0 | 100.0 | mismatch |
| `realcode@035` | `martinkr__next-export-i18n` | TypeScript | 16.0 | 22.6 | 22.6 | 5.3 | 50.0 | 15.0 | 70.0 | 57.1 | 87.4 | 100.0 | 100.0 | 45.0 | 6.2 | 100.0 | mismatch |
| `realcode@036` | `rails__webpacker` | Ruby | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 40.0 | 70.0 | 10.0 | 33.4 | 10.0 | 32.3 | 55.6 | 56.2 | 100.0 | missing+mismatch |
| `realcode@037` | `leoafarias__fvm` | Dart | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 | 10.0 | 40.0 | 11.1 | 103.6 | 11.1 | 4.9 | 66.7 | 50.0 | 100.0 | missing+mismatch |
| `realcode@038` | `nelmio__NelmioCorsBundle` | PHP | 0.0 | 0.0 | 0.0 | 0.0 | 40.0 | 15.0 | 75.0 | 33.3 | 70.5 | 0.0 | 0.0 | 47.8 | 0.0 | 100.0 | missing+mismatch |
| `realcode@039` | `dtolnay__indoc` | Rust | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 | 25.0 | 70.0 | 12.5 | 52.2 | 0.0 | 14.3 | 58.8 | 12.5 | 100.0 | missing+mismatch |
| `realcode@040` | `jaebradley__uber-cli` | JavaScript | 59.3 | 100.0 | 100.0 | 55.6 | 30.0 | 10.0 | 72.0 | 35.3 | 57.0 | 0.0 | 6.5 | 47.6 | 12.5 | 100.0 | mismatch |
| `realcode@041` | `jazzband__django-rest-knox` | Python | 65.0 | 100.0 | 72.4 | 45.5 | 65.0 | 15.0 | 80.0 | 21.4 | 58.1 | 0.0 | 10.7 | 82.8 | 37.5 | 100.0 | mismatch |
| `realcode@042` | `cobrateam__django-htmlmin` | Python | 92.9 | 100.0 | 97.9 | 86.5 | 60.0 | 20.0 | 80.0 | 13.1 | 64.9 | 0.0 | 25.0 | 84.8 | 12.5 | 100.0 | mismatch |
| `realcode@043` | `googlemaps__android-maps-ktx` | Kotlin | 56.9 | 62.2 | 62.2 | 54.2 | 50.0 | 15.0 | 45.0 | 47.6 | 79.4 | 100.0 | 0.0 | 14.9 | 0.0 | 100.0 | mismatch |
| `realcode@044` | `fastify__aws-lambda-fastify` | JavaScript | 84.4 | 97.3 | 97.3 | 66.7 | 55.0 | 55.0 | 70.0 | 128.6 | 78.2 | 100.0 | 17.6 | 52.3 | 0.0 | 100.0 | mismatch |
| `realcode@045` | `mike-engel__jwt-cli` | Rust | 75.0 | 100.0 | 87.5 | 66.7 | 40.0 | 20.0 | 70.0 | 183.3 | 104.4 | 0.0 | 3.3 | 52.4 | 25.0 | 75.0 | mismatch |
| `realcode@046` | `davidgilbertson__react-recollect` | TypeScript | 88.0 | 100.0 | 94.1 | 84.8 | 5.0 | 2.0 | 78.0 | 25.0 | 36.8 | 0.0 | 0.0 | 68.2 | 6.2 | 100.0 | mismatch |
| `realcode@047` | `globocom__megadraft` | JavaScript | 90.6 | 100.0 | 93.3 | 88.2 | 15.0 | 5.0 | 50.0 | 32.1 | 32.5 | 0.0 | 7.7 | 65.0 | 45.5 | 68.8 | mismatch |
| `realcode@048` | `malept__thermite` | Ruby | 65.4 | 100.0 | 67.6 | 60.0 | 40.0 | 15.0 | 45.0 | 47.4 | 40.1 | 22.2 | 0.0 | 81.8 | 25.0 | 100.0 | mismatch |
| `realcode@049` | `mrmckeb__typescript-plugin-css-modules` | TypeScript | 15.1 | 20.0 | 8.7 | 21.3 | 25.0 | 5.0 | 70.0 | 27.8 | 88.8 | 0.0 | 1.4 | 44.0 | 25.0 | 100.0 | missing+mismatch |
| `realcode@050` | `django-cache-machine__django-cache-machine` | Python | 83.9 | 100.0 | 100.0 | 50.0 | 50.0 | 5.0 | 75.0 | 89.5 | 103.1 | 0.0 | 19.6 | 68.6 | 18.8 | 100.0 | partial missing |

## Averages

Mean of each per-repo value over the repos that have one (`n`). Repos with errors: 46/50  |  model-side failures scored 0% (in denominator): 0  |  infra failures excluded (retest-eligible): 0.

| Group | Metric | Mean | n | missing (reason) |
| --- | --- | --- | --- | --- |
| Test Cases Pass Rate | Overall | 48.0 | 50 | 0 |
|  | Public | 56.2 | 50 | 0 |
|  | Native | 52.5 | 50 | 0 |
|  | Enhanced | 44.7 | 50 | 0 |
| Agentic Evaluation | Semantic Sim | 37.4 | 50 | 0 |
|  | API Sim | 20.3 | 50 | 0 |
|  | Design Quality | 63.0 | 50 | 0 |
| Structural Assessment | File Count % | 255.5 | 50 | 0 |
|  | LOC % | 1328.4 | 50 | 0 |
|  | Class Sim | 36.6 | 50 | 0 |
|  | Method Sim | 19.9 | 50 | 0 |
| Interaction Quality | Constraint Cov | 68.6 | 50 | 0 |
|  | Fallback Rate | 26.8 | 50 | 0 |
|  | Budget Usage | 90.9 | 50 | 0 |
