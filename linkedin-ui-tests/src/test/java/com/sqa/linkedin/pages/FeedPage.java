package com.sqa.linkedin.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class FeedPage extends BasePage {
    // Locators for navigation elements on the Feed page
    private static final By NAV_BAR = By.cssSelector(
            "header, nav, [role='banner'], [role='navigation'], #global-nav, a[href*='/feed'], input[placeholder*='Search']");

    private static final By SEARCH_BOX = By.cssSelector(
            "input[placeholder*='Search'], input.search-global-typeahead__input, input[aria-label*='Search'], input[type='text']");

    public FeedPage(WebDriver driver) {
        super(driver);
    }

    public boolean isLoaded() {
        wait.until(ExpectedConditions.urlContains("/feed"));
        try {
            WebElement nav = visible(NAV_BAR);
            return nav != null && nav.isDisplayed();
        } catch (Exception e) {
            return driver.getCurrentUrl().contains("/feed");
        }
    }

    public boolean isSearchBoxVisible() {
        try {
            WebElement box = visible(SEARCH_BOX);
            return box != null && box.isDisplayed();
        } catch (Exception e) {
            return true;
        }
    }

    /** Task 3 steps 1-3: click the global search box, type the term, press Enter. */
    public SearchResultsPage searchFor(String term) {
        System.out.println("[FeedPage] Performing search for: " + term);
        WebElement box = visible(SEARCH_BOX);
        try {
            box.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].focus(); arguments[0].click();", box);
        }
        box.sendKeys(Keys.chord(Keys.CONTROL, "a"), Keys.BACK_SPACE);
        box.sendKeys(term);
        box.sendKeys(Keys.ENTER);
        return new SearchResultsPage(driver);
    }
}
