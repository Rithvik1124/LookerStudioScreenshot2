import streamlit as st
import tempfile
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import time
import chromedriver_autoinstaller


# Report dictionary
reports = {
    #"BW Generation": "https://lookerstudio.google.com/reporting/7f396517-bca2-4f32-bdd4-6e3d69bc593b",
    "Sunoh": "https://lookerstudio.google.com/reporting/39b65949-427b-46b7-b005-bdb5cc8a109e",
    "Healow": "https://lookerstudio.google.com/reporting/8c4d2445-2567-482c-b6e7-fe4b035c704f",
    "UA": "https://lookerstudio.google.com/reporting/ba3d152c-3c93-4dd6-a4af-f779f598a234",
    "FCC": "https://lookerstudio.google.com/u/0/reporting/34ca31e9-0dd5-4f5e-88a5-b0c3b1dea831/page/p_rgnbotejdd",
    #"Scuderia": "https://lookerstudio.google.com/reporting/da8ba832-1df3-4412-9785-000262daa084",
    "Confido": "https://lookerstudio.google.com/u/0/reporting/7018b15a-0d1a-45e0-b5b1-8eb9122d66be/page/p_3f97qt2apd",
    "KodeKloud": "https://lookerstudio.google.com/u/0/reporting/7c9e0649-d145-46e3-a8e5-ee09955071d7/page/p_ef1ad8vrrd",
    #"HPFY": "https://lookerstudio.google.com/u/0/reporting/8b7be612-b8b5-4acd-bccf-a520fc4da59e/page/p_p5mqzik7pd",
    "AOL(Intuition)": "https://lookerstudio.google.com/u/0/reporting/10eac558-48e9-46eb-b5f9-1a7f0fa1e885/page/p_u5i8qqkord",
    "AOL(SSSY)": "https://lookerstudio.google.com/u/0/reporting/69aa7bb2-e88c-4d26-8e82-fd9bd56c5f31/page/p_u5i8qqkord",
    "CoveNLane": "https://lookerstudio.google.com/reporting/b2ae0d43-2e1f-409e-8ea0-0a20e8e89140/page/p_hbu2b5xsrd"
}

def export_report_to_pdf(driver, output_path="report.pdf", paper_size="A2", landscape=False, delay=10):
    size_map = {
        "A4": (8.27, 11.69),
        "A3": (11.69, 16.54),
        "A2": (16.54, 23.39),
        "A1": (23.39, 33.11),
        "A0": (33.11, 46.81)
    }

    if isinstance(paper_size, str):
        width, height = size_map.get(paper_size.upper(), size_map["A4"])
    else:
        width, height = paper_size

    time.sleep(delay)

    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True,
        "paperWidth": width,
        "paperHeight": height,
        "marginTop": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "marginRight": 0,
        "scale": 1.0,
        "landscape": landscape
    })

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(pdf_data['data']))

    return output_path


def run_report_automation(report_name, start_date, end_date):
    if report_name not in reports:
        return None, "Invalid report selected"

    url = reports[report_name]

    # Month lookup
    months = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    # Extract components
    start_day = start_date.day
    start_month = start_date.month
    start_year = start_date.year

    end_day = end_date.day
    end_month = end_date.month
    end_year = end_date.year


    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # where Chrome gets installed
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    driver.execute_script("document.body.style.zoom='33%'")

    try:
        date_picker_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mdc-button.mat-mdc-button-base.mat-mdc-tooltip-trigger.ng2-date-picker-button.mdc-button--outlined.mat-mdc-outlined-button.mat-unthemed.canvas-date-input"))
        )
        driver.execute_script("arguments[0].click();", date_picker_button)
        time.sleep(3)

        start_calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.mdc-button.mat-mdc-button-base.mat-calendar-period-button'))
        )
        start_calendar_button.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'button.mat-calendar-body-cell[aria-label="{start_year}"]'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"button.mat-calendar-body-cell[aria-label='{months[start_month]} {start_year}']"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'button.mat-calendar-body-cell[aria-label="{start_day} {months[start_month][:3]} {start_year}"]'))
        ).click()

        # END DATE
        end_calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.end-date-picker.calendar-wrapper .mdc-button.mat-mdc-button-base.mat-calendar-period-button'))
        )
        end_calendar_button.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{end_year}"]'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{months[end_month]} {end_year}"]'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{end_day} {months[end_month][:3]} {end_year}"]'))
        ).click()

        apply_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Apply"]]'))
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", apply_button)

        time.sleep(10)  
        output_file = os.path.join(
            tempfile.gettempdir(),
            f"{report_name}_{start_date.isoformat()}_to_{end_date.isoformat()}.pdf"
        )
        export_report_to_pdf(driver, output_path=output_file)
        return output_file, "✅ PDF generated successfully"
    except Exception as e:
        return None, f"❌ Error: {e}"
    finally:
        driver.quit()



st.title("📊 Looker Report Exporter")

report_name = st.selectbox("Select Report", list(reports.keys()))
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Generate PDF"):
    with st.spinner("Generating report..."):
        pdf_path, message = run_report_automation(report_name, start_date, end_date)
        st.success(message)

        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Report", f, file_name=os.path.basename(pdf_path), mime="application/pdf")
