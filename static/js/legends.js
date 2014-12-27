// Legends specific javascript


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
    
    buttons.live('click',
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

//        var ladder_re = /.*_(\[a-zA-Z]+)/;
//
//        var ladder_name = link.match(ladder_re)[1];
//        
//        if (ladder_name == 'legends')
//        {
//            var round_re = /(\d+)/;
//            var round_id = link.match(round_re)[1];
//            var id = 'gviz_ladder_' + round_id;
//
//            var table = new Table(document.getElementById(id));
//            var data_table = new google.visualization.DataTable(data, 0.6);
//            var options = {
//                           showRowNumber : true,
//                           allowHtml : true,
//        //                   sortAscending : false,
//        //                   sortColumn : 10,
//                           sort : 'event'
//                          };
//
//            table.draw(data_table, options);
//        }
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

/*** Form procesing ***/

function display_errors(errors) {
    $(".form_errors").empty();
    for (var key in errors) {
        var field = errors[key];
        var error_msg = '<ul class="form_error">';
        for(var i=0; i < field.length; i++) {
            error_msg += '<li>' + field[i] + '</li>';
        }
        error_msg += '</ul>'
        $('.form_errors').append(error_msg);
    }
}

$(function() {
    $(".fancybox").fancybox({
        autoSize      : true,
        helpers : {
            overlay : null,
        },
    });

    $('#login_form').submit(function(){
        submit_login($(this));
        return false;
    });

    function submit_login(form) {
        var link = 'http://' + document.location.host + '/accounts/login';
        var csrfmiddlewaretoken = form.find('input[name$="csrfmiddlewaretoken"]');
        var username = form.find('input[name$="username"]');
        var password = form.find('input[name$="password"]');

        var fields = {
            'csrfmiddlewaretoken' : csrfmiddlewaretoken,
            'username': username,
            'password': password,
        };

        var request_data = {}
        for (var key in fields) {
            request_data[key] = fields[key].val();
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
                    display_errors(response.errors);
                }
            }
        });
    }

    $('#change_password_form').submit(function(){
        submit_change_password($(this));
        return false;
    });

    function submit_change_password(form) {
        link = 'http://' + document.location.host + '/accounts/change_password';
        var csrfmiddlewaretoken = form.find('input[name$="csrfmiddlewaretoken"]');
        var old_password = form.find('input[name$="old_password"]');
        var new_password1 = form.find('input[name$="new_password1"]');
        var new_password2 = form.find('input[name$="new_password2"]');

        var fields = {
            'csrfmiddlewaretoken' : csrfmiddlewaretoken,
            'old_password': old_password,
            'new_password1': new_password1,
            'new_password2': new_password2,
        };

        var request_data = {}
        for (var key in fields) {
            request_data[key] = fields[key].val();
        };

        // Construct POST request
        $.ajax({
            type: 'POST',
            url: link,
            data: request_data,
            dataType: 'json',
            success: function(response) {
                if (response.changed == true) {
                    var msg = '<p>Your password has been changed.</p>';
                    $('#change_password').replaceWith(msg);
                }
                else {
                    display_errors(response.errors);
                }
            }
        });
    }
    // Pop up score details
//    $('td.season_results_score').click(function() {
//        var id_parts = $(this).attr('id').split('_');
//        var link = 'http://' + document.location.host + '/legends/stats/scores/' + id_parts[1] + '/' + id_parts[2] + '/';
//        $('#score_detail').load(link);
//        $('#score_detail').click();
//    });
});

