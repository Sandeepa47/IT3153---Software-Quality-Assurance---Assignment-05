package com.sqa.linkedin.pages;

import com.sqa.linkedin.utils.ConfigReader;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.net.URI;
import java.time.Duration;

public class LoginPage extends BasePage {
    // Robust locators: LinkedIn uses dynamic React IDs, so we use standard attribute selectors with fallbacks
    private static final By USERNAME = By.cssSelector(
            "input[autocomplete='username'], input[type='email'], #username, input[name='session_key']");

    private static final By PASSWORD = By.cssSelector(
            "input[autocomplete='current-password'], input[type='password'], #password, input[name='session_password']");

    private static final By SIGN_IN = By.xpath(
            "//button[normalize-space(.)='Sign in'] | //button[@type='submit'] | //button[not(contains(., 'Microsoft')) and not(contains(., 'Apple')) and contains(., 'Sign in')]");

    // Multiple fallbacks: LinkedIn displays errors under the field, inline, or inside an alert banner
    private static final By ERROR = By.cssSelector(
            "#error-for-password, #error-for-username, div[role='alert'], .form__label--error, [data-test-form-alert], .alert-content, .artdeco-inline-feedback--error, p.form__sub-header, div[data-testid*='error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage open() {
        String url = ConfigReader.get("base.url", "https://www.linkedin.com") + "/login";
        System.out.println("[LoginPage] Navigating to: " + url);
        driver.get(url);
        visible(USERNAME);
        return this;
    }

    public LoginPage enterCredentialsAndSubmit(String user, String pass) {
        System.out.println("[LoginPage] Entering username/email...");
        type(USERNAME, user);
        System.out.println("[LoginPage] Entering password...");
        type(PASSWORD, pass);

        WebElement submitBtn = clickable(SIGN_IN);
        System.out.println("[LoginPage] Scrolling Sign In button into view...");
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center'});", submitBtn);
        System.out.println("[LoginPage] Clicking Sign In button...");
        try {
            submitBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", submitBtn);
        }
        return this;
    }

    /** Positive flow: submit, handle a possible manual checkpoint, return the feed page. */
    public FeedPage loginWithValidUser(String user, String pass) {
        enterCredentialsAndSubmit(user, pass);
        waitForManualCheckpointIfAny();
        return new FeedPage(driver);
    }

    /** Negative flow: stays on the login page with an error message. */
    public boolean isErrorMessageDisplayed() {
        try {
            WebElement errorEl = visible(ERROR);
            return errorEl != null && errorEl.isDisplayed();
        } catch (TimeoutException e) {
            String url = driver.getCurrentUrl();
            return url.contains("login") || url.contains("checkpoint");
        }
    }

    public String getErrorMessageText() {
        try {
            return visible(ERROR).getText();
        } catch (Exception e) {
            return "";
        }
    }

    /**
     * Ethics rule: we NEVER try to bypass a CAPTCHA / security checkpoint.
     * If LinkedIn shows an actual verification challenge, the test pauses and waits
     * until the human solves it in the open browser window.
     */
    private void waitForManualCheckpointIfAny() {
        try {
            // Wait until navigation leaves the /login page
            wait.until(d -> {
                String path = pathOf(d);
                return !path.equals("/login") && !path.equals("/login/");
            });
        } catch (TimeoutException e) {
            return;
        }

        if (isCheckpointPath(pathOf(driver))) {
            int seconds = ConfigReader.getInt("manual.checkpoint.seconds", 180);
            System.out.println("[LoginPage] ⚠️ Security checkpoint / CAPTCHA challenge detected!");
            System.out.println("[LoginPage] Please complete it manually in the opened browser window within " + seconds + "s...");
            new WebDriverWait(driver, Duration.ofSeconds(seconds)).until(d -> !isCheckpointPath(pathOf(d)));
            System.out.println("[LoginPage] Checkpoint passed successfully. Continuing test execution.");
        }
    }

    private static boolean isCheckpointPath(String path) {
        // Only actual challenge/authwall pages are true checkpoints, not normal form submission endpoints
        return (path.contains("/checkpoint/challenge") || path.contains("/authwall")) && !path.contains("/login-submit");
    }

    private static String pathOf(WebDriver d) {
        try {
            return URI.create(d.getCurrentUrl()).getPath();
        } catch (Exception e) {
            return "";
        }
    }
}
