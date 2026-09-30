"""The help agent: answers a user's question about a field from official documents.

It explains; it never supplies a value. Its output goes to the user as an
explanation and nowhere else -- it has no access to FormState, produces no
Candidate, and the architecture test forbids the gate and the write path from
importing it.
"""
