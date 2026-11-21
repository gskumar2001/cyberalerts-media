# cyberalerts-media

Instagram posts and reels for **CyberAlerts** (@gskumar20012018).
*No glamour. Only cyberalerts.* One simple cyber safety alert per post, for everyday people.

## Posts

| # | Topic | Headline | CTA | Folder |
|---|-------|----------|-----|--------|
| 01 | Report fast | Got scammed? Report it in the first hour. | Act now | [01-first-hour](posts/01-first-hour) |
| 02 | Digital arrest | Police never arrest you on a video call. | Hang up | [02-digital-arrest](posts/02-digital-arrest) |
| 03 | OTP | No real company asks for your OTP. | Never share | [03-otp](posts/03-otp) |
| 04 | UPI PIN | You never need a UPI PIN to receive money. | Stay alert | [04-upi-pin](posts/04-upi-pin) |
| 05 | Voice clone | "Mom, I need money" could be AI. | Call back | [05-voice-clone](posts/05-voice-clone) |
| 06 | KYC SMS | "KYC expiring" SMS with a link? It's a trap. | Don't click | [06-kyc-sms](posts/06-kyc-sms) |
| 07 | QR code | Scanning a QR code never gets you money. | Don't scan | [07-qr-code](posts/07-qr-code) |
| 08 | Screen sharing | "Support" wants you to install a screen-sharing app? | Hang up | [08-screen-share](posts/08-screen-share) |
| 09 | Task scam | Paid to like videos? It's a trap. | Walk away | [09-task-scam](posts/09-task-scam) |
| 10 | Power bill | "Power cut tonight" SMS? Don't call that number. | Verify first | [10-power-bill](posts/10-power-bill) |
| ⚡ | Incident: Chrome | Chrome is under attack. Update it today. | Update now | [incident-chrome](posts/incident-chrome) |

Numbered posts are evergreen. `incident-*` posts are tied to a live event and should be posted promptly.

All 11 are posted as reels to Instagram @gskumar20012018 and the "Cyber alerts" Facebook page, and as images (post.jpg) to Threads @gskumar20012018. 01–06 and the Chrome incident went out on 19 Nov 2026; 07–10 on 21 Nov 2026.

## Layout

```
posts/<NN-slug>/
  post.jpg     feed image, 1080x1350 (4:5)
  reel.mp4     reel, 1080x1920, 8 s, shared soundtrack
  caption.md   Instagram caption and hashtags
  spec.json    text used to generate the post (generated posts only)
assets/
  soundtrack.m4a   the original reel soundtrack
tools/
  make_post.py     generator for new posts in the house style
```

## Making a new post

1. Create `posts/NN-slug/spec.json`:
   ```json
   {"headline": "No real company asks for your *OTP.*",
    "sub": "Anyone asking for it is a scammer. Never share it.",
    "cta": "Never share"}
   ```
   Wrap the words to highlight in yellow in `*...*`.
2. Run `python3 tools/make_post.py posts/NN-slug/spec.json`. This writes `post.jpg` and `reel.mp4`.
3. Add `caption.md` and a row to the table above.

Requires Python 3 with Pillow, ffmpeg, and the Anton and Poppins fonts.

## Helplines (India)

- **1930**: National Cyber Crime Helpline
- **cybercrime.gov.in**: file a complaint online
