# The Last Ferry

**Idea:** a courier on a bicycle has to reach the ferry before the ramp lifts.

## Story

**Logline:** At dusk, a young courier races across a rain-washed harbor town with a sealed parcel. The ferry's horn sounds and the ramp begins to rise. She makes a desperate choice and leaps the gap, landing as the ferry pulls away.

- **Setup:** Courier pedals down a steep cobbled street; the ferry horn sounds below.
- **Escalation:** Tight alley shortcut, a rolling cart blocks her, she bunny-hops it.
- **Turn:** Pier reached, ramp already lifting; gap widens.
- **Resolution:** She launches off the ramp edge, lands on deck, parcel safe, harbor lights recede.

## Style Lock (use verbatim in every prompt)

Hand-painted cinematic animation, visible oil-brush strokes and soft canvas grain, palette of deep teal, rain-grey, warm lantern amber, rust red and cream. Dusk lighting with glowing lantern pools and wet reflective cobbles. Anamorphic widescreen 16:9, shallow depth of field, gentle painterly motion blur, 24 fps feel. Negative: no text, no logos, no photoreal skin, no 3D plastic look, no flicker, no style drift, no extra characters in foreground.

## Image Prompts

### CHAR-1 Courier
[Style lock] Character turnaround sheet on a plain warm-grey background: front, three-quarter, side and back views plus a face close-up. A woman in her early 20s, slim athletic build, short black bob with a wind-swept fringe, light brown skin, determined expression. Rust-red waterproof jacket with cream reflective stripe, dark teal cycling shorts under a knee-length rain cape rolled at the waist, tan canvas courier satchel across the chest, fingerless gloves, worn white sneakers. Neutral standing pose, even lighting.

### OBJ-1 Bicycle and Parcel
[Style lock] Multi-angle object sheet on a plain background: a battered steel-frame courier bicycle painted teal with a cream front basket, amber dynamo lamp, flat handlebars, fat tires, mud spatter; beside it a small oilcloth-wrapped parcel tied with red string and a wax seal. Side, front and three-quarter views.

### LOC-1 Harbor Town Street
[Style lock] Wide establishing plate: a steep cobbled street descending toward a harbor at dusk, rain just stopped, crooked timber-and-brick houses, glowing amber lanterns, wet reflective stones, a distant ferry with lit windows at the bottom. Add two variants: a low angle looking down the slope, and a narrow alley shortcut with hanging laundry.

### LOC-2 Ferry Pier
[Style lock] Wide plate: a wooden pier with a lowering and raising steel boarding ramp, mooring ropes, bollards, a small ferry with a warm-lit deck and a rust-red funnel, dark teal water, harbor lamps. Add two variants: ramp lowered (side view) and ramp half raised with a gap of open water.

## Master Video Prompt

**Attach references:** CHAR-1, OBJ-1, LOC-1, LOC-2. **Duration:** 15 s. **Aspect:** 16:9.

Style lock: Hand-painted cinematic animation, visible oil-brush strokes and soft canvas grain, palette of deep teal, rain-grey, warm lantern amber, rust red and cream. Dusk lighting with glowing lantern pools and wet reflective cobbles. Anamorphic widescreen 16:9, shallow depth of field, gentle painterly motion blur, 24 fps feel.

- **0:00-0:03** Wide, slow push-in on LOC-1 from above. CHAR-1 on OBJ-1 crests the top of the steep street and starts downhill. A low ferry horn sounds; lanterns flicker. Ambience: dripping gutters, tire hiss.
- **0:03-0:06** Tracking shot alongside her, low angle, cobbles rattling. She swerves into the narrow alley shortcut, laundry brushing past her shoulder. Amber light strobes through the gaps.
- **0:06-0:08** Front view, the alley exit. A wooden cart rolls across; she pulls up on the handlebars and bunny-hops it, rain cape flaring. Ground-level camera catches the wheels clearing the cart.
- **0:08-0:11** Wide at LOC-2. She bursts onto the pier; the ramp is already rising and open dark water widens. Horn sounds again. Camera tracks behind her, then whips to a side view of the gap.
- **0:11-0:13** Slow-motion side shot: she launches off the end of the ramp, bike and parcel in profile against the glowing ferry, paint-splash droplets hanging in the air.
- **0:13-0:15** Landing on the deck, wheels skid on wet planks. She exhales, grips the satchel. Camera pulls back and up as the ferry glides away and the harbor lanterns shrink into amber dots. Fade to teal.

**Continuity:** CHAR-1 costume, OBJ-1 bike and parcel, and dusk lighting are identical in every shot; no new locations.
**Negative:** no text, no logos, no photoreal skin, no 3D plastic look, no flicker, no style drift, no extra foreground characters.

## Generation Checklist

- [ ] Generate CHAR-1, OBJ-1, LOC-1, LOC-2 sheets into `references/`
- [ ] Attach them and run the master video prompt; save clips in `renders/`
- [ ] Move the accepted master to `final/`
