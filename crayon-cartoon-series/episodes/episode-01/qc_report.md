# QC report: Episode 1 - Why Can't We Just Print More Money?

Result: **31 pass, 1 warnings, 0 failures**

| Status | Check | Detail |
|---|---|---|
| PASS | resolution | 1080x1920 |
| PASS | frame rate | 30/1 |
| PASS | codecs | h264 + aac |
| PASS | runtime | 56.80s (target 55-62s) |
| PASS | frame count | 1704 frames |
| PASS | audio/video length match | audio 56.79s |
| PASS | integrated loudness | -14.8 LUFS (target -14) |
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
| PASS | S7 animation energy | 14.07 mean abs frame diff @4fps |
| WARN | text outside Shorts safe area | "MONEYPRINTER" @ 46.6-48.1s |
| PASS | S1 speech intelligibility (ASR of final mix) | 94% word match |
| PASS | S2 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S3 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S4 speech intelligibility (ASR of final mix) | 90% word match |
| PASS | S5 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S6 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S7 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | captions cover all spoken words | 115/115 words |
| PASS | retention cadence (new development <= 8 s) | longest gap 4.4s (23.6-28.0s); 47 developments in 57s |
| PASS | scene count / hooks | 7 scenes, each with a declared retention hook |
| PASS | characters only via the cast library | no inline person() calls in scene source |
| PASS | no slideshow / still-image scenes | all scenes are vector keyframe animation (no raster images used) |
