import pytest # type: ignore
from spectra_hook.spectra import Spectra
import time
from datetime import datetime
spectra = Spectra(title="Spectra project")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Called after the Session object has been created and before performing collection."""
    spectra.start_date_and_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    spectra.set_start_session()
    session.results = spectra.test_results
    print("\nStarting test session...")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Called after the whole test run finished, right before returning the exit status."""
    spectra.set_duration()
    spectra.set_exit_status(exit_status=exitstatus)
    print(f"Exit status: {exitstatus}")

    # Generate HTML report
    spectra.generate_html_report()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """Called at the end of each test phase: setup, call, and teardown."""
    if report.when == 'call':
        function_name = report.nodeid.split("::")[-1]
        if report.passed and function_name not in spectra.test_results['passed']:
            spectra.test_results['passed'].append(function_name)
            print(f"{function_name} PASSED")
        elif report.failed and function_name not in spectra.test_results['failed']:
            spectra.test_results['failed'].append(function_name) 
            print(f"{function_name} FAILED")
        elif report.skipped and function_name not in spectra.test_results['skipped']:
            spectra.test_results['skipped'].append(function_name)
            print(f"{function_name} SKIPPED")