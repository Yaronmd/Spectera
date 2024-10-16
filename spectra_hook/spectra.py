from typing import Optional


class Spectra:
    def __init__(self,title:Optional[str]):
        self.attached_data = {}
        self.test_results = {"passed": [], "failed": [], "skipped": []}
        self.start_date_and_time = None
        self.title = f"{title}" if title else "Test Result"
    
    def attach(self, description):
        """Decorator to attach data to the test function and track assertions."""
        def decorator(func):
            self.attached_data[func.__name__] = {"description": description, "assertion": None}
            return self.track_assertion(func)
        return decorator
    
    def track_assertion(self, func):
        """Wrapper to track assertions automatically."""
        def wrapper(*args, **kwargs):
            test_name = func.__name__
            try:
                result = func(*args, **kwargs)
                self.test_results['passed'].append(test_name)
                self.attached_data[test_name]["assertion"] = "Passed"
                return result
            except AssertionError as e:
                self.test_results['failed'].append(test_name)
                self.attached_data[test_name]["assertion"] = str(e)
                raise e  # Re-raise to ensure pytest captures the failure
            except Exception as e:
                self.test_results['failed'].append(test_name)
                self.attached_data[test_name]["assertion"] = f"Error: {str(e)}"
                raise e  # Re-raise to ensure pytest captures the failure
        return wrapper

    # def attach_assertion(self, func_name, assertion_value):
    #     """Attach the assertion value to the specified function."""
    #     if func_name in self.attached_data:
    #         self.attached_data[func_name]["assertion"] = assertion_value


    def generate_html_report(self, session):
        """Generate an HTML report for the test session."""
        with open("test_report.html", "w") as f:
            head = """<head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Report</title>
            <link rel="stylesheet" href="styles.css">
            </head>"""

            f.write(head)
            f.write("<html><body>\n")
            f.write("<div class='intro'>")
            f.write(f"<h1>{self.title}</h1>\n")
            f.write(f"<h2>Test Session Summary </h2>\n")
            f.write(f"<h2>{self.start_date_and_time}, Duration: {session.duration:.2f} seconds, Exit status: {session.exitstatus}</h2>\n")
            f.write("</div>")

            f.write("<h2>Passed Tests</h2>\n")
            f.write("<ul>\n")
            for test in self.test_results['passed']:
                if test in self.attached_data.keys():
                    f.write(f"<li>{test}: {self.attached_data[test]['description']}, Assertion: {self.attached_data[test]['assertion']}</li>\n")
                else:
                    f.write(f"<li>{test}</li>")
            f.write("</ul>\n")

            f.write("<h2>Failed Tests</h2>\n")
            f.write("<ul>\n")
            for test in self.test_results['failed']:
                if test in self.attached_data.keys():
                    f.write(f"<li>{test}: {self.attached_data[test]['description']}, Assertion: {self.attached_data[test]['assertion']}</li>\n")
                else:
                    f.write(f"<li>{test}</li>")
            f.write("</ul>\n")

            f.write("<h2>Skipped Tests</h2>\n")
            f.write("<ul>\n")
            for test in self.test_results['skipped']:
                if test in self.attached_data.keys():
                    f.write(f"<li>{test}: {self.attached_data[test]['description']}, Assertion: {self.attached_data[test]['assertion']}</li>\n")
                else:
                    f.write(f"<li>{test}</li>")
            f.write("</ul>\n")

            f.write("</body></html>\n")