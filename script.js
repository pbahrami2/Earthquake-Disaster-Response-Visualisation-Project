// Mapping from location IDs to their names
const locationNames = {
    "1": "PALACE HILLS",
    "2": "NORTHWEST",
    "3": "OLD TOWN",
    "4": "SAFE TOWN",
    "5": "SOUTHWEST",
    "6": "DOWNTOWN",
    "7": "WILSON FOREST", 
    "8": "SCENIC VISTA",
    "9": "BROADVIEW",
    "10": "CHAPPARAL",
    "11": "TERRAPIN SPRINGS",
    "12": "PEPPER MILL",
    "13": "CHEDDARFORD",
    "14": "EASTON",
    "15": "WESTON",
    "16": "SOUTHTON",
    "17": "OAK WILLOW",
    "18": "EAST PARTON",
    "19": "WEST PARTON"
};

// Load data and process it
d3.csv("mc1-reports-data-cleaned.csv").then(function(data) {
    aggregateAndVisualizeData(data);
});

// Function to create a vertical gradient legend for damage levels on the map with roman numerals
function createLegend() {
    const legendHeight = 300; // Height of the gradient legend
    const legendWidth = 20;   // Width of the gradient legend

    // Container for the gradient legend
    const legend = d3.select('#legend')
                     .style('height', `${legendHeight}px`)
                     .style('width', `${legendWidth}px`)
                     .style('background', 'linear-gradient(to top, #f03b20, #feb24c, #fed976, #ffeda0, #ffffcc, #ccc)')
                     .style('position', 'absolute')
                     .style('right', '1000px')
                     .style('top', '200px');

    // Create an array of damage levels and their corresponding Roman numerals
    const damageLevels = [
        { level: 'X', value: 0 },
        { level: 'VIII', value: 2 },
        { level: 'VI', value: 4 },
        { level: 'IV', value: 6 },
        { level: 'II', value: 8 },
        { level: '0', value: 10 }
    ];

    // Append text labels for each damage level
    damageLevels.forEach(damage => {
        legend.append('div')
            .attr('class', 'legend-label')
            .style('position', 'absolute')
            .style('width', `${legendWidth}px`)
            .style('text-align', 'left')
            .style('left', `${legendWidth + 5}px`) // Adjust the position of the labels
            .style('top', `${(1 - damage.value / 10) * legendHeight - 10}px`) // Position the label based on the value
            .text(damage.level);
    });
}

// Function to append hospital icons at specific locations








// Aggregate data for visualization
function aggregateAndVisualizeData(data) {
    const aggregateData = {};
    data.forEach(d => {
        const location = d.location; 
        const time = d.time.split(' ')[0];
        if (!aggregateData[location]) {
            aggregateData[location] = {};
        }
        if (!aggregateData[location][time]) {
            aggregateData[location][time] = {
                sewer_and_water: 0,
                power: 0,
                roads_and_bridges: 0,
                medical: 0,
                buildings: 0,
                shake_intensity: 0,
                count: 0
            };
        }
        // Sum up reports for each category per location and time
        aggregateData[location][time].sewer_and_water += (+d.sewer_and_water || 0);
        aggregateData[location][time].power += (+d.power || 0);
        aggregateData[location][time].roads_and_bridges += (+d.roads_and_bridges || 0);
        aggregateData[location][time].medical += (+d.medical || 0);
        aggregateData[location][time].buildings += (+d.buildings || 0);
        aggregateData[location][time].shake_intensity += (+d.shake_intensity || 0);
        aggregateData[location][time].count += 1;
    });

    // Load and display the SVG map
    d3.xml("map.svg").then((xml) => {
        document.getElementById("map").appendChild(xml.documentElement);
        appendLocationNames();
        appendHospitalIcons(); 
        appendNuclearIcons();
        initializeSelectors(data, aggregateData);
        createIconLegend();
        createLegend();
    });
}

function appendHospitalIcons() {
    const hospitalLocations = ["1", "3", "5", "6", "9", "11", "16"];
    const hospitalIconSVG = `data:image/svg+xml;base64,${btoa(`<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="20px" height="20px" viewBox="0 0 512 512" xml:space="preserve">
        <style type="text/css"><![CDATA[.st0{fill:#000000;}]]></style>
        <g><path class="st0" d="M373.328,138.672V0H138.672v138.672H0V512h208V366.438h96V512h208V138.672H373.328z M131.469,414.188H91.406v-47.766h40.063V414.188z M131.469,308.188H91.406v-47.766h40.063V308.188z M276.031,308.188h-40.063v-47.766h40.063V308.188z M318.656,150.813h-40.281v40.281h-44.75v-40.281h-40.281v-44.766h40.281V65.75h44.75v40.297h40.281V150.813z M380.453,260.422h37.563v47.766h-37.563V260.422z M420.594,414.188h-40.063v-47.766h40.063V414.188z"/></g>
        </svg>`)}`;

    const svg = d3.select("#map svg");

    const hospitalIconOffsets = {
        "6": { x: 10, y: 20 },
        "3": { x: 10, y: 30 },
        "9": { x: 10, y: 20 },
        "5": { x: 30, y: 45 },
        "16": { x: 10, y: -5 },
        // Add more offsets for other location IDs
    };


    hospitalLocations.forEach(locationId => {
        const path = svg.select(`#${CSS.escape(locationId)}`);
        if (!path.empty()) {
            let bbox = path.node().getBBox();
            let x = bbox.x + bbox.width / 2;
            let y = bbox.y + bbox.height / 2;

            const offset = hospitalIconOffsets[locationId] || { x: 0, y: 0 };
            svg.append("image")
                .attr("xlink:href", hospitalIconSVG)
                .attr("x", x - 10 + offset.x) // Offset to center the icon
                .attr("y", y - 10 + offset.y)
                .attr("width", 20)
                .attr("height", 20)
                .attr("class", "hospital-icon");
        }
    });
}

function appendNuclearIcons() {
    const nuclearLocations = ["4"];
    const nuclearIconSVG = `data:image/svg+xml;utf8,${encodeURIComponent(`<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 512 512"  xml:space="preserve">
    <style type="text/css">
        <![CDATA[
        .st0{fill:#000000;}
        ]]>
    </style>
    <g>
        <rect x="63.047" y="57.313" class="st0" width="385.906" height="45.844"/>
        <path class="st0" d="M427.938,126.094H84.063C84.063,320.953,0,454.688,0,454.688h512C512,454.688,427.938,320.953,427.938,126.094
		z M249.203,280.422c2.063-1.203,4.422-1.813,6.781-1.813c4.859,0,9.391,2.594,11.797,6.797c3.75,6.5,1.531,14.844-4.969,18.594
		c-2.078,1.188-4.438,1.828-6.797,1.828c-4.859,0-9.375-2.609-11.797-6.813C240.469,292.516,242.688,284.188,249.203,280.422z
		 M205.469,204.063l37.047,64.172c-8.641,5-13.469,14.047-13.484,23.359h-74.094C155,256.703,173.125,222.734,205.469,204.063z
		 M205.469,379.109l37.063-64.156c4.031,2.344,8.688,3.625,13.484,3.625c4.703,0,9.375-1.25,13.469-3.609h0.016l37.031,64.156
		C274.203,397.813,235.719,396.516,205.469,379.109z M282.969,291.594c0.031-4.672-1.188-9.313-3.609-13.5
		c-2.391-4.141-5.828-7.516-9.875-9.844l37.047-64.156c14.906,8.563,27.813,21.047,37,36.969
		c9.203,15.922,13.563,33.344,13.516,50.531H282.969z"/>
    </g>
    </svg>`)}`;
    

    const svg = d3.select("#map svg");

    nuclearLocations.forEach(locationId => {
        const path = svg.select(`#${CSS.escape(locationId)}`);
        if (!path.empty()) {
            let bbox = path.node().getBBox();
            let x = bbox.x + bbox.width / 2;
            let y = bbox.y + bbox.height / 2;

            svg.append("image")
                .attr("xlink:href", nuclearIconSVG)
                .attr("x", x - 10) // Offset to center the icon
                .attr("y", y - 10)
                .attr("width", 20)
                .attr("height", 20)
                .attr("class", "nuclear-icon");
        }
    });
}

// Function to create a legend for icons
function createIconLegend() {
    const svg = d3.select("#map").append("svg")
                  .attr("id", "icon-legend")
                  .attr("width", 200)
                  .attr("height", 100)
                  .style("position", "absolute")
                  .style("right", "1000px")
                  .style("top", "10px");

    // Define the icons with their descriptions and Base64 encoded SVGs
    const icons = [
        {
            // Base64 encoded hospital SVG from your provided function
            href: "data:image/svg+xml;base64," + btoa(`<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
            <svg version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="20px" height="20px" viewBox="0 0 512 512" xml:space="preserve">
            <style type="text/css"><![CDATA[.st0{fill:#000000;}]]></style>
            <g><path class="st0" d="M373.328,138.672V0H138.672v138.672H0V512h208V366.438h96V512h208V138.672H373.328z M131.469,414.188H91.406v-47.766h40.063V414.188z M131.469,308.188H91.406v-47.766h40.063V308.188z M276.031,308.188h-40.063v-47.766h40.063V308.188z M318.656,150.813h-40.281v40.281h-44.75v-40.281h-40.281v-44.766h40.281V65.75h44.75v40.297h40.281V150.813z M380.453,260.422h37.563v47.766h-37.563V260.422z M420.594,414.188h-40.063v-47.766h40.063V414.188z"/></g>
            </svg>`),
            description: "Hospital",
            x: 10,
            y: 10
        },
        {
            // Assuming the nuclear icon is also correctly encoded in your function
            href: "data:image/svg+xml;base64," + btoa(`<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
            <svg version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 512 512"  xml:space="preserve">
            <style type="text/css">
                <![CDATA[
                .st0{fill:#000000;}
                ]]>
            </style>
            <g>
                <rect x="63.047" y="57.313" class="st0" width="385.906" height="45.844"/>
                <path class="st0" d="M427.938,126.094H84.063C84.063,320.953,0,454.688,0,454.688h512C512,454.688,427.938,320.953,427.938,126.094
                z M249.203,280.422c2.063-1.203,4.422-1.813,6.781-1.813c4.859,0,9.391,2.594,11.797,6.797c3.75,6.5,1.531,14.844-4.969,18.594
                c-2.078,1.188-4.438,1.828-6.797,1.828c-4.859,0-9.375-2.609-11.797-6.813C240.469,292.516,242.688,284.188,249.203,280.422z
                 M205.469,204.063l37.047,64.172c-8.641,5-13.469,14.047-13.484,23.359h-74.094C155,256.703,173.125,222.734,205.469,204.063z
                 M205.469,379.109l37.063-64.156c4.031,2.344,8.688,3.625,13.484,3.625c4.703,0,9.375-1.25,13.469-3.609h0.016l37.031,64.156
                C274.203,397.813,235.719,396.516,205.469,379.109z M282.969,291.594c0.031-4.672-1.188-9.313-3.609-13.5
                c-2.391-4.141-5.828-7.516-9.875-9.844l37.047-64.156c14.906,8.563,27.813,21.047,37,36.969
                c9.203,15.922,13.563,33.344,13.516,50.531H282.969z"/>
            </g>
            </svg>`),
            description: "Nuclear Plant",
            x: 10,
            y: 60
        }
    ];

    // Append the icons and text to the SVG
    icons.forEach(icon => {
        svg.append("image")
            .attr("xlink:href", icon.href)
            .attr("x", icon.x)
            .attr("y", icon.y)
            .attr("width", 30)
            .attr("height", 30);

        svg.append("text")
            .attr("x", icon.x + 40)
            .attr("y", icon.y + 20)
            .text(icon.description)
            .attr("alignment-baseline", "middle")
            .attr("font-size", "12px");
    });
}

// Append this function call at the end of the script where the map is fully loaded



// Tooltip configuration and functionality
const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

function updateMapColors(aggregateData, selectedTimeIndex, selectedCategory, times) {
    const selectedTime = times[selectedTimeIndex];
    document.getElementById("timeLabel").textContent = selectedTime;

    const paths = d3.select("#map").selectAll("path");
    paths.each(function(d) {
        const pathElement = d3.select(this);
        const regionId = pathElement.attr("id");
        const regionData = aggregateData[regionId] && aggregateData[regionId][selectedTime];

        // Bind data to paths for tooltip interaction
        pathElement.data([regionData]) 
            .on('mouseover', function(event, d) {
                const avgDamage = d ? calculateAverageDamage(d, selectedCategory) : 'No data';
                const damageScore = avgDamage === 'No data' ? avgDamage : avgDamage.toFixed(2);

                // Style modifications for mouseover
                pathElement.style("stroke", "red") 
                           .style("stroke-width", "2px"); 

                tooltip.transition()
                       .duration(200)
                       .style("opacity", .9);
                tooltip.html(`Location: ${locationNames[regionId]}<br/>
                              Reports: ${d ? d.count : 'No data'}<br/>
                              Average Damage (${selectedCategory}): ${damageScore}`)
                       .style("left", (event.pageX) + "px")
                       .style("top", (event.pageY - 28) + "px");
            })
            .on('mouseout', function(d) {
                tooltip.transition()
                       .duration(500)
                       .style("opacity", 0);

                // Reset style on mouseout
                pathElement.style("stroke", "black") 
                           .style("stroke-width", "0.5px"); 
            });

        if (regionData) {
            const avgDamageLevel = calculateAverageDamage(regionData, selectedCategory);
            pathElement.style("fill", getColorForDamageLevel(avgDamageLevel));
        } else {
            pathElement.style("fill", "#ccc"); // Default color when no data
        }
    });
}

// Calculate average damage per category and location
function calculateAverageDamage(regionData, selectedCategory) {
    if (regionData.count > 0) {
        return regionData[selectedCategory] / regionData.count;
    } else {
        return 0;
    }
}

// Define color based on damage level
function getColorForDamageLevel(damageLevel) {
    if (damageLevel === 0) return "#ccc";
    if (damageLevel <= 2) return "#ffffcc";
    if (damageLevel <= 4) return "#ffeda0";
    if (damageLevel <= 6) return "#fed976";
    if (damageLevel <= 8) return "#feb24c";
    return "#f03b20";
}

// Initialize UI controls like sliders and buttons
function initializeSelectors(data, aggregateData) {
    let times = Array.from(new Set(data.map(d => d.time.split(' ')[0]))).sort((a, b) => new Date(a) - new Date(b));
    const timeSlider = d3.select("#timeSlider");
    timeSlider.attr("max", times.length - 1);

    timeSlider.on("input", function(event) {
        const selectedTimeIndex = event.target.value;
        const selectedCategory = d3.select("#categorySelector").node().value;
        updateMapColors(aggregateData, selectedTimeIndex, selectedCategory, times);
    });

    const categories = ['sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings', 'shake_intensity'];
    const categorySelector = d3.select("#categorySelector");
    categorySelector.selectAll("option")
        .data(categories)
        .enter()
        .append("option")
        .text(d => d)
        .attr("value", d => d);

    categorySelector.on("change", function(event) {
        const selectedCategory = event.target.value;
        const selectedTimeIndex = timeSlider.node().value;
        updateMapColors(aggregateData, selectedTimeIndex, selectedCategory, times);
    });

    const initialTimeIndex = 0;
    const initialCategory = categories[0];
    timeSlider.node().value = initialTimeIndex;
    categorySelector.node().value = initialCategory;
    updateMapColors(aggregateData, initialTimeIndex, initialCategory, times);
}

// Append location names to the SVG as text labels
const locationOffsets = {
    "1": { x: 5, y: -20 },   // Specific offset for location ID "1"
    "13": { x: 5, y: 5 }, 
    "3": { x: 5, y: 5 }, 
    "4": { x: 5, y: 20},
    "5": { x: 5, y: 25 }, 
    "14": { x: -10, y: 5 },
    "18": { x: 0, y: -25}, 
    "16": { x: -2, y: -25 }, 
    "8": { x: 5, y: 5 }, 
    "10": { x: 0, y: 35}, 
    "11": { x: 0, y: -20}, 
    "12": { x: 5, y: 20}, 
    "7": { x: -25, y: 20},

};
// Append names based on location IDs to the SVG map
function appendLocationNames() {
    const svg = d3.select("#map svg");

    Object.entries(locationNames).forEach(([id, name]) => {
        const path = svg.select(`#${CSS.escape(id)}`);
        if (!path.empty()) {
            let bbox = path.node().getBBox();
            let x = bbox.x + bbox.width / 2;
            let y = bbox.y + bbox.height / 2;

            // Apply offsets if they exist for the current location
            if (locationOffsets[id]) {
                x += locationOffsets[id].x || 0;
                y += locationOffsets[id].y || 0;
            }

            // Append a text element to the SVG
            svg.append("text")
                .attr("x", x)
                .attr("y", y)
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "middle")
                .attr("fill", "black") // You can change this as needed
                .attr("font-size", "8") // Adjust the font size as needed
                .text(name);
        }
    });
}

// Global variables for animation control
let playing = false;
let animationInterval;

// Function to step through the times and update the map
function step() {
    const currentValue = parseInt(d3.select("#timeSlider").property("value"), 10);
    const maxValue = parseInt(d3.select("#timeSlider").property("max"), 10);
    const newValue = currentValue < maxValue ? currentValue + 1 : 0;
    d3.select("#timeSlider").property("value", newValue).dispatch('input');
}

// Function to start the animation
function play() {
    if (!playing) {
        animationInterval = setInterval(step, 1000); // Adjust time interval to your preference
        playing = true;
    }
}

// Function to pause the animation
function pause() {
    if (playing) {
        clearInterval(animationInterval);
        playing = false;
    }
}

// Function to initialize play and pause button event listeners
function initializeAnimationControls() {
    d3.select("#play-button").on("click", play);
    d3.select("#pause-button").on("click", pause);
}

// Call this function after the map is loaded and selectors are initialized
initializeAnimationControls();



