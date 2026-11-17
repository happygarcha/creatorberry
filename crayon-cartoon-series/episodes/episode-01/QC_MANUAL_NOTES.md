# Manual inspection notes, Episode 1

Method: frames were extracted from the FINAL mp4 at the beginning, middle and end of every scene
(`final/E01_contact_sheet_scenes_begin_mid_end.jpg`) and additional stills were taken every 1/8 of every scene during development.
I did not watch or listen to the video in real time; audio was checked with measurements (loudness, peaks, silence detection) and a speech
recognition round trip on the final mix.

Fixed during QC (each fix was re-rendered and re-inspected):
- caption chunks overlapped by 1-2 frames -> chunk windows can no longer overlap
- vault door appeared already open (single-key animation track) -> start keys added
- scene 5 board background leaked at the left edge after the board slid away -> background widened
- scene 6 had ~4 s of idle time after the crash -> scene shortened and the banker's line moved later
- headlines sat too close to the top UI -> moved into the safe band
- cartoon bell masked the first word of the baker's line -> bell moved before the word, crowd murmur lowered

Known limitations (honest list):
- Voices are local text-to-speech (Kokoro via sherpa-onnx): consistent per character but robotic; characters differ only by voice id and speed.
- Lip sync is word-level mouth open/close, not phoneme-accurate mouth shapes.
- Arm gestures are pose changes (swapped on cue), not smoothly tweened skeleton motion; legs scissor only while walking/running.
- Running is the walk cycle plus a faster body bob.
- Music and sound effects are synthesised (original, no licence issues) and simple.
- The prompt's scene timecodes are approximate: timing is voice-locked, so the real boundaries are 0 / 6 / 14 / 23 / 32 / 40.3 / 46.7 / 54.2 / 60.2 s (scene 6 was trimmed by 1.6 s of idle time; the last two scenes are the conclusion and the standard end card).
- No uploaded reference image was available in the prompt; the style follows the cartoon cast and kit already established in this project.
- Economics is deliberately simplified ("prices can rise"); the video says so on screen.

Ending revision: the vault/next-episode cliffhanger was removed. The ending is now the conclusion scene (Banker: print more money; Guy unplugs the printer;
narrator: more money does not automatically mean more wealth) followed by the standard animated Like / Share / Subscribe end card (6 s).
Scenes 1-5 were not re-rendered.
