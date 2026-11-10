# Rewards program (agreed numbers)

Goal: repeat customers, more sign-ups, bigger baskets. Keep total reward cost to about 3-5% of spend.

## Earn
| Action | Points |
|---|---|
| Create an account | 50 |
| Each CA$1 spent | 1 |
| Photo or video review | 100 |
| Text review | 25 |
| Referring a friend (after their first order) | 200 |
| Birthday | 50 |

## Redeem
| Cost | Reward |
|---|---|
| 200 points | CA$5 off |
| 400 points | CA$10 off |
| 600 points | Free shipping (CA$9.99 value) |

## Rules
- Rewards usable on orders of CA$25 or more.
- Points expire after 12 months without a purchase.
- Rewards do not stack with "Buy 2, save 10%" on the same items.
- Only logged-in customers earn points.

## Entered in the app?
Not yet. The app (Loloyal, the "Rewards" bubble) is configured by the store owner in its own admin. Tick off here when done:
- [ ] Earn actions
- [ ] Redeem rewards
- [ ] Rules (minimum order, expiry, no stacking)
- [ ] Bubble colours and wording match the new design

## Site wording to add once the app is live (so the site never promises points that do not exist yet)
- Cart drawer: "Earn 1 point for every CA$1" (logged in) / "Log in to earn 1 point for every CA$1" (guest)
- Product page: same line under the price
- Wishlist page: "Log in to earn points and keep your favourites"

## Updates from the app screens
- Reviews: pick Judge.me (it was Disconnected, needs connecting). Text review 25 points, extra 75 for photos (the extra adds on top).
- Newsletter: Subscribe to newsletter, 25 points.
- Place an order: change from 5 points per $1 to 1 point per $1.
- Referrals: separate Referrals tab (plan availability not yet checked).
- Points expiry is a Pro feature, so leave it off for now.
- Participants: set Members only.
- Social follow rewards: later, once the accounts exist (see docs/todo.md).

## Status (both programs activated)
- Points program and Referral program are Active.
- Earn: order 1 point per $1, sign up 50, birthday 50, newsletter 25.
- Redeem: $5 off at 200 points, $10 off at 400, $15 off at 600 (minimum order CA$25 / $50 on the $10 one as saved in the app, all products, no combining).
- Referral: referrer and referred friend each get $5 off with a CA$30 minimum; email and Facebook sharing on; landing page is the home page.
- Friend popup picture: marketing/friend-popup-400x512.png (upload in the app's Friends get reward screen).

## Parked
- Review reward: needs the rewards app's higher plan for the Judge.me connection (Judge.me private API token, plus Judge.me's Awesome plan). Switch the review reward off for now; revisit when reviews are flowing.
- Points expiry (12 months) and free-shipping reward: locked behind plans (Pro / Essential).
- Panel and bubble appearance (still the default red Christmas look): change in the rewards app settings to coral #E8472B, plain banner, title "Drapewell Rewards".
- Site wording ("Earn 1 point for every CA$1") to add with the product page and cart drawer redesign.
