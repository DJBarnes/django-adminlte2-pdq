/**
 * TODO: Split these up into separate files if they're separate features.
 *  Otherwise, at least document them better.
 */


$(function () {
    // Click the first child found
    // This makes it easier to click checkboxes by clicking the parent element
    $('.click-pass-through').click(function (e) {
        if (e.target !== this) {
            return; // Clicked on a child, we only care about parent
        }
        var child = $(e.target).children().first()

        if (child) {
            child.click();
        }
    });

    // Toggle a row, and it's content
    $('.toggle-visible').click(function (e) {
        var target = $(this).data('toggle-target');
        var content = $(this).data('toggle-content');
        if (target === undefined) {
            console.log("WARNING: data-toggle-target wasn't found.");
            return;
        }
        if (content === undefined) {
            console.log("WARNING: data-toggle-content wasn't found.");
            return;
        }

        // get the current visible status
        var isVisible = $(target).is(':visible');

        // reverse the visibility
        if (isVisible) {
            $(content).slideUp('fast');
            $(target).hide('fast');
            $(this).html('►');
        } else {
            $(target).show('fast');
            $(content).slideDown('fast');
            $(this).html('▼');
        }
    });

    var tableCollapse = function () {
        // Private vars
        var _rows, _speed, _elementSpeed, _animateExpand, _animateCollapse;
        _rows = [];
        _speed = 500;

        // Recursive function to animate expansion one row at a time
        _animateExpand = function () {
            // Base case
            if (_rows === undefined || _rows.length == 0) {
                return;
            }

            // Get the row to operate on.
            var row = _rows.shift();

            // Restore the top and bottom padding from the td / th elements in the row
            $(row)
                .find('td, th')
                .removeClass('remove-top-bottom-padding');
            // Animate the divs that are in each td / th element and then setup
            // a promise to remove the divs and recursively start the next row
            // after all of the animation in this current row is done.
            $(row)
                .find('div')
                .slideDown(_elementSpeed)
                .promise().done(
                    function () {
                        var div_elements = $(row).find('div');
                        $.each(div_elements, function (index, div) {
                            $(div).replaceWith($(div).contents());
                        });
                        _animateExpand();
                    }
                );
            return;
        };
        // Recursive function to animate collapse one row at a time
        _animateCollapse = function () {
            // Base case
            if (_rows === undefined || _rows.length == 0) {
                return;
            }
            // Pop the row off the list of rows
            var row = _rows.pop();

            // Remove the top and bottom padding on the td / th elements
            $(row)
                .find('td, th')
                .addClass('remove-top-bottom-padding');
            // Animate the divs that are in each td / th element and then setup
            // a promise to remove the divs and recursively start the next row
            // after all of the animation in this current row is done.
            $(row)
                .find('div')
                .slideUp(_elementSpeed)
                .promise().done(
                    function () {
                        // Replace the divs with the div's content.
                        var div_elements = $(row).find('div');
                        $.each(div_elements, function (index, div) {
                            $(div).replaceWith($(div).contents());
                        });
                        // Hide the row
                        $(row).hide();
                        // Restore the padding
                        $(row).find('td, th')
                            .removeClass('remove-top-bottom-padding');
                        // Recursively call collapse.
                        _animateCollapse();
                    }
                );
            return;
        };
        return {
            // Public function to expand a Queryset of trs.
            expand: function (tableContent, speed = 500) {
                // Set overall speed
                _speed = speed;
                // Build row array
                $.each($(tableContent), function (index, value) {
                    _rows.push(value);
                });
                // Calculate the speed
                _elementSpeed = Math.floor(_speed / _rows.length);
                // Remove padding, and wrap all tds in divs that can be animated
                $(tableContent)
                    .find('td, th')
                    .addClass('remove-top-bottom-padding')
                    .wrapInner('<div style="display:none;"></div>');
                $(tableContent).show();
                // Call the recursive expand function
                _animateExpand();
            },
            // Public function to collapse a Queryset of trs.
            collapse: function (tableContent, speed = 500) {
                // Set overall speed
                _speed = speed;
                // Build row array
                $.each($(tableContent), function (index, value) {
                    _rows.push(value);
                });
                // Calculate the element speed
                _elementSpeed = Math.floor(_speed / _rows.length);
                // Insert divs to each td.
                $(tableContent)
                    .find('td, th')
                    .wrapInner('<div></div>');
                // Call the recursive collapse function
                _animateCollapse();
            },
        }
    }();

    // Toggle a row, and it's target
    $('.toggle-tr-visible').click(function (e) {
        var target = $(this).data('toggle-target');
        if (target === undefined) {
            console.log("WARNING: data-toggle-target wasn't found.");
            return;
        }

        // Get the current visible status
        var isVisible = $(target).is(':visible');

        // reverse the visibility
        if (isVisible) {

            // Fix any children
            var children = $('[data-toggle-parent="' + target + '"]');
            $.each(children, function (index, value) {
                var childTargetSelector = $(value).data('toggle-target');
                var childTarget = $(childTargetSelector);
                if ($(childTarget).is(':visible')) {
                    $(value).click();
                }
            });

            // Collapse the trs
            tableCollapse.collapse($(target));
            // Change the arrow
            $(this).html('►');
        } else {
            // Expand the trs
            tableCollapse.expand($(target));
            // Change the arrow
            $(this).html('▼');
        }
    });

    // Updates the text input with the filename of the selected file if
    // when the user selects a file.
    //
    // Setup a change listener on the file input change that will trigger
    // a fileselect event that will be handled by the code below.
    $(document).on('change', ':file', function () {
        var input = $(this),
            numFiles = input.get(0).files ? input.get(0).files.length : 1,
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [numFiles, label]);
    });
    // We can watch for our custom `fileselect` event like this
    $(':file').on('fileselect', function (event, numFiles, label) {
        var input = $(this).parents('.input-group').find(':text'),
            output = numFiles > 1 ? numFiles + ' files selected' : label;
        if (input.length) {
            input.val(output);
        } else {
            if (output) {
                alert(output);
            }
        }
    });

    // Allow for clicking tree text and using actual link instead of animation.
    $(document).on('click', '.sidebar-menu li a', function (e) {
        var target = $(e.target);
        var anchor = $(e.currentTarget);
        // If the actual icon for the caret was clicked, find the parent span containing the icon.
        if (e.target.tagName.toLowerCase() === 'i' && target.hasClass('fa-angle-left')) {
            target = target.closest('.treeview-caret');
        }
        if (!target.hasClass('treeview-caret')) {
            e.stopPropagation();
            var href = anchor.attr('href');
            if (href !== undefined && href !== '' && href !== '#') {
                window.location.href = href;
            }
        }
    });
});
