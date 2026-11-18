# Zapzapper Dark Files, 60-second animation test: QC report

Checked on the rendered MP4 `final/Zapzapper_DarkFiles_60sec_Test.mp4` (ffprobe, ffmpeg frame analysis, Whisper round trip on the MP4's own audio, rig contact residuals).

| Status | Check | Result |
|---|---|---|
| PASS | file exists | final/Zapzapper_DarkFiles_60sec_Test.mp4 (16.9 MB) |
| PASS | duration | container 60.000 s, video 60.000 s, audio 60.000 s |
| PASS | resolution | 1920x1080, SAR 1:1, DAR 16:9 |
| PASS | frame rate / frames | 30/1 fps, 1800 frames |
| PASS | codecs | h264 + aac 48000 Hz 2 ch |
| PASS | blank / broken frames | black segments [(0.0, 0.1), (59.9, 59.9667)] (only the 0.3 s fade-in and the final cut to black are expected) |
| PASS | hard cut to black at the end | mean luma at 59.5 s = 30.7, at 59.95 s = 1.0 |
| PASS | S1 (0-7s) motion | mean frame-to-frame change 4.02, 10th percentile 2.63 (0 = frozen) |
| PASS | S2 (7-15s) motion | mean frame-to-frame change 5.31, 10th percentile 3.21 (0 = frozen) |
| PASS | S3 (15-23s) motion | mean frame-to-frame change 4.53, 10th percentile 0.97 (0 = frozen) |
| PASS | S4 (23-32s) motion | mean frame-to-frame change 4.50, 10th percentile 1.46 (0 = frozen) |
| PASS | S5 (32-41s) motion | mean frame-to-frame change 4.24, 10th percentile 1.76 (0 = frozen) |
| PASS | S6 (41-51s) motion | mean frame-to-frame change 4.99, 10th percentile 3.30 (0 = frozen) |
| PASS | S7 (51-60s) motion | mean frame-to-frame change 5.26, 10th percentile 1.01 (0 = frozen) |
| PASS | n1a NARRATOR intelligibility (ASR of the MP4's audio) | 100% word match; heard: "The abandoned Miller House had stood empty for years." |
| PASS | n1b NARRATOR intelligibility (ASR of the MP4's audio) | 100% word match; heard: "But something in its basement didn't belong." |
| PASS | r1 REED intelligibility (ASR of the MP4's audio) | 100% word match; heard: "Why would someone bolt an empty shelf to the floor?" |
| PASS | m1 MORGAN intelligibility (ASR of the MP4's audio) | 100% word match; heard: "Daniel look at this." |
| PASS | n2 NARRATOR intelligibility (ASR of the MP4's audio) | 100% word match; heard: "Behind the shelving unit was a door that appeared on none of the surviving floor plans." |
| PASS | m2 MORGAN intelligibility (ASR of the MP4's audio) | 100% word match; heard: "There's another room." |
| PASS | r2 REED intelligibility (ASR of the MP4's audio) | 100% word match; heard: "Someone's been using this place." |
| PASS | n3 NARRATOR intelligibility (ASR of the MP4's audio) | 100% word match; heard: "And on the desk, they found something unexpected." |
| WARN | g1 LILY intelligibility (ASR of the MP4's audio) | 67% word match; heard: "Mom is me." |
| WARN | speech pace | 187 words per minute while speaking (limit 175); voices at natural speed 1.0, nothing accelerated |
| PASS | dialogue over music | voice is 19.3 dB above the music while speaking; 14.9 dB above music+SFX together |
| PASS | captions | 9 caption cues, none overlapping, each shown from its sentence start (aligned to the measured clip durations) |
| PASS | hand contact: Reed -> bolt wrench | max residual 0.0 px over 33 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |
| PASS | hand contact: Morgan -> bolt wrench | max residual 0.0 px over 33 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |
| PASS | hand contact: Reed -> shelf (push) | max residual 0.0 px over 69 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |
| PASS | hand contact: Morgan -> shelf (push) | max residual 0.0 px over 66 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |
| PASS | hand contact: Reed -> door handle / door | max residual 0.0 px over 145 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |
| PASS | hand contact: Reed -> recorder | max residual 0.0 px over 109 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |
| PASS | hand contact: Reed -> bolt tap | max residual 0.0 px over 82 frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius) |

## What works
- Exactly 60.000 s, 1920x1080, 30 fps (1,800 frames), H.264 + AAC. Fade-in 0.3 s, hard cut to black at 59.9 s.
- Seven shots with distinct camera angles and hard cuts at 7/15/23/32/41/51/56 s. Real rig animation: alternating-leg walk cycles with planted feet, IK arms, crouch/stand, head turns and looks, blinking, three mouth shapes driven by the real audio envelope, body turns, a ratchet wrench turning bolts that rise out and fall, a shelf that slides while both characters push with hands on it, a handle that rotates and a door that swings on its hinges, dust motes in the beams, recorder picked up, thumb press, screen lit, waveform from the girl's audio.
- Hands stay on objects: measured residual 0 px between requested contact point and IK hand for every contact (tools, shelf, handle/door, recorder).
- Locked designs: Reed (glasses, brown coat, dark trousers), Morgan (short dark hair, muted blue jacket, dark trousers), same rig parts all shot long.
- Voices: free local Kokoro TTS, natural speed 1.0, four distinct voices (Narrator, Reed, Morgan, Lily). Dialogue sits 19 dB above the music; music stops dead at 54.95 s before the girl speaks.

## What remains imperfect (honest list)
- **Logo:** no Zapzapper logo asset exists in the repo or filesystem, so it was NOT drawn or invented and is omitted. Please supply the original file.
- **Remotion** is not installed; the existing project SVG/Chromium engine was used instead (allowed by the brief).
- **Speech pace** measures 187 words/min on spoken seconds (series limit 175). Voices were kept at natural speed 1.0 on purpose (slowing sounded sloppy); the only extra pause added is 1.0 s between the two narrator sentences.
- **Lily's voice** is deliberately thin and degraded, so Whisper hears "Mom is me" (it drops "it's"); a human can hear "it's". Raw TTS was recognised 100%.
- **TTS is not human quality**; it is synthetic and sounds like it.
- Characters are front-facing stick-style (series look) so "walking" is a scissor stride with planted feet, not a true side-view gait; turns are a quick horizontal flip. Faces cannot rotate in 3D (head turn = tilt plus eye shift).
- The camera "entering" the hidden room is a zoom into the dark doorway, a 0.4 s dim cross, then a cut inside where the characters appear in the doorway (continuous screen direction, but not one unbroken take).
- Characters are always drawn above the darkness mask, so they are never fully in shadow; beams are not occluded by bodies.
- Wrench is hidden while in the pocket and appears when the hand reaches it; no separate drawer animation. Bolts fall in a simple parabola with no bounce.
- Fixed set pieces, not a full 3D room; the interior is a flat side-view set.
- SFX/music are synthesised, so footsteps/creaks are simple.
