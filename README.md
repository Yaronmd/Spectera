
# Spectra Test Reporting Framework

**Spectra** is a test reporting framework designed to collect and process test results in the background during test execution. It generates an HTML report at the end of a test session, providing a structured view of passed, failed, and skipped test cases. Spectra integrates seamlessly with popular testing frameworks like `pytest` and offers customizable reporting using collapsible sections.

## Key Features

- **Background Data Collection**: Test results are collected in real time as tests run, ensuring a smooth and efficient reporting process.
- **HTML Report Generation**: Spectra generates a detailed HTML report at the end of the test session. The report includes collapsible sections for passed, failed, and skipped tests, making it easy to navigate through the results.
- **Customizable Test Attachments**: Attach additional information (e.g., descriptions) to each test using the `@hookname.attach` decorator, and Spectra will include these details in the report.
- **Collapsible Sections**: Each category of tests (passed, failed, skipped) is displayed in collapsible sections with color-coded buttons (`green`, `red`, `yellow`).

## Installation

To install Spectra, you can clone the repository and install the necessary dependencies.

```bash
git clone https://github.com/yourusername/spectra.git
cd spectra
pip install -r requirements.txt
```

## Usage

### 1. Collecting Test Results

Spectra is designed to integrate with `pytest` and automatically collect test results. Use the built-in hooks to start tracking test sessions and results.

For example:

```python
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    spectra.start_date_and_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    session.start_time = time.time()
    session.results = spectra.test_results
    print("\nStarting test session...")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    session.duration = time.time() - session.start_time
    session.exitstatus = exitstatus
    print(f"\nTest session finished. Duration: {session.duration:.2f} seconds")
    print(f"Exit status: {exitstatus}")
    spectra.generate_html_report(session)
```

### 2. Attaching Data to Tests

You can attach additional data to individual tests using a custom decorator like `@hookname.attach`. This allows you to provide descriptions or additional context for each test in the HTML report.

Example:

```python
@hookname.attach("Test Description")
def test_example():
    assert 1 == 1
```

### 3. Generating HTML Reports

Once the tests are executed, Spectra will automatically generate an HTML report. The report includes collapsible sections for passed, failed, and skipped tests, as shown below:

```html
<ul>
  <button class="collapsible green">Passed tests</button>
  <div class="content">
    <li>test_example: Test Description</li>
  </div>

  <button class="collapsible red">Failed tests</button>
  <div class="content">
    <li>test_failure: Some Failure Description</li>
  </div>
</ul>
```

### Example Output:

The generated HTML report will show:
- **Green collapsible section for passed tests**.
- **Red collapsible section for failed tests**.
- **Yellow collapsible section for skipped tests** (if applicable).

## Customizing the Report

You can customize the appearance of the HTML report by modifying the `collapsible` and `content` styles in the CSS. The default color coding is:
- Green for passed tests
- Red for failed tests
- Yellow for skipped tests

```css
.collapsible.green { background-color: #0ad34a; }
.collapsible.red { background-color: #d33a0a; }
.collapsible.yellow { background-color: #f1c40f; }
```

## Future Enhancements

- **JSON Report**: Add support to generate a JSON report for easier integration with other systems.
- **Test Metrics**: Provide additional metrics like test duration, success rates, etc., in the report.
- **Dynamic Filtering**: Allow users to dynamically filter tests in the HTML report based on the status.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or report any issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
