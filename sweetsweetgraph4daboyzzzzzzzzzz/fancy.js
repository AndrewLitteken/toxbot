var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var format = d3.format(",d");
var pack = d3.pack()
    .size([width, height])
    .padding(1.5);

//var color = d3.scaleOrdinal(d3.schemeCategory20c);
function rgb(r, g, b){
  return "rgb("+r+","+g+","+b+")";
}

var color = d3.scaleLinear()
    .domain([-1, 0, 1])
    .range(["red", "white", "green"]);


function fclasses(root) {
    var classes = [];

    function recurse(name, node) {
        console.log(node);
        if (node.children) node.children.forEach(function (child) {
            recurse(node.user, child);
        });
        else classes.push({
            className: node.user,
            value: node.messages,
            data: node.data
        });
    }

    recurse(null, root);
    return {
        children: classes
    };
}
function updateData() {

  var root = d3.hierarchy({children: classes})
      .sum(function(d) { return d.messages+1; })
      .each(function(d) {
        if (id = d.data.user) {
          d.id = id;
          d.package = d.data.user;
          d.class = d.data.user;
        }
      });
    console.log(fclasses(root));

  var node = svg.selectAll(".node")
    .data(pack(root).leaves())
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("circle")
      .attr("id", function(d) { return d.id; })
      .attr("r", function(d) { return d.r; })
      .style("fill", function(d) { return color(d.data.toxicity); });

  node.append("clipPath")
      .attr("id", function(d) { return "clip-" + d.id; })
    .append("use")
      .attr("xlink:href", function(d) { return "#" + d.id; });

  node.append("text")
      .attr("clip-path", function(d) { return "url(#clip-" + d.class + ")"; })
    .selectAll("tspan")
    .data(function(d) { return d.data.user.split(/(?=[A-Z][^A-Z])/g); })
    .enter().append("tspan")
      .attr("x", 0)
      .attr("y", function(d, i, nodes) { return 13 + (i - nodes.length / 2 - 0.5) * 10; })
      .text(function(d) { return d; });


  node.append("title")
      .text(function(d) { return d.data.user });

var data = classes;//d3.map(classes, function(d) { return d  }).keys();

var legend = svg.selectAll(".legend")
      .data(data)
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });

      legend.append("rect")
                .attr("x", 0)
                .attr("width", 160)
                .attr("height", 18)
                .style("fill", function (d) { return color(d.toxicity);});

      legend.append("text")
                .attr("x", 11)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "start")
                .text(function (d) { return d.user; });


}
updateData();
