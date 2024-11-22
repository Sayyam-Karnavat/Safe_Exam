# Get the current console window's process ID
$currentConsoleId = (Get-Process -Id $PID).Id

# Get a list of all conhost.exe processes
$conhostProcesses = Get-Process conhost

# Iterate through the list of conhost processes
foreach ($process in $conhostProcesses) {
    # Skip the current console window
    if ($process.Id -ne $currentConsoleId) {
        # Kill the process
        Stop-Process -Id $process.Id -Force
    }
}

# Kill Python processes
$pythonProcesses = Get-Process python

foreach ($process in $pythonProcesses) {
    # Kill the process
    Stop-Process -Id $process.Id -Force
}

# Finally, kill the current console window (optional, uncomment if needed)
Stop-Process -Id $currentConsoleId -Force
