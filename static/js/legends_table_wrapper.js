/**
 * A wrapper for a table visualization.
 * The object allows sorting by multiple columns for some sort columns. The sort
 * is initially done in descending order.
 *
 * For more info see:
 * http://code.google.com/apis/visualization/documentation/gallery/table.html
 */


/**
 * Constructs a new table wrapper for the specified container and tableOptions.
 *
 * Note: The wrapper clones the options object to adjust some of its properties.
 * In particular:
 *         sort {string} set to 'event'.
 *         showRowNumber {boolean} set to true.
 *         sortAscending {boolean} set according to the current sort.
 *         sortColumn {number} set according to the given sort.
 */

/** @constructor
 */
var VizTableWrapper = function(container, data, options, selected, multi_keys, linked_to)
{
    this.viz_type = 'table'

    this.container = container;
    this.data_table = new google.visualization.DataTable(data, 0.6);

    options = options || {};
    options = VizTableWrapper.clone(options);

//    options['sort'] = 'event';
//    options['showRowNumber'] = true;
    
    this.options = options;
    this.initial_selection = selected || null;
    this.multi_sort_keys = multi_keys || [];
    this.linked_to = linked_to || null;

    this.viz = new google.visualization.Table(this.container);
    
    var self = this;

    google.visualization.events.addListener(this.viz,
                                            'sort',
                                            function(e) {self.handle_sort(e)});
    google.visualization.events.addListener(this.viz,
                                            'select',
                                            function() {self.handle_select()});

    // Build an array of column IDs
    var columns = [];
    for (var idx = 0; idx < this.data_table.getNumberOfColumns(); idx++)
    {
        columns.push(this.data_table.getColumnId(idx));
    }

    this.table_columns = columns;

    // Remember the sort order for each column so that we can reverse the order
    // next time we sort with this column. Add the first key in multi_keys to
    // avoid repeating the original sort order on the first click.
    this.last_sort_order = {};
    var first_index = $.inArray(this.multi_sort_keys[0], this.table_columns);
    this.last_sort_order[first_index] = true;
};

/**
 * Draws the Table visualization in the container.
 */
VizTableWrapper.prototype.draw = function()
{

    this.viz.draw(this.data_table, this.options);
};


/** Handles a sort event with the given properties. */
VizTableWrapper.prototype.handle_sort = function(properties)
{
  
    var column_index = properties['column'];
    var is_ascending = false;

    // Switch the sort order from the last time we sorted with this column
    if (this.last_sort_order[column_index] == null)
    {
        is_ascending = properties['ascending'];
    }
    else
    {
        is_ascending = !this.last_sort_order[column_index];
    }

    // Remember this sort order so that we can switch next time
    this.last_sort_order[column_index] = is_ascending;

    this.options['sortColumn'] = column_index;
    this.options['sortAscending'] = is_ascending;

    // See if we're doing a multi-column sort
    var sort_columns = [];
    var dt = this.data_table;
    if (dt.getColumnId(column_index) == this.multi_sort_keys[0])
    {
        for (var idx = 0; idx < this.multi_sort_keys.length; idx++)
        {
            key = this.multi_sort_keys[idx];
            sort_columns.push({column : $.inArray(key, this.table_columns),
                               desc : is_ascending});
        }
    }
    else
    {
        sort_columns = [{column : column_index, desc : is_ascending}];
    }
    
    view = new google.visualization.DataView(this.data_table);
    view.setRows(view.getSortedRows(sort_columns));

    // Preserve the current selection before we draw the table
    selection = this.get_new_selection(view);

    this.viz.setSelection(selection);

    this.view = view;

    this.viz.draw(view, this.options);
    
};


/**
 * Handles a select event.
 * We need to find the row(s) matching the selected club(s) since the streaks
 * table and the linked table are unlikely to be sorted in the same order.
 * Note that the 'club' column will be common to both tables.
 */
VizTableWrapper.prototype.handle_select = function()
{
   
    if (this.linked_to.viz_type == 'table')
    {
        dt = this.linked_to.view || this.linked_to.data_table;

        selection = this.get_new_selection(dt);
        
        this.linked_to.viz.setSelection(selection);
    }
//    else
//    {
//        selection = this.linked_to.set_new_selection(this.viz.getSelection());
//        
//        this.linked_to.viz.setSelection(selection);
//    }

};


/* Performs a shallow clone of the given object. */
VizTableWrapper.clone = function(obj)
{
    
    var new_obj = {};
    
    for (var key in obj) {
        new_obj[key] = obj[key];
    }
    
    return new_obj;
};


VizTableWrapper.prototype.get_column_index = function(column, obj)
{
    // Get the index of column in obj
    
    for (idx = 0; idx < obj.getNumberOfColumns(); idx++)
    {
        if (obj.getColumnId(idx) == column)
        {
            return idx;
        }
    }
}


/**
 * Map the table's current selection to rows in another table or view.
 * Arguments: obj is a DataView or DataTable instance
 */
VizTableWrapper.prototype.get_new_selection = function(obj)
{

    var selection = this.viz.getSelection();

    // Get the name of each selected club
    var dt = this.view || this.data_table;
    var club_index = this.get_column_index('club', dt);
    var selected_clubs = [];
    $.each(selection,
           function(idx, club)
           {
               selected_clubs.push(dt.getValue(club.row, club_index));
           });

    // Map the rows in the linked selection to rows in the streak table
    var obj_club_index = this.get_column_index('club', obj);
    var rows = range(obj.getNumberOfRows());
    var obj_selection = $.map(rows,
                              function(club, idx)
                              {
                                  var name = obj.getValue(club, obj_club_index);
                                  if ($.inArray(name, selected_clubs) >= 0)
                                  {
                                      return {row : club};
                                  }
 
                                  return null;
                              }) || [];

    return obj_selection;
}


