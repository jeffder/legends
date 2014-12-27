/**
 * A wrapper for a chart visualization.
 *
 * For more info see:
 * http://code.google.com/apis/visualization/documentation/gallery/table.html
 */


/**
 * Constructs a new chart wrapper for the specified container and tableOptions.
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
var VizChartWrapper = function(container, data, options, selected, linked_to) {

    this.viz_type = 'chart'

    this.container = container;
    this.data_table = new google.visualization.DataTable(data, 0.6);

    options = options || {};
    options = VizChartWrapper.clone(options);

    this.options = options;
    this.initial_selection = selected || null;
    this.linked_to = linked_to || null;

    this.viz = new google.visualization.LineChart(this.container);
    
    var self = this;

//    google.visualization.events.addListener(this.viz,
//                                            'select',
//                                            function() {self.handle_select()});

    // Build an array of column IDs
    var columns = [];
    for (var idx = 0; idx < this.data_table.getNumberOfColumns(); idx++)
    {
        columns.push(this.data_table.getColumnId(idx));
    }

    this.chart_columns = columns;
};

/**
 * Draws the Chart visualization in the container.
 */
VizChartWrapper.prototype.draw = function() {

    this.viz.draw(this.data_table, this.options);
};


/* Performs a shallow clone of the given object. */
VizChartWrapper.clone = function(obj) {
    
    var new_obj = {};
    
    for (var key in obj) {
        new_obj[key] = obj[key];
    }
    
    return new_obj;
};


VizChartWrapper.prototype.get_column_index = function(column, obj)
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
 * Get the linked table's current selection.
 */
VizChartWrapper.prototype.get_new_selection = function(obj)
{
    // obj is a table visualisation

    var selection = obj.getSelection();

    // Get the name of each selected club
    var dt = obj.view || obj.data_table;
    var club_index = obj.get_column_index('club', dt);
    var selected_clubs = [];
    $.each(selection,
           function(idx, club)
           {
               selected_clubs.push(dt.getValue(club.row, club_index));
           });

    // Map the rows in the linked selection to columns in the chart table
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
                              });

    return obj_selection;
}

