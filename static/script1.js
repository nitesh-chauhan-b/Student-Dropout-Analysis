function showContent(contentId) {
    const containers = document.querySelectorAll('.container');
    containers.forEach(container => {
        container.classList.remove('active-container');
    });
    document.getElementById(contentId).classList.add('active-container');
}


// the below funntion is for hiding the footer
function hideanything(shouldhide) {
    var hiddenid = document.getElementById("hidethis");
    if(hiddenid){
        hiddenid.style.display = shouldhide ? "none" : "block";
    }
    else{
        console.error("the tag with id is not there");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    showContent('info');
});


// // this is for backend
// function addDataToTable(index, name, age, email) {
//     const table = document.getElementById("dataTable").getElementsByTagName('tbody')[0];
//     const newRow = table.insertRow(table.rows.length);

//     const cellIndex = newRow.insertCell(0);
//     cellIndex.innerHTML = index;

//     const cellName = newRow.insertCell(1);
//     cellName.innerHTML = name;

//     const cellAge = newRow.insertCell(2);
//     cellAge.innerHTML = age;

//     const cellEmail = newRow.insertCell(3);
//     cellEmail.innerHTML = email;


// }

// // Function to reset the form and hide it
// function resetForm() {
//     document.getElementById("dataForm").reset();
//     document.getElementById("dataForm").style.display = "none";
// }

// // Event listener for "Add Data" button
// document.getElementById("addDataButton").addEventListener("click", function () {
//     document.getElementById("dataForm").style.display = "block";
// });

// // Event listener for form submission
// document.getElementById("dataForm").addEventListener("submit", function (e) {
//     e.preventDefault();

//     const name = document.getElementById("name").value;
//     const age = document.getElementById("age").value;
//     const email = document.getElementById("email").value;


//     const table = document.getElementById("dataTable");
//     const index = table.rows.length; // Index is the number of rows in the table

//     addDataToTable(index, name, age, email);
//     resetForm();
// });



                    var data1Element110 = document.getElementById('demo110');
                    var data110 = data1Element110.textContent;

                    var data1Element111 = document.getElementById('demo111');
                    var data111 = data1Element111.textContent;

                    var data1Element112 = document.getElementById('demo112');
                    var data112 = data1Element112.textContent;

                    var data1Element113 = document.getElementById('demo113');
                    var data113 = data1Element113.textContent;


                // Sample data for student dropout rate by father's income (in lakhs per year)
                const incomeCategories = ['0-10000', '10001-50000', '50001-100000','100000>'];
                const dropoutRates_i = [data110, data111, data112,data113]; // Dropout rates for each income category

                // Create a bar chart
                var ctx = document.getElementById('dropoutChart_Income_wise').getContext('2d');
                var dropoutChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: incomeCategories.map(category => `${category}`),
                        datasets: [{
                            label: 'Dropout',
                            data: dropoutRates_i,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Dropout'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: "Father's Income (per Month)"
                                }
                            }


                        }
                    }
                });

             

                    var data1Element200 = document.getElementById('demo200');
                    var data200 = data1Element200.textContent;

                    var data1Element201 = document.getElementById('demo201');
                    var data201 = data1Element201.textContent;

                    var data1Element202 = document.getElementById('demo202');
                    var data202 = data1Element202.textContent;

                    var data1Element203 = document.getElementById('demo203');
                    var data203 = data1Element203.textContent;


                // Data
                const casteCategories = ['General', 'Scheduled Tribes (ST)', 'Scheduled Cast (SC)', 'Other Backward Class (OBC)'];
                const dropoutRates = [data200, data201, data202, data203]; // Dropout rates for each caste category

                // Create a bar chart
                var ctx = document.getElementById('dropoutChart_Cast_wise').getContext('2d');
                var dropoutChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: casteCategories,
                        datasets: [{
                            label: 'Dropout',
                            data: dropoutRates,
                            backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(255, 205, 86, 0.6)', 'rgba(54, 162, 235, 0.6)'],
                            borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(255, 205, 86, 1)', 'rgba(54, 162, 235, 1)'],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Dropout'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Caste Category'
                                }
                            }
                        }
                    }
                });




// male female                

              var data1Element102 = document.getElementById('demo102');
              var data102 = data1Element102.textContent;

              var data1Element101 = document.getElementById('demo101');
              var data101 = data1Element101.textContent;

              var data1Element100 = document.getElementById('demo100');
              var data100 = data1Element100.textContent;


                               // Data
                const totalStudents = 100;
                const totalDropouts = data102;

                const maleDropouts = data100;
                const femaleDropouts = data101;

                // Create a pie chart
                var ctx = document.getElementById('dropoutChart_Gender_wise').getContext('2d');
                var dropoutChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ['Male', 'Female'],
                        datasets: [{
                            data: [maleDropouts, femaleDropouts],
                            backgroundColor: ['#0074A3', '#F3BA00'],
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: {
                                    // This more specific font property overrides the global property
                                    font: {
                                        size: 18
                                    }
                                }
                            }
                        }
                    }
                });



// bar age chart


                var data1Element5 = document.getElementById('demo5');
                var data5 = data1Element5.textContent;

                var data1Element10 = document.getElementById('demo10');
                var data10 = data1Element10.textContent;

                var data1Element15 = document.getElementById('demo15');
                var data15 = data1Element15.textContent;

                var data1Element20 = document.getElementById('demo20');
                var data20 = data1Element20.textContent;


                // Data
                const dropoutData = [
                    { ageGroup: '0-5', dropoutCount: data5 },
                    { ageGroup: '6-10', dropoutCount: data10 },
                    { ageGroup: '11-15', dropoutCount: data15 },
                    { ageGroup: '16-20', dropoutCount: data20 },
                ];

                // Extract labels and data values from the data
                const labels = dropoutData.map(item => item.ageGroup);
                const dataValues = dropoutData.map(item => item.dropoutCount);

                // Create a chart
                var ctx = document.getElementById('dropoutChart_Age_wise').getContext('2d');
                var dropoutChart = new Chart(ctx, {
                    type: 'bar', // Bar chart type
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Student Dropout Count',
                            data: dataValues,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 3
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                beginAtZero: true
                            },
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });






// pie chat

               var data1Element4000 = document.getElementById('demo4000');
               var demo4000 = data1Element4000.textContent;

               var data1Element = document.getElementById('demo');
               var data1 = data1Element.textContent;
                // Data for the pie chart
                var data = {
                    labels: ['School Students', 'Dropout Students'],
                    datasets: [{
                        data: [demo4000, data1 ],
                        backgroundColor: ['#0074A3', '#F3BA00'],
                    }]
                };

                // Create the pie chart
                var ctx = document.getElementById('dropoutChart').getContext('2d');
                var dropoutChart = new Chart(ctx, {
                    type: 'pie',
                    data: data,
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            legend: {
                                labels: {
                                    // This more specific font property overrides the global property
                                    font: {
                                        size: 18
                                    }
                                }
                            }
                        }
                    }
                });


// category

var data1Element781 = document.getElementById('demo781');
var demo781 = data1Element781.textContent;

var data1Element791 = document.getElementById('demo791');
var demo791 = data1Element791.textContent;

var data1Element801 = document.getElementById('demo801');
var demo801 = data1Element801.textContent;


// Create a pie chart
var ctx = document.getElementById('dropoutChart_Category_wise').getContext('2d');
var dropoutChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Private', 'Goverment','Semi-Goverment'],
        datasets: [{
            data: [demo781,demo791,demo801],
            backgroundColor: ['#0082B6', '#FFF700','#00FF97'],
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 18
                    }
                }
            }
        }
    }
});

