# LinkedIn UI Test Automation

**Module:** IT3153 - Software Quality Assurance  
**Assignment:** 04 - Take Home Assignment  
**Degree:** Bachelor of Science Honours in IT / IS  
**Institution:** General Sir John Kotelawala Defence University  

---

## 1. Project Overview
This project contains an automated UI test suite for **LinkedIn** developed in **Java 17** using **Selenium WebDriver** and **TestNG**. It automates three main user flows:
1. **Login Automation (TC-01 & TC-02):** Valid login test and negative login test with an invalid password.
2. **Search Automation (TC-03):** Global search for a keyword and verification of the search results page.
3. **Click Search Result (TC-04):** Clicking the first search result and verifying that the correct profile/company page opens.

The framework follows the **Page Object Model (POM)** pattern and uses **Explicit Waits** (`WebDriverWait` with `ExpectedConditions`) to handle dynamic content without hardcoded sleeps.

---

## 2. Project Structure
```
linkedin-ui-tests/
├── src/test/java/com/sqa/linkedin/
│   ├── base/            # BaseTest (browser setup & tearDown) and DriverFactory
│   ├── pages/           # Page Object classes (BasePage, LoginPage, FeedPage, SearchResultsPage)
│   ├── tests/           # TestNG test classes (LoginTest, SearchTest, SearchResultTest)
│   └── utils/           # Utility classes (ConfigReader, ScreenshotUtil)
├── src/test/resources/
│   ├── config.properties          # Test credentials and settings (git-ignored)
│   └── config.properties.example  # Template configuration
├── pom.xml              # Maven dependencies (Selenium 4.25, TestNG 7.10)
├── testng.xml           # TestNG test runner suite
├── TestReport.html      # Complete academic report (open in browser and save as PDF)
└── README.md
```

---

## 3. How to Configure Credentials
Before running positive login tests, configure your own LinkedIn test account:

1. Open `src/test/resources/config.properties`.
2. Fill in your username/email and password:
   ```properties
   linkedin.username=your_test_email@example.com
   linkedin.password=your_test_password
   ```
*(Note: `config.properties` is included in `.gitignore` so your credentials will not be committed to GitHub).*

---

## 4. How to Run the Tests

### Option A: Using VS Code (Recommended)
1. Open this project folder in **VS Code** (`File -> Open Folder...`).
2. Make sure the **Extension Pack for Java** is installed.
3. Open any test file in `src/test/java/com/sqa/linkedin/tests/` (e.g. `LoginTest.java`).
4. Click the **Green Play Button ** next to any test method to run it.
5. Or open the **Testing ** tab on the left sidebar to run all tests with one click.

### Option B: Using the Terminal (Maven)
Open the terminal in VS Code (or PowerShell) in the project root:

* **Run all tests:**
  ```bash
  mvn clean test
  ```

* **Run only Login tests (TC-01 & TC-02):**
  ```bash
  mvn test -Dtest=LoginTest
  ```

* **Run only Negative Login test (runs without credentials):**
  ```bash
  mvn test -Dtest=LoginTest#invalidPasswordShouldShowError
  ```

* **Run only Search test (TC-03):**
  ```bash
  mvn test -Dtest=SearchTest
  ```

* **Run only Search Result click test (TC-04):**
  ```bash
  mvn test -Dtest=SearchResultTest
  ```

---

## 5. Test Results and Reports
* **TestNG Execution Report:** Generated automatically at:
  ```
  target/surefire-reports/index.html
  ```
  Open this file in Google Chrome or any browser to see the execution results.
* **Screenshots:** Screenshots for each test (labeled with `PASS_` or `FAIL_`) are captured automatically in:
  ```
  target/screenshots/
  ```
* **PDF Report (Task 6 Deliverable):** Open `TestReport.html` in Chrome/Edge, enter your Name and Index Number, and click **"Print to PDF / Save as PDF"** (or press `Ctrl + P`) to save your submission PDF.

---

## 6. Security and Bot Detection (Rules & Ethics)
* The test suite uses **headed browser mode** (visible browser).
* In accordance with the assignment guidelines, if LinkedIn shows a CAPTCHA or security verification checkpoint, the test pauses (up to 180s) to allow you to complete it manually in the browser before resuming.
