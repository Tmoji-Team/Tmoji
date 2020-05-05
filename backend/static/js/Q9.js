function q9(data, selector) {
var margin9 = {top: 10, right: 20, bottom: 30, left: 50},
    width9 = 500 - margin9.left - margin9.right,
    height9 = 420 - margin9.top - margin9.bottom;

// append the svg object to the body of the page
var svg9 = d3.select(selector)
  .append("svg")
    .attr("idth9 width", width9 + margin9.left + margin9.right)
    .attr("height", height9 + margin9.top + margin9.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin9.left + "," + margin9.top + ")");

  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, 20])
    .range([ 0, width9 ]);
  svg9.append("g")
    .attr("transform", "translate(0," + height9 + ")")
    .call(d3.axisBottom(x));

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([0, 20])
    .range([ height9, 0]);
  svg9.append("g")
    .call(d3.axisLeft(y));

  // Add a scale for bubble size
  var z = d3.scaleLinear()
    .domain([1, 400000])
    .range([ 1, 400000]);

  // Add dots
  svg9.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x(d.x); } )
      .attr("cy", function (d) { return y(d.y); } )
      .attr("r", function (d) { return z(d.num); } )
      .style("fill", "#69b3a2")
      .style("opacity", "0.7")
      .attr("stroke", "black")
      
}