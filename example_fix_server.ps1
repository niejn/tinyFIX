$PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent
. "$PSScriptRoot\tiny_fix.ps1"

[console]::TreatControlCAsInput = $true
 
try
{
    minimalFixInitialise
 
    [int]$simulatorPort = 5555
    [string]$simulatorCompId = "SERVER"
    [string]$simulatorSubId = "01"
    [int]$execId=1
 
    Write-Host ""
    Write-Host "Venue simulator is starting on port $simulatorPort with compid $simulatorCompId" -foregroundcolor "Yellow"
    Write-Host ""
 
    Set-Location $PSScriptRoot
 
    $fixServer = New-Object FixServer
    $fixServer.FixSession.RestoreSequenceNumbersFromFile = $true # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
    $fixServer.FixSession.TimePrecision = [FixTime]::FIX_MICROSECONDS # Default value is FIX_MILLISECONDS, you can also set to FIX_SECONDS
    
    $connected = $fixServer.start($simulatorPort, $simulatorCompId, $simulatorSubId) # Responds with logon message, you can customise it by passing a FIX message
    
    while($true)
    {
        $fixMessage = $fixServer.recv()
   
        if( $fixMessage -eq $null)
        {
            continue
        }
 
        Write-Host
        Write-Host "Received : " -foregroundcolor "Yellow"
        Write-Host $fixMessage.toString($false)
        Write-Host
        
        $messageType = $fixMessage.getMessageType()
   
        if( $messageType -eq [FixConstants]::FIX_MESSAGE_LOG_OFF )
        {
            Write-Host
            Write-Host "Client logged off " -foregroundcolor "Yellow"
            Write-Host
            break
        }
        elseif( $messageType -eq [FixConstants]::FIX_MESSAGE_HEARTBEAT )
        {
            Write-Host "Client sent heartbeat " -foregroundcolor "Yellow"
            continue
        }
        else
        {
            [string]$clientOrderId = $fixMessage.getTagValue([FixConstants]::FIX_TAG_CLIENT_ORDER_ID)
            $execReport = $fixServer.FixSession.getBaseMessage( [FixConstants]::FIX_MESSAGE_EXECUTION_REPORT)
            $execReport.setTag( [FixConstants]::FIX_TAG_CLIENT_ORDER_ID,  $clientOrderId)
            $execReport.setTag( [FixConstants]::FIX_TAG_EXEC_ID, $execId.ToString() )
            $execReport.setTag( [FixConstants]::FIX_TAG_ORDER_STATUS, [FixConstants]::FIX_ORDER_STATUS_NEW )
            $execReport.setTag( [FixConstants]::FIX_TAG_EXEC_TYPE, [FixConstants]::FIX_ORDER_STATUS_NEW )
            $sent = $fixServer.send($execReport)
 
            Write-Host
            Write-Host "Sent : " -foregroundcolor "Yellow"
            Write-Host $execReport.toString($false)
            Write-Host
 
            $execId++
        }
 
        if ([console]::KeyAvailable)
        {
            $key = [system.console]::readkey($true)
            if (($key.modifiers -band [consolemodifiers]"control") -and ($key.key -eq "C"))
            {
                break
            }
        }
    }
}
catch
{}
finally
{
    $fixServer.disconnect() # You can also pass a custom logoff message
    Write-Host "Press any key to continue..."
    $x = $host.ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}