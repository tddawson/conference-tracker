$(document).ready(function() {
	var ratios = $('.completion-ratio');
	$.each(ratios, function( index, div ) {
		var s = $(div).find('span').html().split("/");
		var canvas = document.getElementsByTagName('canvas')[index];

		var complete = parseInt(s[0]);
		var incomplete = parseInt(s[1]) - complete;
		
		drawPieChart(canvas, complete, incomplete);
	});

});


function drawPieChart(canvas, complete, incomplete)
{
	var graph = new PieChart();
	graph.attachCanvas(canvas);

	var dataSet = new DataSet();
	graph.addDataSet(dataSet);

	var pComplete = new Point("Completed", complete);
	pComplete.setColor("#6ca");
	dataSet.addPoint(pComplete);

	var pIncomplete = new Point("Not Completed", incomplete);
	pIncomplete.setColor("#F2EFEC");
	dataSet.addPoint(pIncomplete);

	graph.draw();
}