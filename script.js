const reportData = []; // Report data will be populated here
    let workSessionStart = null;

    // Function to add data to the report table
    function populateReportTable() {
        const reportTable = document.getElementById("reportTable").getElementsByTagName('tbody')[0];
        
        reportData.forEach(entry => {
            const row = reportTable.insertRow();
            row.insertCell(0).textContent = entry["Work session start"];
            row.insertCell(1).textContent = entry["Work session stop"];
            row.insertCell(2).textContent = entry["Elapsed time"];
            row.insertCell(3).textContent = entry["Task time"];
            row.insertCell(4).textContent = entry["Task description"];
        });
    }

    // Function to start a work session
    function startWork() {
        workSessionStart = new Date();
    }

    // Function to stop a work session
    function stopWork() {
        if (workSessionStart) {
            const currentTime = new Date();
            reportData.push({
                "Work session start": workSessionStart,
                "Work session stop": currentTime,
                "Elapsed time": calculateElapsedTime(workSessionStart, currentTime),
                "Task time": "N/A",
                "Task description": "Work Session"
            });

            workSessionStart = null;
            populateReportTable();
        }
    }

    // Function to calculate elapsed time
    function calculateElapsedTime(startTime, endTime) {
        const elapsedMilliseconds = endTime - startTime;
        const hours = Math.floor(elapsedMilliseconds / (1000 * 60 * 60));
        const minutes = Math.floor((elapsedMilliseconds % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((elapsedMilliseconds % (1000 * 60)) / 1000);
        return `${hours}h ${minutes}m ${seconds}s`;
    }

    // Function to add work data
    function addWork() {
        const workDescription = document.getElementById("workDescription").value;
        if (workSessionStart) {
            const currentTime = new Date();
            reportData.push({
                "Work session start": workSessionStart,
                "Work session stop": currentTime,
                "Elapsed time": calculateElapsedTime(workSessionStart, currentTime),
                "Task time": currentTime,
                "Task description": workDescription
            });

            populateReportTable();
        }
    }

    // Function to clear work data
    function clearWork() {
        reportData.length = 0; // Clear the array
        workSessionStart = null;
        const reportTable = document.getElementById("reportTable").getElementsByTagName('tbody')[0];
        reportTable.innerHTML = ""; // Clear the report table
    }

    // Function to export data to Excel
    function exportToExcel() {
        const wb = XLSX.utils.book_new();
        wb.Props = {
            Title: "Work Report",
            Author: "Your Name",
            CreatedDate: new Date()
        };
        wb.SheetNames.push("Report Data");
        const wsData = reportData.map(entry => [
            entry["Work session start"],
            entry["Work session stop"],
            entry["Elapsed time"],
            entry["Task time"],
            entry["Task description"]
        ]);
        const ws = XLSX.utils.aoa_to_sheet(wsData);
        wb.Sheets["Report Data"] = ws;
        const excelFileName = "work_report.xlsx";
        XLSX.writeFile(wb, excelFileName);
    }

    // Add event listeners to buttons
    document.addEventListener("DOMContentLoaded", function() {
        populateReportTable();
        
        const startWorkButton = document.getElementById("startWorkButton");
        startWorkButton.addEventListener("click", startWork);
        
        const stopWorkButton = document.getElementById("stopWorkButton");
        stopWorkButton.addEventListener("click", stopWork);
        
        const addWorkButton = document.getElementById("addWorkButton");
        addWorkButton.addEventListener("click", addWork);
        
        const clearWorkButton = document.getElementById("clearWorkButton");
        clearWorkButton.addEventListener("click", clearWork);
        
        const exportButton = document.getElementById("exportButton");
        exportButton.addEventListener("click", exportToExcel);
    });