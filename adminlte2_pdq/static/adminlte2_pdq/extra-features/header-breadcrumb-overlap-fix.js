/**
 * When the Page Header (block "page_name") value is long, it can sometimes overlap with the page breadcrumbs.
 * This appears to be an issue with original AdminLTE2, but is still probably undesired behavior.
 *
 * This JS checks the size of each, plus the size of the parent, and sets them to have their own lines if they overlap.
 */

// Limit scope of visibility.
// Don't want this affecting outside JS logic from projects that import this package.
$(function () {

    // Required to calculate text size.
    // From https://stackoverflow.com/a/15302051.
    $.fn.textWidth = function(text, font) {
        if (!$.fn.textWidth.fakeEl) $.fn.textWidth.fakeEl = $('<span>').hide().appendTo(document.body);
        $.fn.textWidth.fakeEl.text(text || this.val() || this.text()).css('font', font || this.css('font'));
        return $.fn.textWidth.fakeEl.width();
    };

    console.log('Loaded header-breadcrumb-overlap-fix.js');

    let page_header_element = $('section.content-header > h1:first-child');
    console.log($(page_header_element));
    console.log($(page_header_element).textWidth());
    let page_header_width = $(page_header_element).textWidth();
    console.log(page_header_width);

    let breadcrumb_element = $('section.content-header > ol.breadcrumb');
    console.log($(breadcrumb_element));
    console.log($(breadcrumb_element).width());
    let breadcrumb_width = $(breadcrumb_element).width()

    console.log('');
    let content_header_section = $('section.content-header');
    console.log('Total content size: ' + (page_header_width + breadcrumb_width));
    console.log('Content header size: ' + $(content_header_section).width());
    if ( $(content_header_section).width() <= (page_header_width + breadcrumb_width)) {
        // Width overlaps. Correct by setting breadcrumb element to have mobile-handling.
        console.log('OVERLAPS!');

        // Set CSS for overall breadcrumb element.
        $(breadcrumb_element).css('position', 'relative');
        $(breadcrumb_element).css('top', '0');
        $(breadcrumb_element).css('right', '0');
        $(breadcrumb_element).css('float', 'none');
        $(breadcrumb_element).css('padding-left', '10px');
        $(breadcrumb_element).css('background', '#d2d6de');

        // Set CSS for inner breadcrumb elements.
        // Due to :before elements, we have to do this with a custom CSS class.
        $(breadcrumb_element).children('li:not(:eq(0))').each(function() {
            $(this).addClass('header-fix');
        });

    } else {
        console.log('Is okay.');
    }

});