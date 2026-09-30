"""A small fillable PDF shaped like a real bank form, for tests of LF-014.

Field names are deliberately unlike ours (txtApplicantName, PAN_No...) and the
labels are printed text beside the boxes, as in real forms.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

FIELDS = [
    # (widget name, printed label, kind, options, tooltip)
    ("txtApplicantName", "Name of Applicant", "text", None, ""),
    ("FatherName", "Father's Name", "text", None, ""),
    ("DOB", "Date of Birth", "text", None, ""),
    ("cboGender", "Gender", "choice", ["Male", "Female", "Other"], ""),
    ("PAN_No", "PAN", "text", None, ""),
    ("MobileNo", "Mobile Number", "text", None, ""),
    ("EmailID", "Email", "text", None, ""),
    ("Text12", "Postal PIN", "text", None, "PIN Code"),
    ("NomineeName", "Nominee Name", "text", None, ""),
    ("BankBranch", "Branch Name", "text", None, ""),
    ("DateJoining", "Date of Joining", "text", None, ""),
    ("chkAgree", "I agree", "check", None, ""),
]


def build(out: Path) -> Path:
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, 800, "Sample Bank Account Opening Form")
    c.setFont("Helvetica", 10)
    y = 760
    for name, label, kind, options, tooltip in FIELDS:
        c.drawString(60, y + 4, label)
        if kind == "text":
            c.acroForm.textfield(name=name, tooltip=tooltip or None, x=220, y=y, width=250, height=16, borderWidth=1)
        elif kind == "choice":
            c.acroForm.choice(name=name, options=options, value=options[0], x=220, y=y, width=120, height=16)
        else:
            c.acroForm.checkbox(name=name, x=220, y=y, size=14)
        y -= 34
    c.save()
    return out


if __name__ == "__main__":
    print(build(Path("sample_bank_form.pdf")))
