/**
 * Follow the browser's light or dark mode.
 *
 * Swaps the body's skin class for the one in data-skin-light or data-skin-dark, based on the
 * browser's prefers-color-scheme setting, and again whenever that setting changes. Not wrapped in
 * a document.ready, so it runs before the page is drawn. It must be loaded right after the body tag.
 */
(function () {
    var body = document.body;
    var lightClass = body.getAttribute('data-skin-light');
    var darkClass = body.getAttribute('data-skin-dark');
    var currentClass = body.getAttribute('data-skin-current');
    if (!lightClass || !darkClass || !window.matchMedia) {
        return;
    }

    var darkQuery = window.matchMedia('(prefers-color-scheme: dark)');

    function applySkin() {
        var wantedClass = darkQuery.matches ? darkClass : lightClass;
        if (wantedClass === currentClass) {
            return;
        }
        if (currentClass) {
            body.classList.remove(currentClass);
        }
        body.classList.add(wantedClass);
        body.setAttribute('data-skin-current', wantedClass);
        currentClass = wantedClass;
    }

    applySkin();
    if (darkQuery.addEventListener) {
        darkQuery.addEventListener('change', applySkin);
    } else if (darkQuery.addListener) {
        // Safari before 14.
        darkQuery.addListener(applySkin);
    }
})();
