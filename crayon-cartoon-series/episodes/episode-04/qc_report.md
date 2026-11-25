# QC report: Episode 4 - Floating AI Data Centers? Panthalassa Explained

Result: **45 pass, 3 warnings, 0 failures**

| Status | Check | Detail |
|---|---|---|
| PASS | resolution | 1080x1920 |
| PASS | frame rate | 30/1 |
| PASS | codecs | h264 + aac |
| PASS | runtime within the 3-minute Shorts limit | 178.10s (content is never cut to hit 90-180s) |
| PASS | frame count | 5343 frames |
| PASS | audio/video length match | audio 178.09s |
| PASS | integrated loudness | -14.3 LUFS (target -14) |
| PASS | true peak | -1.1 dBFS |
| PASS | unintended silent gaps (>0.35s) | none |
| PASS | intentional silences | none |
| PASS | blank frames | none |
| PASS | motion (no scene frozen >1.5s) | every scene moves |
| PASS | S1 animation energy | 2.22 mean abs frame diff @4fps |
| PASS | S2 animation energy | 2.60 mean abs frame diff @4fps |
| PASS | S3 animation energy | 3.05 mean abs frame diff @4fps |
| PASS | S4 animation energy | 3.45 mean abs frame diff @4fps |
| PASS | S5 animation energy | 3.34 mean abs frame diff @4fps |
| PASS | S6 animation energy | 2.95 mean abs frame diff @4fps |
| PASS | S7 animation energy | 3.25 mean abs frame diff @4fps |
| PASS | S8 animation energy | 1.94 mean abs frame diff @4fps |
| PASS | S9 animation energy | 1.67 mean abs frame diff @4fps |
| PASS | S10 animation energy | 5.13 mean abs frame diff @4fps |
| PASS | ENDCARD animation energy | 6.24 mean abs frame diff @4fps |
| PASS | text inside Shorts safe area | all visible text within x 4-94%, y 10-80% (sampled 4 fps) |
| PASS | S1 speech intelligibility (ASR of final mix) | 85% word match |
| PASS | S2 speech intelligibility (ASR of final mix) | 98% word match |
| PASS | S3 speech intelligibility (ASR of final mix) | 89% word match |
| PASS | S4 speech intelligibility (ASR of final mix) | 94% word match |
| PASS | S5 speech intelligibility (ASR of final mix) | 97% word match |
| PASS | S6 speech intelligibility (ASR of final mix) | 94% word match |
| WARN | S7 speech intelligibility (ASR of final mix) | 76% word match |
| PASS | S8 speech intelligibility (ASR of final mix) | 85% word match |
| PASS | S9 speech intelligibility (ASR of final mix) | 97% word match |
| PASS | S10 speech intelligibility (ASR of final mix) | 98% word match |
| PASS | ENDCARD speech intelligibility (ASR of final mix) | 100% word match |
| WARN | speech pace (slow enough to follow facts) | 177 words per minute while speaking (limit 175) |
| PASS | music sits under the voice | voice is 30.4 dB above the music while speaking (min 18) |
| PASS | effects do not mask the voice | voice is 25.9 dB above effects while speaking |
| PASS | captions cover all spoken words | 465/465 words |
| WARN | retention cadence (new development <= 8 s) | longest gap 10.4s (157.3-167.7s); 82 developments in 178s |
| PASS | scene count / hooks | 11 scenes, each with a declared retention hook |
| PASS | ends with the standard end card | ENDCARD |
| PASS | end card length (5-7 s) | 6.0s |
| PASS | spoken invitation to like, share and subscribe | like, share, and subscribe for more crazy explanations! |
| PASS | LIKE / SHARE / SUBSCRIBE shown on screen |  |
| PASS | no next-episode title shown or promised | none found in the video text |
| PASS | characters only via the cast library | no inline person() calls in scene source |
| PASS | no slideshow / still-image scenes | all scenes are vector keyframe animation (no raster images used) |
