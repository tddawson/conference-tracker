function Point(x, y) 
{
	this.x = x;
	this.y = y;
}


Point.prototype.setX = function (x)
{
	this.x = x;
}

Point.prototype.getX = function()
{
	return this.x;
}


Point.prototype.setY = function (y)
{
	this.y = y;
}

Point.prototype.getY = function()
{
	return this.y;
}


Point.prototype.getColor = function()
{
	return this.color;
}

Point.prototype.setColor = function(color)
{
	this.color = color;
}