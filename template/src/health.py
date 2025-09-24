from fastapi_healthchecks.checks import Check, CheckResult

class SimpleHealthCheck(Check):
    """Simple health check that always returns true."""
    async def __call__(self) -> CheckResult:
        return CheckResult(name="server", passed=True)