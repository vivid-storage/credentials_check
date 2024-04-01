from shiny import App, render, ui
import requests

# UI layout
app_ui = ui.page_fluid(
    ui.tags.div(
        ui.output_text_verbatim("urls_to_test_output"),
        style="white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word;",
    ),
    ui.tags.div(
        ui.output_text_verbatim("network_check_results_output"),
        style="white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word;",
    ),
)

# Server logic
def server(input, output, session):
    # Define URLs to test
    urls_to_test = [
        ("https://google.com", "success"),
        ("http://169.254.169.254", "failure"),
    ]

    @output
    @render.text
    def urls_to_test_output():
        # Display the URLs and their expected outcomes
        return "\n".join([f"{url} (Expected: {expected_result})" for url, expected_result in urls_to_test])

    @output
    @render.text
    def network_check_results_output():
        # Perform network checks and compile results
        results = []
        total_failures = 0
        
        for url, expected_result in urls_to_test:
            result = test_url(url)
            if (result and expected_result == "success") or (not result and expected_result == "failure"):
                results.append(f"Testing for {expected_result} connecting to {url}\tPASS")
            else:
                results.append(f"Testing for {expected_result} connecting to {url}\tFAIL")
                total_failures += 1
        
        results.append(f"TOTAL FAILURES = {total_failures}")
        return "\n".join(results)

def test_url(url):
    try:
        response = requests.get(url, timeout=2)
        # Assuming success means a status code less than 400
        return response.status_code < 400
    except (requests.ConnectionError, requests.Timeout):
        return False

app = App(app_ui, server)
