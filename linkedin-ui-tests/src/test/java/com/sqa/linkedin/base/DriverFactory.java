package com.sqa.linkedin.base;

import com.sqa.linkedin.utils.ConfigReader;
import org.openqa.selenium.PageLoadStrategy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;

import java.time.Duration;

/**
 * Creates the WebDriver instance with optimal settings for Single Page Applications (LinkedIn).
 * Uses PageLoadStrategy.EAGER to prevent hanging on third-party telemetry/analytics pixels.
 */
public final class DriverFactory {
    private DriverFactory() { }

    public static WebDriver create() {
        String browser = ConfigReader.get("browser", "chrome").toLowerCase();
        WebDriver driver;
        if (browser.equals("firefox")) {
            FirefoxOptions options = new FirefoxOptions();
            options.setPageLoadStrategy(PageLoadStrategy.EAGER);
            driver = new FirefoxDriver(options);
        } else {
            ChromeOptions options = new ChromeOptions();
            options.setPageLoadStrategy(PageLoadStrategy.EAGER);
            options.addArguments("--start-maximized", "--disable-notifications");
            options.addArguments("--remote-allow-origins=*");
            options.addArguments("--no-sandbox");
            options.addArguments("--disable-dev-shm-usage");
            options.addArguments("--disable-blink-features=AutomationControlled");
            driver = new ChromeDriver(options);
        }
        driver.manage().window().maximize();
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
        return driver;
    }
}
