package com.sqa.linkedin.utils;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.util.Properties;

/**
 * Reads settings. Priority: environment variable (LINKEDIN_USERNAME) >
 * JVM system property (-Dlinkedin.username=...) > config.properties.
 * Credentials are therefore never hard-coded in source code.
 */
public final class ConfigReader {
    private static final Properties PROPS = new Properties();

    static {
        try (InputStream in = ConfigReader.class.getClassLoader().getResourceAsStream("config.properties")) {
            if (in != null) {
                PROPS.load(in);
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private ConfigReader() { }

    public static String get(String key, String defaultValue) {
        String env = System.getenv(key.toUpperCase().replace('.', '_'));
        if (env != null && !env.isBlank()) return env;
        String sys = System.getProperty(key);
        if (sys != null && !sys.isBlank()) return sys;
        return PROPS.getProperty(key, defaultValue);
    }

    public static int getInt(String key, int defaultValue) {
        return Integer.parseInt(get(key, String.valueOf(defaultValue)).trim());
    }
}
