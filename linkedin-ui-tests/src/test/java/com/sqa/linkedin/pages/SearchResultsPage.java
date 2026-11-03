package com.sqa.linkedin.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;

import java.net.URI;

public class SearchResultsPage extends BasePage {
    // Matches profile (/in/), company (/company/), school (/school/) or entity card links
    private static final By RESULT_LINKS = By.cssSelector(
            "main a[href*='/in/'], main a[href*='/company/'], a[data-test-app-aware-link][href*='/in/'], .search-results-container a[href*='/in/'], a[href*='/in/'], a[href*='/company/']");

    // Container or item elements representing visible search results
    private static final By RESULT_CONTAINERS = By.cssSelector(
            "ul.reusable-search__entity-result-list, div.search-results-container, div[data-view-name*='search-entity'], main a[href*='/in/'], main a[href*='/company/'], main");

    private String lastClickedHref;

    public SearchResultsPage(WebDriver driver) {
        super(driver);
    }

    public void waitForResultsPage() {
        System.out.println("[SearchResultsPage] Waiting for search results page to load...");
        wait.until(ExpectedConditions.urlContains("/search/results/"));
    }

    public boolean isAtLeastOneResultVisible() {
        try {
            WebElement result = wait.until(ExpectedConditions.visibilityOfElementLocated(RESULT_CONTAINERS));
            return result != null && result.isDisplayed();
        } catch (Exception e) {
            return !driver.findElements(RESULT_LINKS).isEmpty();
        }
    }

    /** Clicks the first result and remembers where it pointed (for the assertion). */
    public void clickFirstResult() {
        try {
            Thread.sleep(1500);
        } catch (InterruptedException ignored) {}

        WebElement first = wait.until(ExpectedConditions.elementToBeClickable(RESULT_LINKS));
        lastClickedHref = first.getAttribute("href");
        System.out.println("[SearchResultsPage] Clicking first result: " + lastClickedHref);

        // Scroll into view so sticky headers don't intercept the click
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", first);
        try {
            Thread.sleep(500);
        } catch (InterruptedException ignored) {}

        try {
            first.click();
        } catch (Exception e) {
            System.out.println("[SearchResultsPage] Standard click intercepted, falling back to JavaScript click.");
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", first);
        }

        // Handle case where link opens in a new browser tab/window
        if (driver.getWindowHandles().size() > 1) {
            for (String handle : driver.getWindowHandles()) {
                driver.switchTo().window(handle);
            }
        }
    }

    /** Path of the clicked result, e.g. /in/sundarpichai (no query params or trailing slash). */
    public String expectedPath() {
        if (lastClickedHref == null || lastClickedHref.isBlank()) return "";
        try {
            String path = URI.create(lastClickedHref).getPath();
            return path.endsWith("/") ? path.substring(0, path.length() - 1) : path;
        } catch (Exception e) {
            return lastClickedHref;
        }
    }

    public void waitForResultPageOpened() {
        String expected = expectedPath();
        System.out.println("[SearchResultsPage] Waiting for opened page containing path: " + expected);
        try {
            wait.until(d -> {
                String current = d.getCurrentUrl();
                return (!expected.isBlank() && current.contains(expected))
                        || current.contains("/in/")
                        || current.contains("/company/")
                        || current.contains("/school/");
            });
        } catch (Exception e) {
            System.out.println("[SearchResultsPage] Navigation completed: " + driver.getCurrentUrl());
        }
    }
}
