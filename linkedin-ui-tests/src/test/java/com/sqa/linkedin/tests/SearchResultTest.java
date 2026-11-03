package com.sqa.linkedin.tests;

import com.sqa.linkedin.base.BaseTest;
import com.sqa.linkedin.pages.FeedPage;
import com.sqa.linkedin.pages.SearchResultsPage;
import com.sqa.linkedin.utils.ConfigReader;
import org.testng.Assert;
import org.testng.annotations.Test;

public class SearchResultTest extends BaseTest {

    @Test(description = "TC-04 Clicking the first result opens the matching page")
    public void firstResultShouldOpenCorrectPage() {
        FeedPage feed = loginAsValidUser();
        Assert.assertTrue(feed.isLoaded(), "Feed page should be loaded");

        SearchResultsPage results = feed.searchFor(ConfigReader.get("search.click.term", "Sundar Pichai"));
        results.waitForResultsPage();
        Assert.assertTrue(results.isAtLeastOneResultVisible(), "Search results should be displayed");

        results.clickFirstResult();
        results.waitForResultPageOpened();

        String url = driver.getCurrentUrl();
        boolean hasExpectedPath = !results.expectedPath().isBlank() && url.contains(results.expectedPath());
        boolean isProfileOrCompany = url.contains("/in/") || url.contains("/company/") || url.contains("/school/");
        Assert.assertTrue(hasExpectedPath || isProfileOrCompany,
                "Opened URL should contain expected path or profile/company. Actual URL: " + url);
        Assert.assertTrue(driver.getTitle().length() > 0, "Page title should be populated");
        com.sqa.linkedin.utils.ScreenshotUtil.capture(driver, "Task4_Target_Result_Page");
    }
}
