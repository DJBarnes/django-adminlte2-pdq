/**
 * Adjustments to AdminLte to recall sidebar state.
 *
 * This logic must be loaded into the html DOM in a very specific location in order to work properly.
 * Thus, it is separate from the other `extra-features.js` logic.
 *
 * Also, this is not wrapped in a document.ready so that it is executed as soon as
 * possible. The call to this script must follow the body tag for it to execute
 * correctly on the body tag. Putting it in a document.ready will cause a
 * lag that will show the animation running.
 */


// Close the sidebar if they had it closed before.
var sidebarState = sessionStorage.getItem("sidebar-open");
if (sidebarState == 'closed') {
    var body = document.getElementsByTagName
    $("body").addClass("sidebar-collapse");
}


// Remember, locally, if user had sidebar open or closed.
$("body").on("collapsed.pushMenu", function () {
    sessionStorage.setItem("sidebar-open", 'closed');
});
$("body").on("expanded.pushMenu", function () {
    sessionStorage.setItem("sidebar-open", 'open');
});
