# Episode 3 research notes: the Microsoft 365 / Outlook outage of November 12-13, 2026

## Facts used and sources
| Claim in the video | Source | Note |
|---|---|---|
| On Thursday, November 12, 2026 Outlook stopped working for millions | Variety; ABC News | Outlook on the web, desktop and mobile; also Teams calendar features, Copilot, parts of SharePoint (all things that depend on Exchange Online) |
| Reports spiked around 12:39 PM ET; more than 129,000 Downdetector reports by 1:09 PM ET | Variety | one UK summary has Downdetector peaking near 130,000 |
| Teams chat and calls mostly kept working; Exchange-dependent features failed | Microsoft service-health updates (via On-Site Technology, azureblog.co.uk) | |
| More than 450 million paid Microsoft 365 commercial seats | Variety (Microsoft earnings call, December 2025 quarter) | context, not part of the outage |
| Microsoft: technical issue, not related to cyber or AI | Microsoft statement via ABC News | |
| Front-door gateway servers; a Windows fix for them rolled out from July; ran for 3+ months without issue | Microsoft's preliminary post-incident report, as published by Office Watch | preliminary and subject to change |
| Latent bug (lock contention) triggered under heavy load on newer, higher-core-count servers; lab testing used weaker hardware | same report | |
| About 15 hours before, Teams traffic failed over onto the same gateway; nearly 14% of gateway capacity already out of service from an unrelated problem | same report | |
| At peak US business hours servers locked up; traffic redirected to healthy servers which also locked up; more than 80% unresponsive in under two hours | same report | |
| Recovery slow: restarted servers swamped by waiting traffic; usual rollback tools did not help because the change was months old; code rolled back; servers restored in batches, Asia Pacific then Europe | same report | |
| Webmail back to normal worldwide Friday morning ET; Microsoft declared the incident over around 11:10 AM ET Friday; marked fully restored late Friday after the email backlog was processed | Office Watch (report timings, UTC converted to ET); On-Site Technology; azureblog.co.uk (final update) | sources describe different end markers, so the video says "back to normal Friday morning" and "fully restored late Friday" |
| Delayed email not lost; Microsoft gave messages extra time to be delivered; check important messages sent Thu/Fri | Office Watch; azureblog.co.uk | |

## Conflicts and what I did
- Microsoft's earlier statement blamed "an issue during an earlier network capacity upgrade that surfaced following a recent network change". Its later preliminary report describes the July-fix bug plus load plus lost capacity. The video follows the later, more detailed report and says it is preliminary.
- Duration: Yahoo Finance said "about 36 hours" of disruption; Microsoft's own markers imply roughly a day (Thursday midday to Friday late morning for most impact). The video avoids a total-hours claim.
- A Boston University blog post about a November 2024 Microsoft outage appeared in search results; it is a different event and was not used.

## Not claimed
No claim of who is to blame, no claim of a link to other outages that week, no total-hours claim. The final post-incident report was still pending when this was written.
