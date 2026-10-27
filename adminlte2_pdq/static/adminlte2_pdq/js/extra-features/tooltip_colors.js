/**
 * Colored tooltips.
 *
 * Add a `tooltip-{color}` class, or a `data-tooltip-color="{color}"` attribute, to an
 * element that has a Bootstrap tooltip. AdminLTE creates tooltips inside <body> instead of
 * next to the element, so this copies the color class onto each tooltip as Bootstrap
 * inserts it. The colors themselves are in css/extra-colors/extra-colors.css.
 */
$(document).on('inserted.bs.tooltip', function (event) {
    var element = $(event.target);
    var tooltip = element.data('bs.tooltip');
    if (!tooltip) {
        return;
    }

    var color = element.data('tooltip-color');
    if (!color) {
        var match = (element.attr('class') || '').match(/(?:^|\s)tooltip-([\w-]+)/);
        color = match ? match[1] : null;
    }

    var tip = tooltip.tip();
    tip.removeClass(function (index, className) {
        return (className.match(/(?:^|\s)tooltip-[\w-]+/g) || []).join(' ');
    });
    if (color) {
        tip.addClass('tooltip-' + color);
    }
});
