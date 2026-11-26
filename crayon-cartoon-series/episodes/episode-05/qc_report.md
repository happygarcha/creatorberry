# QC report: Episode 5 - Never Drink AC Water

Result: **38 pass, 2 warnings, 0 failures**

| Status | Check | Detail |
|---|---|---|
| PASS | resolution | 1080x1920 |
| PASS | frame rate | 30/1 |
| PASS | codecs | h264 + aac |
| PASS | runtime within the 3-minute Shorts limit | 107.63s (content is never cut to hit 60-180s) |
| PASS | frame count | 3229 frames |
| PASS | audio/video length match | audio 107.63s |
| PASS | integrated loudness | -14.2 LUFS (target -14) |
| PASS | true peak | -1.4 dBFS |
| PASS | unintended silent gaps (>0.35s) | none |
| PASS | intentional silences | none |
| PASS | blank frames | none |
| PASS | motion (no scene frozen >1.5s) | every scene moves |
| PASS | S1 animation energy | 2.68 mean abs frame diff @4fps |
| PASS | S2 animation energy | 2.09 mean abs frame diff @4fps |
| PASS | S3 animation energy | 2.13 mean abs frame diff @4fps |
| PASS | S4 animation energy | 1.59 mean abs frame diff @4fps |
| PASS | S5 animation energy | 1.84 mean abs frame diff @4fps |
| PASS | S6 animation energy | 4.03 mean abs frame diff @4fps |
| PASS | ENDCARD animation energy | 7.02 mean abs frame diff @4fps |
| PASS | text inside Shorts safe area | all visible text within x 4-94%, y 10-80% (sampled 4 fps) |
| PASS | S1 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S2 speech intelligibility (ASR of final mix) | 98% word match |
| PASS | S3 speech intelligibility (ASR of final mix) | 92% word match |
| PASS | S4 speech intelligibility (ASR of final mix) | 93% word match |
| PASS | S5 speech intelligibility (ASR of final mix) | 96% word match |
| PASS | S6 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | ENDCARD speech intelligibility (ASR of final mix) | 100% word match |
| WARN | speech pace (slow enough to follow facts) | 181 words per minute while speaking (limit 175) |
| PASS | music sits under the voice | voice is 30.8 dB above the music while speaking (min 18) |
| PASS | effects do not mask the voice | voice is 26.3 dB above effects while speaking |
| PASS | captions cover all spoken words | 282/282 words |
| WARN | retention cadence (new development <= 8 s) | longest gap 9.7s (64.3-74.0s); 50 developments in 108s |
| PASS | scene count / hooks | 7 scenes, each with a declared retention hook |
| PASS | ends with the standard end card | ENDCARD |
| PASS | end card length (5-7 s) | 6.0s |
| PASS | spoken invitation to like, share and subscribe | like, share, and subscribe for more crazy explanations! |
| PASS | LIKE / SHARE / SUBSCRIBE shown on screen |  |
| PASS | no next-episode title shown or promised | none found in the video text |
| PASS | characters only via the cast library | no inline person() calls in scene source |
| PASS | no slideshow / still-image scenes | all scenes are vector keyframe animation (no raster images used) |
