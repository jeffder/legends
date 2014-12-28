// Legends specific javascript

// Show tips/results for selected game
function show_tips(button)
    /*
     *   Show tips and results for selected game in games list.
     */

{

}
function expand_collapse(button, hidden)
{
    /*
     *   Toggle display of hidden rows and update button label
     *   when a button is clicked
    */
   
    action = button.html();

    if (action == 'Show')
    {
        hidden.show();
        button.html('Hide');
    }
    else
    {
        hidden.hide();
        button.html('Show');
    }
}


function bind_click_to_expand_collapse(buttons, expand_part)
{
    /*
     * Bind the click event to expand/collapse elements in tab pane tables.
    */
    
    buttons.live(
        'click',
         function(evnt)
         {
             evnt.preventDefault();
             var hidden = $(expand_part, $(this).parents().filter('table')[0]);
             expand_collapse($(this), hidden);
             //return false;
         });
}


function prepare_ajax_form(form)
{
    form.live('submit', function(evnt)
    {
        evnt.preventDefault();

        var request_context = $(this).parent('div');

        $.ajax(
        {
            url : $(this).attr('action'),
            type : $(this).attr('method'),
            data : $(this).serialize(),
            dataType : 'html',
            context : $(request_context),
            beforeSend : function(request)
            {
                request_context.fadeOut(800);
            },
            success : function(response, status, xhr)
            {
                request_context.html(response);
                request_context.fadeIn(800);
            }
        });
    });
}


function update_ladder_tabs()
{
    // Update the ladder tabs after results are submitted

    var new_tab = $('ul.ladder_round_tabs li.hidden:first');
    new_tab.removeClass('hidden');
    
    var initial_index = $('ul.ladder_round_tabs li').index(new_tab) - 1;
    
    // Remove the existing ladder tabs
    $("ul.ladder_round_tabs").removeData("tabs");
    $("ul.ladder_tabs").removeData("tabs");
    
    // Recreate the tabs
    $("ul.ladder_round_tabs").tabs("div.ladder_round_panes > div",
                                   {
                                      initialIndex: initial_index
                                   });
    
    $("ul.ladder_tabs").tabs("div.ladder_panes > div",
                             {
                              initialIndex: 0,
                              effect: 'ajax'
                             });
}   


function update_tip_tabs()
{
    // Update the tip tabs and the tipping deadline after results are submitted

    // Update the tipping deadline
    var request_context = $('#deadline');
    var link = 'view_deadline/';

    $.ajax(
    {
        url : link,
        context : request_context,
        dataType : 'html',
        success : function(html)
        {
            request_context.html(html);
        }
    });

    // Update the tip tabs
    var new_tab = $('ul.tips_tabs li.hidden:first');
    new_tab.removeClass('hidden');
    
    var initial_index = $('ul.tips_tabs li').index(new_tab) - 1;
    
    // Remove the existing ladder tabs
    $("ul.tips_tabs").removeData("tabs");
    
    // Recreate the tabs
    $("ul.tips_tabs").tabs("div.tips_panes > div",
                           {
                              initialIndex: initial_index,
                              effect: 'ajax'
                           });
}   


function ladder_header_click()
{
    // Make a tags in ladder headers clickable

    a_tags = $('div.ladder th a');
    
    a_tags.live('click', function(evnt)
    {
        evnt.preventDefault();
    
        var request_context = $(this).parents().filter('div.ladder_content');
        var link = $(this).attr('href');

        $.ajax(
        {
            url : link,
            context : request_context,
            dataType : 'html',
            success : function(html)
            {
                request_context.html(html);
            }
        });
    });
}


function range(start, stop, step)
{
    // The equivalent of Python's range function.
    // It only works with integers

    arr = [];

    switch(arguments.length)
    {
        case 0:
            return [];

        case 1:
            begin = 0;
            end = arguments[0];
            skip = 1;
            break;

        case 2:
            begin = arguments[0];
            end = arguments[1];
            skip = 1;
            break;

        default:
            begin = arguments[0];
            end = arguments[1];
            skip = arguments[2];
            break;
    }

    if (begin > end)
    {
        skip *= -1;
    }

    for (i = begin; i < end; i += skip)
    {
        arr.push(i);
    }

    return arr;
}

/*** Form processing ***/

function set_validation_styles(obj, is_valid) {
    var group = obj.parent();
    var span = obj.next();

    if (is_valid == true) {
        if (group.hasClass('has-error')) {
            group.removeClass('has-error');
        }
        if (!group.hasClass('has-success')) {
            group.addClass('has-success');
        }
        if (span.hasClass('glyphicon-remove')) {
            span.removeClass('glyphicon-remove');
        }
        if (!span.hasClass('glyphicon-ok')) {
            span.addClass('glyphicon-ok');
        }
    }
    else {
        if (group.hasClass('has-success')) {
            group.removeClass('has-success');
        }
        if (!group.hasClass('has-error')) {
            group.addClass('has-error');
        }
        if (span.hasClass('glyphicon-ok')) {
            span.removeClass('glyphicon-ok');
        }
        if (!span.hasClass('glyphicon-remove')) {
            span.addClass('glyphicon-remove');
        }
    }
}

function submit_login(form) {
    var link = 'http://' + document.location.host + '/accounts/login';

    var request_data = {
        'csrfmiddlewaretoken': form.find('input[name$="csrfmiddlewaretoken"]').val(),
        'username': form.find('input[name="username"]').val(),
        'password': form.find('input[name="password"]').val()
    };

    // Construct POST request
    $.ajax({
        type: 'POST',
        url: link,
        data: request_data,
        dataType: 'json',
        success: function(response) {
            if (response.logged_in == true) {
                window.location.reload();
            }
            else {
                // Set validation styles
                set_validation_styles($('#username'), false);
                set_validation_styles($('#password'), false);
            }
        }
    });
}

function submit_change_password(form) {
    var link = 'http://' + document.location.host + '/accounts/change_password';

    var request_data = {
        'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
        'old_password': form.find('input[name="old_password"]').val(),
        'new_password1': form.find('input[name="new_password1"]').val(),
        'new_password2': form.find('input[name="new_password2"]').val()
    };

    // Construct POST request
    $.ajax({
        type: 'POST',
        url: link,
        data: request_data,
        dataType: 'json',
        success: function(response) {
            if (response.changed == true) {
                set_validation_styles($('#old-password'), true);
                set_validation_styles($('#new-password1'), true);
                set_validation_styles($('#new-password2'), true);
            }
            else {
                // Set validation styles
                if ('old_password' in errors) {
                    set_validation_styles($('#old-password'), false);
                }
                else {
                    set_validation_styles($('#old-password'), true);
                }
                if ('new_password2' in errors) {
                    set_validation_styles($('#new-password1'), false);
                    set_validation_styles($('#new-password2'), false);
                }
                else {
                    set_validation_styles($('#new-password1'), true);
                    set_validation_styles($('#new-password2'), true);
                }
            }
        }
    });
}


