package com.sqa.linkedin.utils;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public final class ScreenshotUtil {
    private static final Path DIR = Paths.get("target", "screenshots");

    private ScreenshotUtil() { }

    public static Path capture(WebDriver driver, String name) {
        try {
            Files.createDirectories(DIR);
            byte[] bytes = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            String ts = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            Path file = DIR.resolve(name + "_" + ts + ".png");
            Files.write(file, bytes);
            System.out.println("[Screenshot] " + file.toAbsolutePath());
            return file;
        } catch (IOException | RuntimeException e) {
            System.out.println("[Screenshot] could not capture: " + e.getMessage());
            return null;
        }
    }
}
