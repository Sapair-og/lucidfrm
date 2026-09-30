# Live demo — 5 minutes, terminal only

Everything below runs against the real model (`gemini-3.5-flash-lite`). All data is synthetic.
Before starting: `.env` has `GEMINI_API_KEY`, and the help index exists (`lucidform help build`).

```bash
cd LucidForm
.venv/Scripts/python -m lucidform.cli run --export data/forms/demo.pdf
```

## Script — what to type, and what to point out

| # | When asked for | Type | What happens / what to say |
|---|---|---|---|
| 1 | Full name | `mera naam suresh prasad yadav hai` | Gemini pulls the name out of the sentence. Read back → type `haan ji` → saved. |
| 2 | Father's name | `ram prasad yadav` | `yes` |
| 3 | Date of birth | `fourteenth march nineteen fifty eight` | Read back as a date. `yes` |
| 4 | Gender | `male` | `yes` |
| 5 | PAN | `pan kya hota hai` | **Help agent**: a plain-language answer with its source ("Income Tax PAN FAQ, Q1"). Not a value — the field is asked again. |
| 6 | PAN | `A F R P X 4 5 2 1 K` | **Gate rejects**: the 5th letter must match the surname (Y for Yadav). The model proposed it; the deterministic check said no. |
| 7 | PAN | `A F R P Y 4 5 2 1 K` | Read back letter by letter. `yes` |
| 8 | Aadhaar | `kya aadhaar dena zaroori hai?` | Help agent answers from **RBI KYC FAQ, Q10**. |
| 9 | Aadhaar | `9 6 3 4 8 6 0 0 9 4 7 3` | **Gate rejects: checksum** (Verhoeff). One digit is wrong; nothing a model said can get it past. |
| 10 | Aadhaar | `9 6 3 4 8 6 0 0 9 4 7 2` | Read back in groups of four. Type **`yes I know that's wrong`** → **not saved** (the whole reply must be a yes, not merely contain one). Asked again; give it again, then `yes`. |
| 11 | Address | `sarai mohana, rajghat` | `yes` |
| 12 | City | `varanasi` | `yes` |
| 13 | State | `uttar pradesh` | `yes` |
| 14 | PIN | `110001` | **Gate rejects: cross-field** — a Delhi PIN with Uttar Pradesh. Then `221001`, `yes`. |
| 15 | Mobile | `+91 98390 12457` | Normalised to 10 digits and read back. `yes` |
| 16 | Email | `email nahi hai` | Optional — recorded as declined, not as an empty value. |
| 17 | Occupation | `kheti karta hoon` | **Not mapped** to "Agriculture" by the model — rejected as not an option. Then `agriculture`, `yes`. |
| 18 | Income band | `ek lakh se kam` | Same rule. Then `below 1 lakh`, `yes`. |

End: the form is written to `data/forms/demo.pdf`; open it to show the filled fields.

## The one-line pitch while it runs
The model interprets; it never writes. Every value passed a deterministic gate, was read back, and
was saved only on an explicit yes — and a test fails the build if any code path skips that.

## Backup commands (if the network is slow)
```bash
.venv/Scripts/python -m lucidform.cli run --persona p02 --replay     # offline, whole form, simulated user
.venv/Scripts/python -m lucidform.cli help ask -f aadhaar -q "kya aadhaar dena zaroori hai?" --lang hi
.venv/Scripts/python -m lucidform.cli gate-check -f aadhaar -v 963486009473   # checksum rejection, no model
.venv/Scripts/python -m lucidform.cli graph                               # the LangGraph pipeline
```
