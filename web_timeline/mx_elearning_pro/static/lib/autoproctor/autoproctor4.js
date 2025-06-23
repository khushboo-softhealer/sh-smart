const apSDKVersionNum = '4.1.0';

// This is the configuration file. which will figure out the version of the sdk needed to download.
const apSDKDomain = "https://cdn.autoproctor.co";

(function injectSDK() {
    const query = new URLSearchParams(location.search)
    const apQueryVersionNum = query.get("apQueryVersionNum");
    const apFinalVersionNum = apQueryVersionNum ?? typeof apVersionNum === "undefined" ?  apSDKVersionNum :  apVersionNum;
    let apFinalDomain = apSDKDomain;
    if (typeof apDomain !== 'undefined') {
        apFinalDomain = apDomain;
    }
    const jsUrl = `${apFinalDomain}/autoproctor.${apFinalVersionNum}.min.js`;
    const cssUrl = `${apFinalDomain}/autoproctor.${apFinalVersionNum}.min.css`;
    // Injecting the SDK files into the DOM
    const jsRequest = new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = jsUrl;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });

    const cssRequest = new Promise((resolve, reject) => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = cssUrl;
        link.onload = resolve;
        link.onerror = reject;
        document.head.appendChild(link);
    });
    
    Promise.all([jsRequest, cssRequest]).then(()=> {
        // If we reach this that means we have already downloaded the relavent versions of SDK files
        // Emiting event apLibReady so AutoProctor can be initialaized.
        const apLibReadyEvent = new CustomEvent("apLibReady", {
            detail: {
                statusDetails: "Loaded AP SDK successfully",
                statusCode: 2005,
            },
            bubbles:true,
        })
        window.dispatchEvent(apLibReadyEvent);
    }).catch((err)=> {
        const apLibLoadingFailedEvent = new CustomEvent("apLibLoadingFailed", {
            detail: {
                statusDetails: "Failed to load AP SDK. Please check internet connection and refresh the page to try again.",
            },
            bubbles:true,
        })
        window.dispatchEvent(apLibLoadingFailedEvent);
        alert("Failed to load AutoProctor SDK. Please check your internet connection and refresh the page to try again.")
        location.reload();
    })
})();