


// create the svg area
var svg = d3.select("#Q2-content")
  .append("svg")
    .attr("width", 440)
    .attr("height", 440)
  .append("g")
    .attr("transform", "translate(220,220)")

// create a matrix
var NameProvider = ["Apple","HTC","Huawei","LG","Nokia","Samsung","Sony","Other"];

var matrix = [
  [2,  1, 8, 9],
  [ 1, 9, 5, 5],
  [ 5, 5, 5, 5],
  [ 8, 15,  15, 2]
];

// give this matrix to d3.chord(): it will calculates all the info we need to draw arc and ribbon
var res = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending)
    (matrix)

// Add the links between groups
svg
  .datum(res)
  .append("g")
  .selectAll("path")
  .data(function(d) { return d; })
  .enter()
  .append("path")
    .attr("d", d3.ribbon()
      .radius(190)
    )
    .style("fill", "#69b3a2")
    .style("stroke", "black");

// this group object use each group of the data.groups object
var group = svg
  .datum(res)
  .append("g")
  .selectAll("g")
  .data(function(d) { return d.groups; })
  .enter()

// add the group arcs on the outer part of the circle
group.append("g")
    .append("path")
    .style("fill", "grey")
    .style("stroke", "black")
    .attr("d", d3.arc()
      .innerRadius(190)
      .outerRadius(200)
    )

// Add the ticks
group
  .selectAll(".group-tick")
  .data(function(d) { return groupTicks(d, 1); })    // Controls the number of ticks: one tick each 25 here.
  .enter()
  .append("g")
    .attr("transform", function(d) { return "rotate(" + (d.angle * 180 / Math.PI - 90) + ") translate(" + 200 + ",0)"; })
  .append("line")               // By default, x1 = y1 = y2 = 0, so no need to specify it.
    .attr("x2", 6)
    .attr("stroke", "black")

// Add the labels of a few ticks:
group
  .selectAll(".group-tick-label")
  .data(function(d) { return groupTicks(d, 1); })
  .enter()
  .filter(function(d) { return d.value % 25 === 0; })
  .append("g")
    .attr("transform", function(d) { return "rotate(" + (d.angle * 180 / Math.PI - 90) + ") translate(" + 200 + ",0)"; })
  .append("text")
    .attr("x", 8)
    .attr("dy", ".35em")
    .attr("transform", function(d) { return d.angle > Math.PI ? "rotate(180) translate(-16)" : null; })
    .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
    .text(function(d) { return d.value })
    .style("font-size", 9)



// Returns an array of tick angles and values for a given group and step.
function groupTicks(d, step) {
  var k = (d.endAngle - d.startAngle) / d.value;
  return d3.range(0, d.value, step).map(function(value) {
    return {value: value, angle: value * k + d.startAngle};
  });
}