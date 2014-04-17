/**
A generic object that can be graphed by an object that inherits from Graph.
*/
function DataSet()
{
	this.label = "";
	this.points = [];
	this.color = "#000000";
	this.lineWidth = 1;
	this.maxX = 0;
	this.maxY = 0;
}

// Should sort it as it goes, too.
DataSet.prototype.addPoint = function(point)
{
	if (!(point instanceof Point))
		throw Error("TYPE ERROR: Object adding to DataSet points must be of type Point.");

	this.points.push(point);

	this.maxX = Math.max(point.getX(), this.maxX);
	this.maxY = Math.max(point.getY(), this.maxY);
}

DataSet.prototype.getPoints = function()
{
	return this.points;
}

DataSet.prototype.getPoint = function(index)
{
	if (index >= this.points.length)
		throw Error("OUT OF BOUNDS ERROR: Index " + index + " is out of bounds of points.")

	return this.points[index];
}

DataSet.prototype.getLastPoint = function()
{
	return this.getPoint(this.points.length - 1);
}

DataSet.prototype.clearPoints = function()
{
	this.points = [];
	this.maxX = 0;
	this.maxY = 0;
}

DataSet.prototype.getLabel = function()
{
	return this.label;
}

DataSet.prototype.setLabel = function(label)
{
	if (typeof label != "string")
		throw Error("TYPE ERROR: DataSet label must be of type string.");

	this.label = label;
}

DataSet.prototype.getLineWidth = function()
{
	return this.lineWidth;
}

DataSet.prototype.setLineWidth = function(lineWidth)
{
	if (typeof lineWidth != "number")
		throw Error("TYPE ERROR: lineWidth must be a number.");

	this.lineWidth = lineWidth;
}

DataSet.prototype.setColor = function(color)
{
	if (typeof color != "string")
		throw Error("TYPE ERROR: DataSet label must be of type string.");

	this.color = color;
}

DataSet.prototype.getColor = function() 
{
	return this.color;
}

DataSet.prototype.getMaxX = function()
{
	return this.maxX;
}

DataSet.prototype.getMaxY = function()
{
	return this.maxY;
}