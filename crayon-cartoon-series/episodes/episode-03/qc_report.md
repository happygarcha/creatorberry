# QC report: Episode 3 - Why Did Outlook Go Down Worldwide?

Result: **49 pass, 1 warnings, 0 failures**

| Status | Check | Detail |
|---|---|---|
| PASS | resolution | 1080x1920 |
| PASS | frame rate | 30/1 |
| PASS | codecs | h264 + aac |
| PASS | runtime within the 3-minute Shorts limit | 163.33s (content is never cut to hit 90-180s) |
| PASS | frame count | 4900 frames |
| PASS | audio/video length match | audio 163.33s |
| PASS | integrated loudness | -14.4 LUFS (target -14) |
| PASS | true peak | -1.3 dBFS |
| PASS | unintended silent gaps (>0.35s) | none |
| PASS | intentional silences | none |
| PASS | blank frames | none |
| PASS | motion (no scene frozen >1.5s) | every scene moves |
| PASS | S1 animation energy | 1.42 mean abs frame diff @4fps |
| PASS | S2 animation energy | 2.33 mean abs frame diff @4fps |
| PASS | S3 animation energy | 1.99 mean abs frame diff @4fps |
| PASS | S4 animation energy | 3.38 mean abs frame diff @4fps |
| PASS | S5 animation energy | 3.38 mean abs frame diff @4fps |
| PASS | S6 animation energy | 2.83 mean abs frame diff @4fps |
| PASS | S7 animation energy | 3.18 mean abs frame diff @4fps |
| PASS | S8 animation energy | 2.32 mean abs frame diff @4fps |
| PASS | S9 animation energy | 2.78 mean abs frame diff @4fps |
| PASS | S10 animation energy | 3.05 mean abs frame diff @4fps |
| PASS | S11 animation energy | 2.38 mean abs frame diff @4fps |
| PASS | ENDCARD animation energy | 6.25 mean abs frame diff @4fps |
| WARN | text outside Shorts safe area | "TEAMS TRAFFIC" @ 83.6-83.6s |
| PASS | S1 speech intelligibility (ASR of final mix) | 95% word match |
| PASS | S2 speech intelligibility (ASR of final mix) | 86% word match |
| PASS | S3 speech intelligibility (ASR of final mix) | 88% word match |
| PASS | S4 speech intelligibility (ASR of final mix) | 98% word match |
| PASS | S5 speech intelligibility (ASR of final mix) | 97% word match |
| PASS | S6 speech intelligibility (ASR of final mix) | 93% word match |
| PASS | S7 speech intelligibility (ASR of final mix) | 91% word match |
| PASS | S8 speech intelligibility (ASR of final mix) | 90% word match |
| PASS | S9 speech intelligibility (ASR of final mix) | 98% word match |
| PASS | S10 speech intelligibility (ASR of final mix) | 100% word match |
| PASS | S11 speech intelligibility (ASR of final mix) | 95% word match |
| PASS | ENDCARD speech intelligibility (ASR of final mix) | 100% word match |
| PASS | speech pace (slow enough to follow facts) | 166 words per minute while speaking (limit 175) |
| PASS | music sits under the voice | voice is 30.3 dB above the music while speaking (min 18) |
| PASS | effects do not mask the voice | voice is 26.0 dB above effects while speaking |
| PASS | captions cover all spoken words | 400/400 words |
| PASS | retention cadence (new development <= 8 s) | longest gap 7.2s (14.9-22.1s); 76 developments in 163s |
| PASS | scene count / hooks | 12 scenes, each with a declared retention hook |
| PASS | ends with the standard end card | ENDCARD |
| PASS | end card length (5-7 s) | 6.0s |
| PASS | spoken invitation to like, share and subscribe | like, share, and subscribe for more crazy explanations! |
| PASS | LIKE / SHARE / SUBSCRIBE shown on screen |  |
| PASS | no next-episode title shown or promised | none found in the video text |
| PASS | characters only via the cast library | no inline person() calls in scene source |
| PASS | no slideshow / still-image scenes | all scenes are vector keyframe animation (no raster images used) |
