const { Builder, By, until } = require("selenium-webdriver");

async function findRoute(rNum, direction) {
    // Open the browser
    let driver = await new Builder().forBrowser("chrome").build();
    // Saves the result of the function
    let url = "";
    try {
        // Navigate to the VTA routes webpage
        await driver.get("https://www.vta.org/go/routes");
        // Fill in the route name
        const x = await driver.findElement(By.id("edit-route-search"));
        x.sendKeys(rNum);
        // Click the apply button
        await driver.findElement(By.id("edit-submit-routes")).click();
        // So far, the  user has navigated to a page that shows various routes based on keyword
        // Click the desired route
        await driver.findElement(By.xpath(`//*[contains(text(), '${rNum}')]`)).click();
        // Click in the direction and during what time in the week the user wants to go
        await driver.findElement(By.xpath(`//*[contains(text(), '${direction}')]`)).click(); 
        url = await driver.getCurrentUrl();   
    }
    finally {
        // Close the browser and return the url with the desired route
        //await driver.quit();
        return url;
    }
}