from typing import Optional
import time

class Spectra:
    def __init__(self,title:Optional[str]):
        self.attached_data = {}
        self.test_results = {"passed": [], "failed": [], "skipped": []}
        self.start_date_and_time = None
        self.title = f"{title}" if title else "Test Result"
        self.start_session = None

    def set_start_session(self):
        self.start_session = time.time()

    def set_duration(self):
        if self.start_session:
            self.end_session = time.time() - self.start_session
            print(f"\nTest session finished. Duration: {self.end_session:.2f} seconds")

    def set_exit_status(self,exit_status):
        self.exit_status = exit_status
        
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
                self.attached_data[test_name]["assertion"] = ""
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
    
    def __parse_tests_to_html(self, status, collapsible_class):
        if not self.test_results[status]:
            return ""
        
        # Create the button with the correct status (passed/failed) and class (green/red)
        html_result = f"<button type='button' class='collapsible {collapsible_class}'>{status.capitalize()} tests</button>\n"
        rows = ""
        description = ""
        assert_str = ""
        for test in self.test_results[status]:
            if test in self.attached_data.keys():
                # If description is a string, add it directly
                if isinstance(self.attached_data[test]['description'], str):
                    if self.attached_data[test]["assertion"]:
                        assert_str = self.attached_data[test]["assertion"]
                    rows += f"<li>{test}: {description}<ul>\n {'Assertion:'+assert_str if assert_str else ""}</ul></li>\n"
                    
                
                # If description is a list, format it as a nested <ul>
                elif isinstance(self.attached_data[test]['description'], list):
                    if self.attached_data[test]["assertion"]:
                        assert_str = self.attached_data[test]["assertion"]
                    description = "<p>Test body</p> <ol type='1'>\n" + "\n".join(f"<li>{item}</li>\n" for i, item in enumerate(self.attached_data[test]['description'])) + "\n</ol>\n"
                    rows += f"<li>{test}: {description} {'Assertion:'+assert_str if assert_str else ""}</li>\n"
            else:
                # If no attached data, just show the test name
                rows += f"<li>{test}</li>\n"

        # Wrap the results inside a collapsible content div
        html_result += f"<div class='content'>\n<ul>{rows}</ul>\n</div>\n"
        return html_result
 

    def __parse_passed_to_html(self):
        return self.__parse_tests_to_html(collapsible_class="green",status="passed")

    def __parse_fail_to_html(self):
       return self.__parse_tests_to_html(collapsible_class="red",status="failed")

    def __parse_skip_to_html(self):
        return self.__parse_tests_to_html(collapsible_class="yellow",status="skipped")
    
    def generate_html_report(self):


        def add_collepse_script():
            return """<script src="spectra_hook/scripts/collepse_script.js"></script>"""
        

        """Generate an HTML report for the test session."""
        with open("test_report.html", "w") as f:
            head = """<head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Report</title>
            <link rel="stylesheet" href="styles.css">
            </head>"""

            f.write(head)
            f.write("<html>\n<body>\n")
            f.write("<div class='intro'>")
            f.write(f"<h1>{self.title}</h1>\n")
            f.write(f"<h2>Test Session Summary </h2>\n")
            f.write(f"<h2>{self.start_date_and_time}, Duration: {self.end_session:.2f} seconds, Exit status: {self.exit_status}</h2>\n")
            f.write("</div>")
            f.write(self.__parse_passed_to_html())
            f.write(self.__parse_fail_to_html())
            f.write(self.__parse_skip_to_html())
            f.write(add_collepse_script())
            f.write("\n</body>\n</html>\n")