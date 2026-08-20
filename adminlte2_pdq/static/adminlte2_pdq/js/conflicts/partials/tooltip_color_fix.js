/***
 * Resolve issue in newer version of AdminLTE where the tooltip color is always default white/grey.
 */


$(function () {

    /**
     * Attempts to get element using relevant selector.
     * Attempts periodically until hits timeout.
     * Necessary for some dynamically generated elements,
     * if they aren't yet on the DOM when we try to call
     * logic on them.
     *
     * Core logic from https://stackoverflow.com/a/29754070
     * @param selector Class identifier for element.
     * @param callback Function to execute on find.
     * @param checkFrequencyInMs How often to check.
     * @param timeoutInMs How long before giving up.
     */
    function waitForElementToDisplay(selector, callback, checkFrequencyInMs, timeoutInMs) {
      var startTimeInMs = Date.now();
      (function loopSearch() {
        var foundElement = document.body.getElementsByClassName(selector);
        if (foundElement != null && foundElement.length > 0) {
          callback(foundElement);
          return;
        }
        else {
          setTimeout(function () {
            if (timeoutInMs && Date.now() - startTimeInMs > timeoutInMs)
              return;
            loopSearch();
          }, checkFrequencyInMs);
        }
      })();
    }

    var colorClass = "";

    // Bind to hover start.
    $(".label").on("mouseenter", function () {

        // Attempt to get from tooltip property.
        colorClass = $(this).data("tooltip-color");
        if (colorClass == null || colorClass === "") {
            // Failed to get by tooltip data. Attempt by class.
            var elementCssClasses = $(this).attr("class").toString();
            elementCssClasses = elementCssClasses.toString().split(" ");

            // Loop through each css class to try to find our desired one.
            elementCssClasses.forEach( function(item, index) {

                // Check if starts with "tooltip-".
                if ( item.toString().match("^tooltip-") ) {
                    // If we find a prefix match, assume is our intended color.
                    item = item.replace("tooltip-", "");
                    colorClass = item;
                }
            });
        }

        // Apply color to tooltip.
        if (colorClass != null && colorClass !== "") {
            colorClass = "tooltip-" + colorClass;

            // Wait until tooltip exists.
            waitForElementToDisplay("tooltip",function(item){

                // Check if has leftover hover data. Can happen if user moves mouse between labels fast enough.
                if ( $(item).data("tooltip-color") ) {

                    // Get old value.
                    var oldData = $(item).data("tooltip-color");
                    // Make sure old class is removed.
                    $(item).removeClass(oldData);
                }

                // Add class attr to tooltip.
                $(item).addClass(colorClass);

                // Add data attr, for easy removal on hover exit.
                $(item).data("tooltip-color", colorClass);

            // Check every 50 ms, waiting up to a full second.
            },50,1000);

        }
    });

});
