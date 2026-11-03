package com.sqa.linkedin.tests;

import com.sqa.linkedin.base.BaseTest;
import com.sqa.linkedin.pages.FeedPage;
import com.sqa.linkedin.pages.LoginPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class LoginTest extends BaseTest {

    @Test(priority = 1, description = "TC-01 Valid login lands on the feed")
    public void validLoginShouldOpenFeed() {
        FeedPage feed = loginAsValidUser();
        Assert.assertTrue(feed.isLoaded(), "Feed page should be loaded");
        Assert.assertTrue(driver.getCurrentUrl().contains("/feed"), "URL should contain /feed");
        Assert.assertTrue(feed.isSearchBoxVisible(), "Search box should be visible");
        com.sqa.linkedin.utils.ScreenshotUtil.capture(driver, "Task2_Positive_Feed_Page");
    }

    @Test(priority = 2, description = "TC-02 Invalid password shows an error")
    public void invalidPasswordShouldShowError() {
        // If user credentials are not configured, use a test email to still verify negative flow
        String testUser = username().isBlank() ? "sqa.invalid.user@example.com" : username();
        LoginPage login = new LoginPage(driver).open();
        login.enterCredentialsAndSubmit(testUser, "Wrong#Password_123!");
        Assert.assertTrue(login.isErrorMessageDisplayed(), "An error message should be displayed");
        Assert.assertTrue(driver.getCurrentUrl().contains("login") || driver.getCurrentUrl().contains("checkpoint"),
                "Should remain on the login or checkpoint page");
        com.sqa.linkedin.utils.ScreenshotUtil.capture(driver, "Task2_Negative_Password_Error");
    }
}
