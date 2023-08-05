exports.config = {
    framework: 'jasmine',
    capabilities: {
        'browserName': 'chrome',
    },
    specs: [
        './e2e/cls.e2e-spec.js',
        './e2e/options.e2e-spec.js',
    ],
    seleniumServerJar: './node_modules/selenium-server-standalone-jar/jar/selenium-server-standalone-3.4.0.jar',
}
