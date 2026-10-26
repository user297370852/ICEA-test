# ICAE-Bench — Per-Repo Results (GLM-5.3-Flash)

- **append_id**: `3992f153f5bf4d0aa80a27105e752e67`
- **Tested model**: GLM-5.3-Flash  |  **User model**: DeepSeek-V3.2  |  **Critic**: GLM-5.3-Flash
- **env_mode**: base  |  **prd_type**: fuzzy  |  **eval_mode**: lite  |  **query_count**: 16
- **repos evaluated**: 50
- **wall-clock**: 342.2 min (20533s)  |  **gen/repo**: mean 2460s, min 834s, max 20418s  |  **concurrency**: 4
- **finished_at**: 2026-10-26 04:24:14

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
| `realcode@001` | `dependents__node-dependency-tree` | JavaScript | 91.4 | 100.0 | 100.0 | 87.5 | 50.0 | 40.0 | 75.0 | 18.8 | 120.8 | 100.0 | 27.3 | 65.4 | 20.0 | 62.5 | mismatch |
| `realcode@002` | `developit__unfetch` | JavaScript | 97.4 | 100.0 | 100.0 | 94.4 | 20.0 | 20.0 | 55.0 | 77.8 | 173.7 | 100.0 | 75.0 | 58.3 | 25.0 | 75.0 | mismatch |
| `realcode@003` | `mperham__connection_pool` | Ruby | 88.5 | 100.0 | 100.0 | 83.3 | 70.0 | 45.0 | 55.0 | 25.0 | 82.7 | 66.7 | 42.9 | 0.0 | 0.0 | 43.8 | mismatch |
| `realcode@004` | `planetscale__fast_page` | Ruby | 45.8 | 100.0 | 88.9 | 20.0 | 45.0 | 15.0 | 65.0 | 100.0 | 178.1 | 0.0 | 0.0 | 25.0 | 25.0 | 75.0 | mismatch |
| `realcode@005` | `bmentges__django-cart` | Python | 4.4 | 16.7 | 16.7 | 2.6 | 55.0 | 30.0 | 80.0 | 100.0 | 63.1 | 12.5 | 16.0 | 55.6 | 0.0 | 87.5 | partial missing |
| `realcode@006` | `marp-team__marp-vscode` | TypeScript | 93.5 | 100.0 | 100.0 | 90.0 | 45.0 | 55.0 | 45.0 | 75.0 | 119.0 | 100.0 | 21.4 | 109.1 | 66.7 | 75.0 | mismatch |
| `realcode@007` | `balena-io-modules__drivelist` | C++ | 96.4 | 88.9 | 93.3 | 97.5 | 10.0 | 5.0 | 65.0 | 45.5 | 126.4 | 100.0 | 100.0 | 0.0 | 0.0 | 18.8 | mismatch |
| `realcode@008` | `danistefanovic__hooka` | JavaScript | 0.8 | 0.0 | 0.0 | 1.6 | 45.0 | 30.0 | 60.0 | 39.3 | 85.3 | 100.0 | 10.9 | 71.4 | 61.5 | 81.2 | missing+mismatch |
| `realcode@009` | `dwyl__flutter-todo-list-tutorial` | Dart | 100.0 | 100.0 | 100.0 | 100.0 | 30.0 | 20.0 | 70.0 | 13.0 | 51.0 | 0.0 | 9.1 | 54.5 | 20.0 | 62.5 | — |
| `realcode@010` | `microsoft__DacFx` | C# | 95.2 | 100.0 | 100.0 | 91.7 | 60.0 | 50.0 | 70.0 | 36.4 | 140.7 | 100.0 | 100.0 | 82.4 | 33.3 | 75.0 | mismatch |
| `realcode@011` | `nunomaduro__laravel-mojito` | PHP | 98.5 | 100.0 | 100.0 | 96.9 | 25.0 | 0.0 | 50.0 | 5.0 | 110.6 | 0.0 | 7.1 | 54.5 | 25.0 | 100.0 | mismatch |
| `realcode@012` | `Treblle__treblle-laravel` | PHP | 100.0 | 100.0 | 100.0 | 100.0 | 20.0 | 25.0 | 40.0 | 70.0 | 38.2 | 40.0 | 20.0 | 61.5 | 35.7 | 87.5 | — |
| `realcode@013` | `aboutyou__dart_packages` | Dart | 100.0 | 100.0 | 100.0 | 100.0 | 5.0 | 5.0 | 60.0 | 30.0 | 59.3 | 6.7 | 0.0 | 62.5 | 25.0 | 100.0 | — |
| `realcode@014` | `ankane__distribute_reads` | Ruby | 96.8 | 100.0 | 92.9 | 100.0 | 50.0 | 20.0 | 35.0 | 9.1 | 48.2 | 12.5 | 0.0 | 38.5 | 0.0 | 100.0 | mismatch |
| `realcode@015` | `esanchezm__prometheus-qbittorrent-exporter` | Python | 88.6 | 100.0 | 100.0 | 84.0 | 45.0 | 15.0 | 80.0 | 300.0 | 86.4 | 0.0 | 7.1 | 96.0 | 18.2 | 68.8 | mismatch |
| `realcode@016` | `gemini-testing__looks-same` | JavaScript | 19.0 | 21.1 | 9.8 | 36.4 | 45.0 | 15.0 | 72.0 | 200.0 | 194.6 | 100.0 | 9.1 | 50.0 | 18.8 | 100.0 | mismatch |
| `realcode@017` | `justintaddei__v-wave` | TypeScript | 97.8 | 100.0 | 100.0 | 96.7 | 20.0 | 10.0 | 45.0 | 10.0 | 49.2 | 0.0 | 7.0 | 54.5 | 12.5 | 100.0 | mismatch |
| `realcode@018` | `atom__etch` | JavaScript | 91.1 | 100.0 | 93.8 | 90.0 | 10.0 | 10.0 | 40.0 | 31.2 | 127.2 | 0.0 | 13.0 | 93.1 | 0.0 | 100.0 | mismatch |
| `realcode@019` | `doctrine__deprecations` | PHP | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 20.0 | 75.0 | 271.4 | 143.6 | 20.0 | 4.5 | 82.8 | 0.0 | 100.0 | no output |
| `realcode@020` | `shelljs__shx` | JavaScript | 85.5 | 97.0 | 88.6 | 83.3 | 25.0 | 15.0 | 55.0 | 262.5 | 212.2 | 100.0 | 12.5 | 84.6 | 37.5 | 100.0 | mismatch |
| `realcode@021` | `donovanglover__hyprnome` | Rust | 100.0 | 100.0 | 100.0 | 100.0 | 50.0 | 20.0 | 80.0 | 33.3 | 115.0 | 0.0 | 7.7 | 84.0 | 38.5 | 81.2 | — |
| `realcode@022` | `jonbern__fetch-retry` | JavaScript | 87.0 | 92.3 | 90.9 | 83.3 | 60.0 | 30.0 | 75.0 | 150.0 | 64.8 | 100.0 | 50.0 | 81.8 | 45.5 | 68.8 | mismatch |
| `realcode@023` | `asakusarb__action_args` | Ruby | 100.0 | 100.0 | 100.0 | 100.0 | 30.0 | 10.0 | 65.0 | 27.3 | 33.1 | 0.0 | 0.0 | 75.0 | 15.4 | 81.2 | — |
| `realcode@024` | `patsplat__plist` | Ruby | 83.9 | 100.0 | 93.9 | 69.6 | 45.0 | 20.0 | 40.0 | 8.3 | 39.4 | 0.0 | 0.0 | 55.2 | 12.5 | 100.0 | mismatch |
| `realcode@025` | `dart-archive__ffi` | Dart | 50.9 | 100.0 | 48.5 | 54.5 | 20.0 | 15.0 | 55.0 | 100.0 | 123.1 | 60.0 | 16.7 | 75.0 | 6.2 | 100.0 | mismatch |
| `realcode@026` | `xnimorz__use-debounce` | TypeScript | 98.4 | 100.0 | 100.0 | 97.2 | 45.0 | 10.0 | 80.0 | 100.0 | 90.3 | 100.0 | 5.6 | 80.0 | 83.3 | 75.0 | mismatch |
| `realcode@027` | `omniauth__omniauth_openid_connect` | Ruby | 52.5 | 75.0 | 56.5 | 50.0 | 45.0 | 5.0 | 35.0 | 9.1 | 36.1 | 0.0 | 0.0 | 81.0 | 25.0 | 100.0 | mismatch |
| `realcode@028` | `lucascaton__enumerate_it` | Ruby | 75.7 | 86.5 | 67.9 | 83.1 | 35.0 | 35.0 | 55.0 | 7.7 | 21.5 | 66.7 | 17.1 | 57.1 | 25.0 | 100.0 | mismatch |
| `realcode@029` | `asgrim__ofxparser` | PHP | 73.0 | 100.0 | 89.3 | 63.0 | 50.0 | 30.0 | 75.0 | 175.0 | 170.0 | 30.0 | 19.1 | 79.2 | 31.2 | 100.0 | mismatch |
| `realcode@030` | `auth0__passport-auth0` | JavaScript | 85.9 | 100.0 | 100.0 | 66.7 | 35.0 | 10.0 | 70.0 | 128.6 | 87.5 | 100.0 | 25.0 | 68.9 | 18.8 | 100.0 | mismatch |
| `realcode@031` | `final-form__react-final-form-arrays` | TypeScript | 97.0 | 100.0 | 100.0 | 95.6 | 25.0 | 15.0 | 70.0 | 70.0 | 106.6 | 0.0 | 100.0 | 70.4 | 18.8 | 100.0 | mismatch |
| `realcode@032` | `cashapp__turbine` | Kotlin | 0.0 | 0.0 | 0.0 | 0.0 | 35.0 | 10.0 | 65.0 | 44.4 | 66.7 | 14.3 | 0.0 | 80.8 | 35.7 | 87.5 | no output |
| `realcode@033` | `bmw-tech__lumberdash` | Dart | 97.1 | 100.0 | 100.0 | 95.5 | 45.0 | 15.0 | 85.0 | 15.9 | 24.9 | 0.0 | 0.0 | 72.7 | 12.5 | 50.0 | mismatch |
| `realcode@034` | `mjrussell__redux-auth-wrapper` | JavaScript | 93.9 | 100.0 | 100.0 | 84.6 | 30.0 | 15.0 | 70.0 | 33.3 | 110.4 | 0.0 | 11.8 | 0.0 | 0.0 | 75.0 | mismatch |
| `realcode@035` | `martinkr__next-export-i18n` | TypeScript | 64.0 | 67.7 | 67.7 | 57.9 | 60.0 | 15.0 | 70.0 | 9.5 | 50.0 | 100.0 | 100.0 | 45.0 | 6.2 | 100.0 | mismatch |
| `realcode@036` | `rails__webpacker` | Ruby | 83.7 | 88.9 | 92.3 | 80.0 | 50.0 | 35.0 | 70.0 | 15.0 | 39.9 | 20.0 | 25.8 | 88.9 | 55.6 | 56.2 | mismatch |
| `realcode@037` | `leoafarias__fvm` | Dart | 80.4 | 100.0 | 94.7 | 71.9 | 20.0 | 10.0 | 30.0 | 7.4 | 13.5 | 0.0 | 0.0 | 50.0 | 53.3 | 93.8 | mismatch |
| `realcode@038` | `nelmio__NelmioCorsBundle` | PHP | 73.1 | 100.0 | 100.0 | 22.2 | 30.0 | 5.0 | 65.0 | 46.7 | 54.7 | 0.0 | 0.0 | 47.8 | 6.2 | 100.0 | mismatch |
| `realcode@039` | `dtolnay__indoc` | Rust | 82.6 | 75.0 | 83.3 | 82.4 | 25.0 | 15.0 | 60.0 | 12.5 | 53.6 | 0.0 | 10.7 | 35.3 | 6.2 | 100.0 | mismatch |
| `realcode@040` | `jaebradley__uber-cli` | JavaScript | 54.2 | 100.0 | 100.0 | 50.0 | 45.0 | 10.0 | 70.0 | 35.3 | 39.9 | 4.8 | 6.5 | 33.3 | 0.0 | 100.0 | mismatch |
| `realcode@041` | `jazzband__django-rest-knox` | Python | 12.5 | 100.0 | 13.8 | 9.1 | 60.0 | 5.0 | 80.0 | 42.9 | 50.0 | 0.0 | 7.1 | 0.0 | 0.0 | 93.8 | missing+mismatch |
| `realcode@042` | `cobrateam__django-htmlmin` | Python | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 30.0 | 72.0 | 8.2 | 36.8 | 100.0 | 33.3 | 81.8 | 0.0 | 68.8 | runtime err |
| `realcode@043` | `googlemaps__android-maps-ktx` | Kotlin | 100.0 | 100.0 | 100.0 | 100.0 | 30.0 | 15.0 | 60.0 | 61.9 | 113.1 | 100.0 | 0.0 | 53.2 | 0.0 | 100.0 | — |
| `realcode@044` | `fastify__aws-lambda-fastify` | JavaScript | 76.6 | 94.6 | 94.6 | 51.9 | 45.0 | 55.0 | 60.0 | 42.9 | 45.1 | 100.0 | 14.7 | 56.8 | 25.0 | 100.0 | mismatch |
| `realcode@045` | `mike-engel__jwt-cli` | Rust | 0.0 | 0.0 | 0.0 | 0.0 | 55.0 | 50.0 | 65.0 | 183.3 | 112.7 | 0.0 | 13.3 | 47.6 | 25.0 | 100.0 | no output |
| `realcode@046` | `davidgilbertson__react-recollect` | TypeScript | 88.0 | 100.0 | 100.0 | 81.8 | 30.0 | 10.0 | 70.0 | 17.9 | 29.3 | 0.0 | 0.0 | 45.5 | 0.0 | 93.8 | mismatch |
| `realcode@047` | `globocom__megadraft` | JavaScript | 87.5 | 100.0 | 93.3 | 82.4 | 15.0 | 5.0 | 65.0 | 32.1 | 32.8 | 0.0 | 3.9 | 55.0 | 7.7 | 81.2 | mismatch |
| `realcode@048` | `malept__thermite` | Ruby | 67.3 | 100.0 | 70.3 | 60.0 | 30.0 | 10.0 | 45.0 | 5.3 | 35.1 | 11.1 | 0.0 | 75.8 | 0.0 | 100.0 | mismatch |
| `realcode@049` | `mrmckeb__typescript-plugin-css-modules` | TypeScript | 37.6 | 75.0 | 41.3 | 34.0 | 20.0 | 10.0 | 55.0 | 33.3 | 90.2 | 0.0 | 0.0 | 72.0 | 25.0 | 100.0 | mismatch |
| `realcode@050` | `django-cache-machine__django-cache-machine` | Python | 83.9 | 100.0 | 100.0 | 50.0 | 70.0 | 30.0 | 75.0 | 63.2 | 113.0 | 0.0 | 23.5 | 60.0 | 7.1 | 87.5 | mismatch |

## Averages

Mean of each per-repo value over the repos that have one (`n`). Repos with errors: 44/50  |  model-side failures scored 0% (in denominator): 0  |  infra failures excluded (retest-eligible): 0.

| Group | Metric | Mean | n | missing (reason) |
| --- | --- | --- | --- | --- |
| Test Cases Pass Rate | Overall | 71.6 | 50 | 0 |
|  | Public | 83.6 | 50 | 0 |
|  | Native | 77.6 | 50 | 0 |
|  | Enhanced | 66.6 | 50 | 0 |
| Agentic Evaluation | Semantic Sim | 38.2 | 50 | 0 |
|  | API Sim | 19.9 | 50 | 0 |
|  | Design Quality | 62.5 | 50 | 0 |
| Structural Assessment | File Count % | 64.8 | 50 | 0 |
|  | LOC % | 84.2 | 50 | 0 |
|  | Class Sim | 37.3 | 50 | 0 |
|  | Method Sim | 19.5 | 50 | 0 |
| Interaction Quality | Constraint Cov | 60.2 | 50 | 0 |
|  | Fallback Rate | 20.2 | 50 | 0 |
|  | Budget Usage | 86.1 | 50 | 0 |
