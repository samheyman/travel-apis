// import { csv } from "./bundle.js";

const renderMostTraveled = data => {
  const svg = d3.select("#most_traveled");
  const height = +svg.attr("height");
  const width = +svg.attr("width");
  const xValue = d => d.travels;
  const yValue = d => d.destination;
  const margin = { top: 20, right: 20, bottom: 20, left: 40 };
  const innerHeight = height - margin.top - margin.bottom;
  const innerWidth = width - margin.left - margin.right;

  const xScale = d3
    .scaleLinear()
    .domain([0, d3.max(data, xValue)])
    .range([0, innerWidth]);

  const yScale = d3
    .scaleBand()
    .domain(data.map(yValue))
    .range([0, innerHeight])
    .padding(0.1);

  const yAxis = d3.axisLeft(yScale);

  const g = svg
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.right})`);

  // yAxis(g.append("g")); or rather:
  g.append("g").call(d3.axisLeft(yScale));
  g.append("g")
    .call(d3.axisBottom(xScale))
    .attr("transform", `translate(0,${innerHeight})`);

  g.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("y", d => yScale(yValue(d)))
    .attr("width", d => xScale(xValue(d)))
    .attr("height", yScale.bandwidth());
};

// d3.csv(most_travelled_data).then(data => {
//   data.forEach(element => {
//     element.travels = +element.travels;
//   });
renderMostTraveled(JSON.parse(most_traveled_data).data);

// renderMostTraveled(data);
// });
