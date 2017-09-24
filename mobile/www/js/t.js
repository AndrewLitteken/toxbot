var format = d3.format(",d");
var width = 600;
var height = 1000;

var color = d3.scaleLinear()
    .domain([-1, 0, 1])
    .range(["red", "white", "green"]);
//var color = function(){return "rgb(122,122,122)"};

var bubble = d3.layout.pack()
    .sort(null)
    .size([width, height])
    .padding(10);

var svg = d3.select("#chart").append("svg")
    .attr("viewBox", "0 0 "+width+" "+height)
    .attr("preserveAspectRatio","xMinYMin meet")
    .attr("class", "bubble")
    .attr("font-family", "sans-serif")
    .attr("font-size", "16")
    .attr("text-anchor", "middle");

var root = {
    "children": []
};

var node = svg.selectAll(".node")
    .data(bubble.nodes(classes(root))
    .filter(function (d) {
    return !d.children;
}))
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", function (d) {
    return "translate(" + d.x + "," + d.y + ")";
});

node.append("title")
    .text(function (d) {
    return d.className;
});

node.append("circle")
    .attr("r", function (d) {
    return d.r;
})
    .style("fill", function (d, i) {
    return color(d.toxicity);
})
    .style("stroke-width", function() { return "5px"; })
    .style("stroke", function() { return "black"; })



// Returns a flattened hierarchy containing all leaf nodes under the root.

function classes(root) {
    var classes = [];

    function recurse(name, node) {
        if (node.children) node.children.forEach(function (child) {
            recurse(node.name, child);
        });
        else classes.push({
            packageName: name,
            className: node.name,
            value: node.size,
            toxicity: node.toxicity
        });
    }

    recurse(null, root);
    return {
        children: classes
    };
}

//d3.select(self.frameElement).style("height", diameter + "px");


//My Refer;
var click = 0;

function changevalues() {
    click++;
    if (click == 1) changebubble(root2);
    else if (click == 2) changebubble(root3);
    else changebubble(root4);

}

//update function
function changebubble(root) {
    var node = svg.selectAll(".node")
        .data(
            bubble.nodes(classes(root)).filter(function (d){return !d.children;}),
            function(d) {return d.className} // key data based on className to keep object constancy
        );
    
    // capture the enter selection
    var nodeEnter = node.enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    
    // re-use enter selection for circles
    nodeEnter
        .append("circle")
        .attr("r", function (d) {return d.r;})
        .style("fill", function (d, i) {return color(d.toxicity);})
        .style("stroke-width", function() { return "5px"; })
        .attr("stroke", function() { return "black"; })
        .on("click", function(e) {
            fill_in_username(e.className);
         })
        /*.on("onmouseout", function() {
           d3.select(this)
      	  .transition()
      	  .duration(1000)
      	  .attr('stroke','black')
         })
        */
    
    // re-use enter selection for titles
    nodeEnter
        .append("title")
        .text(function (d) {
            return d.className;
        });
/*
  nodeEnter.append("clipPath")
      .attr("id", function(d) { return "clip-" + d.className; })
    .append("use")
      .attr("xlink:href", function(d) { return "#" + d.className; });
*/
      nodeEnter.append("text")
      .style("font-size", function(d) { return Math.min(2 * d.r, (2 * d.r - 8) / d.className.length ) + "px"; })
      .attr("clip-path", function(d) { return "url(#clip-" + d.class + ")"; })
    .selectAll("tspan")
    .data(function(d) { return [d.className.split(/(?=[A-Z][^A-Z])/g)[0]]; })
    .enter().append("tspan")
      .attr("x", 0)
      .attr("y", function(d, i, nodes) { return 13 + (i - nodes.length / 2 - 0.5) * 10; })
      .text(function(d) { return d; })
    
    node.select("circle")
        .transition().duration(1000)
        .attr("r", function (d) {
            return d.r;
        })
        .style("fill", function (d, i) {
            return color(d.toxicity);
        })

    node.transition().duration(300).attr("class", "node")
        .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    }).select("text").duration(1000)
      .style("font-size", function(d) { return Math.min(2 * d.r, (2 * d.r - 8) / d.className.length ) + "px"; })

    node.exit().remove();

    // Returns a flattened hierarchy containing all leaf nodes under the root.
    function classes(root) {
        var classes = [];

        function recurse(name, node) {
            if (node.children) node.children.forEach(function (child) {
                recurse(node.name, child);
            });
            else classes.push({
                packageName: name,
                className: node.name,
                value: node.size,
                toxicity: node.toxicity
            });
        }

        recurse(null, root);
        return {
            children: classes
        };
    }

    //d3.select(self.frameElement).style("height", diameter + "px");
}
