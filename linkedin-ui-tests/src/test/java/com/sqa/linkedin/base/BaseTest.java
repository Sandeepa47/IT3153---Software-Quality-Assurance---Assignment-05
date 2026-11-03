package com.sqa.linkedin.base;

import com.sqa.linkedin.pages.FeedPage;
import com.sqa.linkedin.pages.LoginPage;
import com.sqa.linkedin.utils.ConfigReader;
import com.sqa.linkedin.utils.ScreenshotUtil;
import org.openqa.selenium.WebDriver;
import org.testng.ITestResult;
import org.testng.SkipException;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

/** Starts a fresh browser before every test and closes it afterwards. */
public abstract class BaseTest {
    protected WebDriver driver;

    @BeforeMethod(alwaysRun = true)
    public void setUp() {
        driver = DriverFactory.create();
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown(ITestResult result) {
        if (driver == null) return;
        // Automatic screenshot for every test; prefix tells pass/fail (used in the report)
        String prefix = result.getStatus() == ITestResult.SUCCESS ? "PASS_" : "FAIL_";
        ScreenshotUtil.capture(driver, prefix + result.getMethod().getMethodName());
        driver.quit();
    }

    protected String username() { return ConfigReader.get("linkedin.username", ""); }

    protected String password() { return ConfigReader.get("linkedin.password", ""); }

    /** Logs in with the credentials from config / env vars and returns the feed page. */
    protected FeedPage loginAsValidUser() {
        if (username().isBlank() || password().isBlank()) {
            throw new SkipException("Credentials not configured. See README.md");
        }
        LoginPage loginPage = new LoginPage(driver);
        loginPage.open();
        return loginPage.loginWithValidUser(username(), password());
    }
}
