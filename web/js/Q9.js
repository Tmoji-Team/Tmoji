// set the dimensions and margins of the graph
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 900 - margin.left - margin.right,
    height = 720 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#try9")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

//Read the data
d3.csv("https://raw.githubusercontent.com/Tmoji-Team/Tmoji/master/web/test_data/q9_test.csv", function(data) {

  extent_x = d3.extent(data, d => d.x)
  extent_y = d3.extent(data, d => d.y)
  extent_num = d3.extent(data, d => d.num)
  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, extent_x[1]])
    .range([ 0, width ]);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([0, extent_y[1]])
    .range([ height, 0]);
  svg.append("g")
    .call(d3.axisLeft(y));

  // Add a scale for bubble size
  var z = d3.scaleLinear()
    .domain([1, extent_num[1]])
    .range([ 1, 20]);

  // Add dots
  svg.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x(d.x); } )
      .attr("cy", function (d) { return y(d.y); } )
      .attr("r", function (d) { return z(d.num); } )
      .style("fill", "#ff6619")
      .style("opacity", "0.7")
      .attr("stroke", "#ffd5b0")
      .attr("stroke-width", "2px")
      
})