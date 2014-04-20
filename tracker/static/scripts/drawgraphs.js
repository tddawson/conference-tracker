$(document).ready(function() {
	var ratios = $('.completion-ratio');
	$.each(ratios, function( index, div ) {
		progressBar(index, div);
		//pieChart(index,div);
	});

});


function progressBar(index, div) {
	var s = $(div).html().split("/");	
	var complete = parseInt(s[0]);
	var total = parseInt(s[1]);
	var percent = parseInt(100 * complete / total);

	var bar = $('.progress-tracker:eq(' + index + ')');//.get(index);
	bar.width(percent + "%");
	bar.attr('data-content', percent + "%");
}

function pieChart(index, div) {
	var s = $(div).find('span').html().split("/");
	var canvas = document.getElementsByTagName('canvas')[index];

	var complete = parseInt(s[0]);
	var incomplete = parseInt(s[1]) - complete;
		
	drawPieChart(canvas, complete, incomplete);

}

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