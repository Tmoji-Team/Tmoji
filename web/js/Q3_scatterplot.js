// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 40, left: 50},
    width = 520 - margin.left - margin.right,
    height = 520 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#Q3-content")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")")

// Add the grey background that makes ggplot2 famous
svg
  .append("rect")
    .attr("x",0)
    .attr("y",0)
    .attr("height", height)
    .attr("width", height)
    .style("fill", "EBEBEB")

//Read the data
d3.csv("https://raw.githubusercontent.com/Tmoji-Team/Tmoji/master/web/test_data/q3_test.csv", function(data) {

  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, 1])
    .range([ 0, width ]);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([0, 1])
    .range([ height, 0]);

  svg.append("g")
    .call(d3.axisLeft(y));


  // Add X axis label:
  svg.append("text")
      .attr("text-anchor", "end")
      .attr("x", width/2 + margin.left)
      .attr("y", height + margin.top + 20)
      .text("Upper case %");

  // Y axis label:
  svg.append("text")
      .attr("text-anchor", "end")
      .attr("transform", "rotate(-90)")
      .attr("y", -margin.left + 20)
      .attr("x", -margin.top - height/2 + 20)
      .text("Lower case %")


  // // Add dots
  // svg.append('g')
  //   .selectAll("dot")
  //   .data(data)
  //   .enter()
  //   .append("circle")
  //     .attr("cx", function (d) { return x(d.Upper); } )
  //     .attr("cy", function (d) { return y(d.Lower); } )
  //     .attr("r", 1.5)
  //     .style("fill", "#69b3a2");

  //Add text
  svg.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("text")
      .attr("dx", function (d) { return x(d.Upper); } )
      .attr("dy", function (d) { return y(d.Lower); } )
      .text(function(d) { return d.emoji });


})
