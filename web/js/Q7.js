var margin_7 = {top: 100, right: 0, bottom: 0, left: 0},
    width = 460 - margin_7.left - margin_7.right,
    height = 460 - margin_7.top - margin_7.bottom,
    //width = 256
    //height = 256

    innerRadius = 90,
    outerRadius = Math.min(width, height) / 2;   // the outerRadius goes from the middle of the SVG area to the border

// append the svg object
var svg = d3.select("#try7")
  .append("svg")
    .attr("width", width + margin_7.left + margin_7.right)
    .attr("height", height + margin_7.top + margin_7.bottom)
  .append("g")
    .attr("transform", "translate(" + (width / 2 + margin_7.left) + "," + (height / 2 + margin_7.top) + ")");

var data = [{
  "Emoji": "hoge",
  "Value": "100"
}, {
  "Emoji": "hellow",
  "Value": " 312"
}, {
  "Emoji": "world",
  "Value": " 222"
}, {
  "Emoji": "fuga",
  "Value": " 254"
}];
// d3.csv("https://raw.githubusercontent.com/Tmoji-Team/Tmoji/master/web/test_data/q7_test.csv", function(data) {
//   console.log(data)

  // Scales
var x = d3.scaleBand()
    .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
    .align(0)                  // This does nothing
    .domain(data.map(function(d) { return d.Emoji; })); // The domain of the X axis is the list of states.
var y = d3.scaleRadial()
    .range([innerRadius, outerRadius])   // Domain will be define later.
    .domain([0, 14000]); // Domain of Y is from 0 to the max seen in the data

// Add the bars
svg.append("g")
  .selectAll("path")
  .data(data)
  .enter()
  .append("path")
    .attr("fill", "#69b3a2")
    .attr("d", d3.arc()     // imagine your doing a part of a donut plot
        .innerRadius(innerRadius)
        .outerRadius(function(d) { return y(d['Value']); })
        .startAngle(function(d) { return x(d.Emoji); })
        .endAngle(function(d) { return x(d.Emoji) + x.bandwidth(); })
        .padAngle(0.01)
        .padRadius(innerRadius));

// Add the labels
svg.append("g")
    .selectAll("g")
    .data(data)
    .enter()
    .append("g")
      .attr("text-anchor", function(d) { return (x(d.Emoji) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
      .attr("transform", function(d) { return "rotate(" + ((x(d.Emoji) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d['Value'])+10) + ",0)"; })
    .append("text")
      .text(function(d){return(d.Emoji)})
      .attr("transform", function(d) { return (x(d.Emoji) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
      .style("font-size", "11px")
      .attr("alignment-baseline", "middle");

// });