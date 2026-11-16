# Animated Short Film

One sentence in, a painterly cinematic short film out.

Run `/animate` followed by your idea, for example:

```
/animate a courier on a bicycle has to reach the ferry before the ramp lifts
```

The skill writes the story, the image prompts for your character, location and
object sheets, and one timestamped master video prompt with a style lock. You
generate the images and the clip in the image and video tools of your choice; the
skill never generates anything itself.

Folder layout (created as needed, all optional):

- `references/` your generated plates
- `prompts/` saved prompt packages
- `renders/` clips from the video tool
- `final/` accepted masters

## Tips for the best results

- Write the idea as **goal plus obstacle**: "a courier has to reach the ferry before the ramp lifts" beats "a courier rides through the city".
- Keep **one hero, one vehicle, one location per scene**. The more identities you mix, the faster the model drifts.
- Generate the asset sheets **before** the video, never let the video model invent the character.
- Wide and medium shots hold the painted look better than close-ups.
