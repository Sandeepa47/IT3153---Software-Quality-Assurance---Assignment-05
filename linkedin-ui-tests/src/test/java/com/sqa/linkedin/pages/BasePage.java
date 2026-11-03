package com.sqa.linkedin.pages;

import com.sqa.linkedin.utils.ConfigReader;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * Common helpers for all Page Objects.
 * Uses resilient explicit waits that handle responsive/duplicate DOM elements gracefully.
 */
public abstract class BasePage {
    protected final WebDriver driver;
    protected final WebDriverWait wait;

    protected BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(ConfigReader.getInt("timeout.seconds", 20)));
    }

    /**
     * Waits for and returns the first DISPLAYED element matching the locator.
     * This avoids issues where responsive sites (like LinkedIn) keep a hidden
     * mobile version of the same element in the DOM before the visible desktop one.
     */
    protected WebElement visible(By locator) {
        return wait.until(d -> {
            for (WebElement el : d.findElements(locator)) {
                try {
                    if (el.isDisplayed()) {
                        return el;
                    }
                } catch (Exception ignored) {
                }
            }
            return null;
        });
    }

    /** Waits for and returns the first DISPLAYED and ENABLED element matching the locator. */
    protected WebElement clickable(By locator) {
        return wait.until(d -> {
            for (WebElement el : d.findElements(locator)) {
                try {
                    if (el.isDisplayed() && el.isEnabled()) {
                        return el;
                    }
                } catch (Exception ignored) {
                }
            }
            return null;
        });
    }

    protected void type(By locator, String text) {
        WebElement el = visible(locator);
        el.click();
        // Clear using Control+A and Backspace to work reliably with React-controlled inputs
        el.sendKeys(Keys.chord(Keys.CONTROL, "a"), Keys.BACK_SPACE);
        el.sendKeys(text);
    }

    protected void click(By locator) {
        clickable(locator).click();
    }
}
