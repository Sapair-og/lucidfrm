# LucidForm — Live Demo Guide (official CKYC form)

Script verified live against Gemini on 2026-10-01 (20 answers, approved, clean PDF).
Replies can vary run to run, so **read each question before typing**. If it asks
"Is that correct?", answer `yes` or `no`.

## Before the meeting
1. Open `data\forms\official\ckyc_individual_amfi.pdf`, the blank official 4-page CKYC form.
2. In a **new** terminal: `lucidform extract -f pan -u "A F R P Y 4 5 2 1 K"` should say PASS.

## Opening (30 s)
"This is the real KYC form. People who can't read it well depend on someone else to fill it.
LucidForm fills it by conversation. The AI only interprets what they say; fixed rules check
every value, and nothing is saved until the person says yes."

## Live run: type `lucidform`

First it asks **"Do you want to fill your own PDF form?"**. Type `no` for the official
CKYC demo below. To show your own form, type `yes`, then paste the path (in File Explorer:
right-click the PDF → "Copy as path"). Try `data\forms\samples\sample_bank_form.pdf`.

| Asked for | Type | Point out |
|---|---|---|
| Title | `Mr` → `yes` | |
| Name | `mera naam suresh prasad yadav hai` → `haan ji` | Hindi sentence in, clean name out |
| Father | `ram prasad yadav` → `yes` | |
| DOB | `fourteenth march nineteen fifty eight` → `yes` | |
| Gender | `male` → `yes` | |
| PAN | `pan kya hota hai` | **Help agent** cites the Income Tax FAQ |
| PAN | `mere paas pan hai par number yaad nahi` | **How to find it**: DigiLocker, Instant e-PAN steps, YouTube help link. Not treated as "no PAN" |
| PAN | `A F R P X 4 5 2 1 K` | **Rejected**: 5th letter must match the surname |
| PAN | `A F R P Y 4 5 2 1 K` → `yes` | Read back letter by letter |
| Marital | `shaadi shuda` → `yes` | |
| Citizenship | `indian` → `yes` | |
| Residence | `i live in india` → `yes` | **Offer**: "I think you meant Resident Individual" (needs yes) |
| Proof of identity | `voter card` → `yes` | |
| Document number | `ABC123` | **Rejected**: voter ID is 3 letters + 7 digits |
| Document number | `ABC1234567` → `yes` | |
| Address | `sarai mohana, rajghat` → `yes` | |
| PIN | `221001` → `yes` | |
| District | *(proposed)* `yes` | "Your PIN code 221001 is in Varanasi" |
| City | `kota` | **Rejected**: Kota is in Rajasthan, the PIN is in UP |
| City | `varanasi` → `yes` | |
| State | *(proposed)* `yes` | Derived from the PIN |
| Same address? | `haan` → `yes` | |
| Mobile | `+91 98390 12457` → `yes` | |
| Email | `suresh.yadav@gmial.com` → `yes` | **Typo caught**, gmail.com offered |
| Place | *(proposed)* `yes` | |
| Final review | say `change city`, answer again, then `yes` | Every value read back; nothing is final without a yes |

The filled official PDF opens automatically. Show the boxes filled in BLOCK letters and the ticks.

## Things to try if asked
- Say `i dont have` at PAN: it offers **Form 60** and ticks "FORM 60 furnished".
- Say `no` at "same address": it asks for the current address block.
- Quit halfway (Ctrl+C): the PDF is stamped **INCOMPLETE**.

## Backups
- No network: `lucidform run --persona p02 --replay` (template form, offline).
- One rule alone: `lucidform gate-check -f aadhaar -v 999999999999` (placeholder rejected).
- Pipeline diagram: `lucidform graph`.
