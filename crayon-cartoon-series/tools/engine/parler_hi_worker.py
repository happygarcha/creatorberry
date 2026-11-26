"""Runs INSIDE ~/venvs/parler (torch + parler-tts). Synthesises Hindi lines with ai4bharat/indic-parler-tts (Apache-2.0, trained on Devanagari speech).
  parler_hi_worker.py jobs.json     jobs = [{"text","desc","out"}]; skips jobs whose out file already exists."""
import sys, os, json, time, torch, soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
torch.set_num_threads(os.cpu_count() or 4)
jobs = [j for j in json.load(open(sys.argv[1])) if not os.path.exists(j['out'])]
if not jobs: sys.exit(0)
model = ParlerTTSForConditionalGeneration.from_pretrained('ai4bharat/indic-parler-tts')
tok = AutoTokenizer.from_pretrained('ai4bharat/indic-parler-tts'); dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
for j in jobs:
    t0 = time.time(); d = dtok(j['desc'], return_tensors='pt'); p = tok(j['text'], return_tensors='pt')
    torch.manual_seed(7)
    g = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask, prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
    a = g.cpu().numpy().squeeze(); sf.write(j['out'], a, model.config.sampling_rate); print(f"{len(a) / model.config.sampling_rate:.1f}s audio in {time.time() - t0:.0f}s: {j['text'][:40]}", flush=True)
