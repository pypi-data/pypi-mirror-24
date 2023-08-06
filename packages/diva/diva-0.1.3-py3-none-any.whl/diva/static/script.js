// reportId is a string like "report-0", "report-1", ...
function changeTab(reportId) {
    // hide all report tabs
    $('.report-tab').css('display', 'none');

    // display the components for the desired tab
    $('.' + reportId).css('display', 'block');
}

$(document).ready(function() {
    // setup the buttons in report dropdown menu
    $('.report-option').on('click', function() {
        var reportId = $(this).attr('value');
        changeTab(reportId);
    });
        
    // init all reports
    var reportElements = $('.report');
    reportElements.each(function(index) {
        var reportElement = $(this);
        var report = Reports.create();
        
        // setup the report's user-defined widgets
        var widgetElements = $('#widgetform-' + index).find('.user-widgets').children();
        widgetElements.each(function() {
            // extract name and type from the widget's outer div
            // , which is of class widgetcontainer (see index.html)
            var element = $(this);
            var widgetType = element.data('widget-type');
            // setup a widget of the requested type, and add to report
            var setupFunc = Reports.Widgets.setupMap[widgetType];
            var widget = setupFunc(element);
            report.widgets.add(widget);
        });
    });

    // open the first tab
    $('.report-option').first().trigger('click');
});
