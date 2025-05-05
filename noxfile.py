from __future__ import annotations

import nox


@nox.session
def tests(session: nox.Session) -> None:
    session.install("pytest", "sphinx")
    session.install(".")
    session.run("pytest")
