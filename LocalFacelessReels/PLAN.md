# Local Faceless Reels: personal build plan

## 1. What facelessreels.com actually is (from its public pages only)

Evidence: the public homepage (Next.js site), its meta text, and the legal-page links. The app itself is behind "Sign in with Google", and I did not try to get past that.

- **Pitch:** "AI generates and posts faceless videos to TikTok, Instagram & YouTube on autopilot."
- **Niche presets:** mythology, school gossip, scary stories, history, acts of kindness, biblical stories, anime stories, heists.
- **Claims:** a first video "in under 5 minutes". It positions itself against hiring editors ($50-200 per video) and against making videos by hand.
- **Inferred pipeline (not confirmed):** niche → AI story script → voiceover → visuals → word-by-word captions → vertical render → scheduled auto-post.
- **Not visible from outside:** which models, voices and image sources it uses, how it posts to each platform, and its pricing. Anything about those would be a guess.

This plan is a clean-room design. Nothing from their code, assets or branding is copied.

## 2. Product to build: "LocalReels" (private, single user)

One pipeline, two front ends:

| Piece | Laptop-first choice | Notes |
|---|---|---|
| Orchestrator | Python 3.11 + FastAPI | One job = one video, stored as a folder with a `job.json` |
| Script writer | Ollama (Llama 3.x / Qwen) locally, or any API model | Prompt templates per niche; output is a JSON list of scenes (narration + visual prompt) |
| Voice | Piper or Kokoro TTS (offline) | Check each voice's licence before monetising |
| Word timings | faster-whisper on the generated audio | Gives word-level timestamps for captions |
| Visuals | (a) free stock via Pexels/Pixabay APIs, (b) local Stable Diffusion / FLUX if a GPU exists, (c) your own uploaded clips | Start with (a); it works on any laptop |
| Motion | FFmpeg `zoompan` / moviepy Ken-Burns, crossfades | Gives real movement on still images |
| Captions | Generate `.ass` subtitles, burn in with FFmpeg | Word-by-word highlight, centred lower third |
| Music | CC0/royalty-free loop folder, ducked under voice | `sidechaincompress` in FFmpeg |
| Render | FFmpeg, 1080x1920, 30 fps, H.264 + AAC | Same validation with ffprobe |
| Scheduler | APScheduler / cron | Queue of finished videos with post times |
| Publishing | YouTube Data API (your own channel); TikTok and Instagram start as "export + reminder" | Their upload APIs need app approval; add them later if approved |
| UI | Small web page served by FastAPI (a PWA) | Open it from your phone over home Wi-Fi |

## 3. Running it on your phone

- **Best:** run the engine on your laptop or a home PC, and use the phone only as a remote control through the PWA. Use Tailscale if you want access away from home. All heavy work (TTS, Whisper, render) stays on the laptop.
- **Fully on-phone (Android only):** Termux with FFmpeg, Python, Piper and a small Whisper model. It works for slideshow-style stock videos but is slow and battery-hungry. iPhone cannot realistically run this stack.

## 4. Build phases

1. **MVP (CLI):** `reels make --niche history --topic "..."`. Script → TTS → Whisper → stock clips → captions → MP4. Done when one 30-45 s Short renders end to end.
2. **Quality pass:** niche templates, hook line, scene pacing, music ducking, per-niche caption styles, thumbnail frame.
3. **Web UI:** a topic box, a niche picker, a preview player, an "approve" button, and a queue page.
4. **Scheduler and publishing:** YouTube upload first. Then TikTok/Instagram via official APIs, or semi-manual export with a copy-paste caption and hashtags.
5. **Polish:** batch generation (10 scripts at once), a no-repeat topic history, retry on failed stages, a log per job.

## 5. Risks to decide on early

- **Content policy:** YouTube, TikTok and Instagram reduce reach or demonetise mass-produced, repetitive AI content. Vary topics, voices and visuals, and keep a human approval step.
- **Licensing:** check licences for TTS voices, stock footage and music. The stock APIs allow free use but have attribution and no-redistribution rules.
- **Auto-posting:** TikTok and Instagram publishing APIs are gated. Don't plan on unofficial login-based bots; accounts get banned.
- **Hardware:** local image generation needs a decent GPU. Without one, use stock footage.

## 6. What I need from you to start Phase 1

1. Laptop OS and whether it has an NVIDIA GPU.
2. Which niche to start with, and which platform to publish to first.
3. Whether to use a local LLM (free, slower) or an API key you already have.
4. A confirmation that you want me to build it in this repo under `LocalFacelessReels/`.
