# QC report: Episode 1 - Why Can't We Just Print More Money?

Result: **33 pass, 1 warnings, 0 failures**

| Status | Check | Detail |
|---|---|---|
| PASS | resolution | 1080x1920 |
| PASS | frame rate | 30/1 |
| PASS | codecs | h264 + aac |
| PASS | runtime | 59.70s (target 55-62s) |
| PASS | frame count | 1791 frames |
| PASS | audio/video length match | audio 59.69s |
| PASS | integrated loudness | -14.7 LUFS (target -14) |
| PASS | true peak | -1.4 dBFS |
| PASS | unintended silent gaps (>0.35s) | none |
| PASS | intentional silences | 10.5s |
| PASS | blank frames | none |
| PASS | motion (no scene frozen >1.5s) | every scene moves |
| PASS | S1 animation energy | 2.03 mean abs frame diff @4fps |
| PASS | S2 animation energy | 8.00 mean abs frame diff @4fps |
| PASS | S3 animation energy | 3.52 mean abs frame diff @4fps |
| PASS | S4 animation energy | 6.86 mean abs frame diff @4fps |
| PASS | S5 animation energy | 4.63 mean abs frame diff @4fps |
| PASS | S6 animation energy | 9.55 mean abs frame diff @4fps |
| PASS | S7 animation energy | 14.53 mean abs frame diff @4fps |
| PASS | S8 animation energy | 9.86 mean abs frame diff @4fps |
| WARN | text outside Shorts safe area | "MONEYPRINTER" @ 46.6-48.1s |
| PASS | S1 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S2 speech intelligibility (ASR of final mix) | 92% word match |
| PASS | S3 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S4 speech intelligibility (ASR of final mix) | 95% word match |
| PASS | S5 speech intelligibility (ASR of final mix) | 95% word match |
| PASS | S6 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S7 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S8 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | captions cover all spoken words | 121/121 words |
| PASS | retention cadence (new development <= 8 s) | longest gap 4.4s (23.6-28.0s); 51 developments in 60s |
| PASS | scene count / hooks | 8 scenes, each with a declared retention hook |
| PASS | characters only via the cast library | no inline person() calls in scene source |
| PASS | no slideshow / still-image scenes | all scenes are vector keyframe animation (no raster images used) |
