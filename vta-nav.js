const { Builder, By, until } = require("selenium-webdriver");

findRoute = async function(rNum, station) {
    // Open the browser
    let driver = await new Builder().forBrowser("chrome").build();
    // Saves the result of the function
    let url = "";
    try {
        // Navigate to the VTA routes webpage
        await driver.get("https://www.vta.org/go/routes");
        // Fill in the route name
        const routeSearch = await driver.findElement(By.id("edit-route-search"));
        await routeSearch.sendKeys(rNum);
        // Click the apply button
        await routeSearch.click();
        // So far, the  user has navigated to a page that shows various routes based on keyword
        // Click the desired route
        await driver.findElement(By.xpath(`//*[contains(text(), '${rNum}')]`)).click();
        // Choose the departing station from the options available
        const selectElement = await driver.findElement(By.id("edit-origin"));
        await selectElement.click();
        await selectElement.findElement(By.xpath(`//*[contains(text(), '${station}')]`)).click();
        await driver.findElement(By.id("edit-submit")).click();
        // Save the url
        url = await driver.getCurrentUrl();  
    }
    finally {
        // Close the browser and get the url with the desired route
        await driver.quit();
        console.log(url)
    }
}

findRoute(process.argv[2], process.argv[3]);