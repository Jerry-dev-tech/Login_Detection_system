// ======================================
// LOGIN ACTIVITY CHART
// ======================================

if (document.getElementById("hourChart")) {

    new Chart(document.getElementById("hourChart"), {

        type: "bar",

        data: {

            labels: hourLabels,

            datasets: [{

                label: "Login Activity",

                data: hourValues,

                backgroundColor: "#3b82f6",

                borderRadius: 8,

                borderSkipped: false

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    grid: {

                        color: "rgba(255,255,255,.08)"

                    }

                },

                x: {

                    grid: {

                        display: false

                    }

                }

            }

        }

    });

}



// ======================================
// THREAT DISTRIBUTION
// ======================================

if (document.getElementById("statusChart")) {

    new Chart(document.getElementById("statusChart"), {

        type: "doughnut",

        data: {

            labels: [

                "Normal",

                "Suspicious"

            ],

            datasets: [{

                data: [

                    normalCount,

                    suspiciousCount

                ],

                backgroundColor: [

                    "#22c55e",

                    "#ef4444"

                ],

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "70%",

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}



// ======================================
// COUNTRY CHART
// ======================================

if (document.getElementById("countryChart")) {

    new Chart(document.getElementById("countryChart"), {

        type: "bar",

        data: {

            labels: countryLabels,

            datasets: [{

                label: "Country Distribution",

                data: countryValues,

                backgroundColor: "#06b6d4",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

}