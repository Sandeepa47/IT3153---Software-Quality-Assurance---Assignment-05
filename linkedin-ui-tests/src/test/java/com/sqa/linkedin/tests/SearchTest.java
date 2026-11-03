package com.sqa.linkedin.tests;

import com.sqa.linkedin.base.BaseTest;
import com.sqa.linkedin.pages.FeedPage;
import com.sqa.linkedin.pages.SearchResultsPage;
import com.sqa.linkedin.utils.ConfigReader;
import org.testng.Assert;
import org.testng.annotations.Test;

public class SearchTest extends BaseTest {

    @Test(description = "TC-03 Global search shows a results page")
    public void searchShouldShowResults() {
        FeedPage feed = loginAsValidUser();
        Assert.assertTrue(feed.isLoaded());

        SearchResultsPage results = feed.searchFor(ConfigReader.get("search.term", "software testing"));

        results.waitForResultsPage();
        Assert.assertTrue(driver.getCurrentUrl().contains("/search/results/"), "URL should be a search results URL");
        Assert.assertTrue(results.isAtLeastOneResultVisible(), "At least one result should be visible");
        com.sqa.linkedin.utils.ScreenshotUtil.capture(driver, "Task3_Search_Results_Page");
    }
}
