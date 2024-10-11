import pytest # type: ignore
from spectra_hook.spectra import Spectra
import time

spectra = Spectra()

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Called after the Session object has been created and before performing collection."""
    session.start_time = time.time()
    session.results = spectra.test_results
    print("\nStarting test session...")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Called after the whole test run finished, right before returning the exit status."""
    session.duration = time.time() - session.start_time
    session.exitstatus = exitstatus
    print(f"\nTest session finished. Duration: {session.duration:.2f} seconds")
    print(f"Exit status: {exitstatus}")

    # Generate HTML report
    spectra.generate_html_report(session)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """Called at the end of each test phase: setup, call, and teardown."""
    if report.when == 'call':
        function_name = report.nodeid.split("::")[-1]
        if report.passed:
            spectra.test_results['passed'].append(function_name)
            print(f"{function_name} PASSED")
        elif report.failed:
            spectra.test_results['failed'].append(function_name)
            print(f"{function_name} FAILED")
        elif report.skipped:
            spectra.test_results['skipped'].append(function_name)
            print(f"{function_name} SKIPPED")