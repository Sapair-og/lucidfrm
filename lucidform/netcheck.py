"""Network checks the gate may be given, but never performs itself (ISSUES.md LF-004).

The gate reads no network, so its verdicts are reproducible. A live session
injects `email_domain_ok` into it; offline tests and persona replays do not,
and the check is recorded as skipped there.
"""

from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=256)
def email_domain_ok(domain: str, timeout: float = 4.0) -> bool | None:
    """True if the domain publishes a mail server (MX), False if it cannot
    receive email, None if the lookup itself failed.

    An MX record is required. A domain with only a website (A record) is
    usually a parked or mistyped domain, and mail sent there is lost.
    """
    try:
        import dns.exception
        import dns.resolver
    except ImportError:
        return None
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=timeout)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False
    except (dns.exception.DNSException, OSError):
        return None
    # A "null MX" (RFC 7505: preference 0, target ".") says the domain takes no mail.
    return any(str(r.exchange) not in (".", "") for r in answers)
