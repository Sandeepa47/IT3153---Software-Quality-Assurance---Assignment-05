# LinkedIn Automated UI Test Suite (Selenium + TestNG + Java 17+)

**Module:** IT3153 - Software Quality Assurance  
**Assignment:** 05 (Take Home Assignment)  
**Institution:** General Sir John Kotelawala Defence University - Faculty of Computing  

---

## Project Overview
This repository contains a test automation framework developed in **Java 17** using **Selenium WebDriver (4.25.0)** and **TestNG (7.10.2)** to automate core user flows on **LinkedIn**:
1. **Login Automation:** Positive authentication (valid credentials) and Negative testing (invalid credentials with error assertions).
2. **Search Automation:** Global search execution and result page validation.
3. **Search Result Navigation:** Locating, clicking the primary entity result, and asserting destination page authenticity.

The architecture strictly follows the **Page Object Model (POM)** pattern and uses **pure explicit waits** (`WebDriverWait` + `ExpectedConditions`) without brittle hardcoded sleeps.

---

## Project Architecture (Page Object Model)

```
linkedin-ui-tests/
│
├── .gitignore                                 # Ignores target/, IDE files, and sensitive credentials
├── pom.xml                                    # Maven configuration & dependencies
├── testng.xml                                 # TestNG test suite runner
├── run_tests.bat                              # 1-Click test execution script (preconfigured with JDK 21)
├── README.md                                  # Setup & execution instructions
├── Test_Report_IT3153.html                    # Academic test report template (ready to print to PDF)
├── REPORT_TEMPLATE.md                         # Markdown report template
│
└── src/test/
    ├── java/com/sqa/linkedin/
    │   ├── base/
    │   │   ├── BaseTest.java                  # Browser lifecycle (@BeforeMethod, @AfterMethod) & auto screenshots
    │   │   └── DriverFactory.java             # Driver initialization (Selenium Manager handles drivers)
    │   │
    │   ├── pages/
    │   │   ├── BasePage.java                  # Base page with explicit wait helpers & resilient element finders
    │   │   ├── LoginPage.java                 # Login page locators & authentication flows
    │   │   ├── FeedPage.java                  # LinkedIn feed & global search interaction
    │   │   └── SearchResultsPage.java         # Search results verification & result navigation
    │   │
    │   ├── tests/
    │   │   ├── LoginTest.java                 # TC-01 (Valid login) & TC-02 (Invalid password)
    │   │   ├── SearchTest.java                # TC-03 (Search verification)
    │   │   └── SearchResultTest.java          # TC-04 (Search result navigation)
    │   │
    │   └── utils/
    │       ├── ConfigReader.java              # Configuration loader (Env variables > config.properties)
    │       └── ScreenshotUtil.java            # Automatic screenshot capture utility
    │
    └── resources/
        ├── config.properties                  # Local credentials file (git-ignored)
        └── config.properties.example          # Sample configuration template
```

---

## Getting Started

### 1. How to Open the Project

#### In Visual Studio Code (Recommended):
1. Open VS Code.
2. Go to **File -> Open Folder...** and select the folder `linkedin-ui-tests`.
3. If prompted to install recommended Java extensions ("Extension Pack for Java"), click **Install**.

#### In IntelliJ IDEA:
1. Open IntelliJ IDEA.
2. Click **Open** or **File -> Open...**.
3. Select `pom.xml` in this directory and click **Open as Project**.

---

### 2. Configure Your Credentials

For security, **credentials are NEVER hardcoded into source code**. You have two options:

#### Option A: Local Properties File (Simplest)
Open `src/test/resources/config.properties` and add your dedicated LinkedIn test credentials:
```properties
linkedin.username=your_test_account@example.com
linkedin.password=your_test_account_password
```
*(Note: `config.properties` is already added to `.gitignore` so your credentials will not be committed to GitHub).*

#### Option B: Environment Variables
Alternatively, you can set environment variables in your terminal:
```powershell
# Windows PowerShell:
$env:LINKEDIN_USERNAME="your_test_account@example.com"
$env:LINKEDIN_PASSWORD="your_test_account_password"
```

---

### 3. How to Run the Tests

#### Method 1: 1-Click Batch Script (Easiest on Windows)
Simply double-click `run_tests.bat` (or run `./run_tests.bat` from PowerShell/CMD).
A menu will appear allowing you to:
1. Run ALL Tests (`testng.xml`)
2. Run ONLY Negative Login Test (TC-02, runs even without credentials)
3. Run ONLY Login Tests (TC-01 & TC-02)
4. Run ONLY Search Test (TC-03)
5. Run ONLY Search Result Click Test (TC-04)
6. Open HTML Test Report in Browser

#### Method 2: Maven Command Line
```powershell
# Set Java 21 & Maven path (if not in system PATH):
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"
$env:PATH = "C:\Program Files\Java\jdk-21\bin;C:\Users\DELL\.m2\wrapper\dists\apache-maven-3.9.16\0daed3be3ebd1c706f0e69e8b07c6b73f5cc4ea3dfce72a8d0ec2e849ca2ddb0\bin;" + $env:PATH

# Run all tests using Chrome (default):
mvn clean test

# Run using Firefox:
mvn clean test -Dbrowser=firefox

# Run a specific test class:
mvn test -Dtest=LoginTest
```

---

## Viewing Test Reports and Screenshots

* **Automated Screenshots:** Every test run automatically captures and timestamps screenshots upon completion (with `PASS_` or `FAIL_` prefixes) in:
  ```
  target/screenshots/
  ```
* **TestNG HTML Report:** Comprehensive TestNG execution reports are generated in:
  ```
  target/surefire-reports/index.html
  ```
  Open this file in Google Chrome or Edge to view execution durations, assertion details, and pass/fail statistics.

---

## Bot Detection, CAPTCHA & Security Ethics
LinkedIn implements active anti-scraping and bot-detection heuristics (such as Arkose Labs puzzles or SMS/email verification).
In strict compliance with the assignment instructions:
* **The test suite never attempts to bypass or hack security checkpoints.**
* The browser runs in **headed (visible) mode** (not headless).
* If a security checkpoint (`/checkpoint`, `/uas/`, or `/authwall`) is detected, the test execution politely pauses for up to **180 seconds** (configurable in `config.properties`), allowing the user to solve the verification challenge manually in the open browser window. Once verified, the suite automatically detects navigation back to LinkedIn and resumes test execution seamlessly.

---

## Test Report PDF Generation
1. Open `Test_Report_IT3153.html` in Google Chrome or Microsoft Edge.
2. Fill in your **Name**, **Index Number**, and **GitHub Repo Link**.
3. Click the **"🖨️ Print to PDF / Save as PDF"** button at the top (or press `Ctrl + P`).
4. Select Destination: **Save as PDF**, set Margins to **Default**, and click **Save**.

---

## Screen Recording Instructions (Deliverable 4)
* Maximum duration: **3 minutes**.
* Use Windows Game Bar (`Win + G` or `Win + Alt + R`) or OBS Studio to record your screen while running `run_tests.bat`.
* Ensure no personal confidential passwords or sensitive details are visible.
