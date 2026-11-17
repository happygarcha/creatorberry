# facelessreels.com: public-surface recon

Method: static analysis only. I read the public homepage, its public JavaScript bundles, and the public legal pages (terms, privacy, refund, cancellation). I did not log in and did not call any private API.

## Confirmed (from public files)

| Area | Finding | Source |
|---|---|---|
| Front end | Next.js (App Router) on Vercel | `/_next/static` paths, `server: Vercel`, Vercel Live script |
| Auth | Google sign-in via Auth.js (next-auth) | login page, `errors.authjs.dev` in bundle |
| Payments | Stripe (monthly, annual, one-time); trial periods exist | privacy policy, terms 4.4-4.6 |
| Credits | "Premium credits" are one-time and are spent on animating and regenerating images; a welcome grant comes with the first paid plan | terms 4.8-4.9 |
| Publishing | Real YouTube upload through the YouTube Data API with stored OAuth tokens, for videos the user schedules | privacy policy |
| Other platforms | TikTok and Instagram are named as targets; the privacy policy names only YouTube as an API integration | homepage, privacy |
| Analytics | PostHog, Google Tag Manager/Ads, Facebook Pixel, TikTok Pixel, Sentry, AppLovin/Axon pixels | bundle strings |
| Storage | Own CDN at `cdn.facelessreels.com`; generated content kept 3 months | bundle, terms 9.1 |
| Referrals | An affiliate programme with click tracking (`/api/referrals/track-click`) | bundle, affiliate terms |
| Niches | Mythology, school gossip, scary stories, history, acts of kindness, biblical stories, anime stories, heists | homepage |
| Images | Images are generated, then animated; this is the paid step | terms 4.8 |
| Own music | Users can supply their own audio; it is deleted within 24 h of delivery | terms 7.5 |
| Pipeline | Cloud rendering ("automated rendering pipeline") | terms 7.5 |
| Limits | Fair-use monitoring; accounts with automated or excessive use can be suspended | terms 9.3-9.4 |

## Not discoverable from outside

The AI models (script, voice, image, animation), the render engine, how scenes are timed, the database, and the app screens. They sit behind the login, and I did not try to get past it. Anything about them in the plan is my own design.

## What this means for the local build

1. **The core product is image-based storytelling.** Script → generated images → animated (Ken-Burns or image-to-video) → voice → captions. The expensive part there is image generation and animation, which is the part to replace with local models or free stock.
2. **Publishing is the only part that needs the cloud.** The YouTube API is official and free for your own channel, and is worth doing. TikTok and Instagram need approved apps, so use export plus a copy-ready caption.
3. **Skip what only exists for their business:** Stripe billing, credits, referrals, ad pixels, user accounts. A single-user local tool needs none of them.
4. **Keep what makes the output sell:** niche prompt templates, a strong first-second hook, word-by-word captions, scene pacing, music under the voice.

## Terms worth knowing

- Terms 6.3 give them a perpetual licence to use users' content for marketing. A local tool avoids this.
- No refunds; the content is deleted after 3 months. A local tool keeps your files.
