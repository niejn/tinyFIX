$PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent
. "$PSScriptRoot\tiny_fix.ps1"

[console]::TreatControlCAsInput = $true
 
try
{
    minimalFixInitialise
 
    [int]$simulatorPort = 5555
    [string]$simulatorCompId = "SERVER"
    [string]$clientCompId="CLIENT"
    [int]$execId=1
 
    Write-Host ""
    Write-Host "Venue simulator is starting on port $simulatorPort with compid $simulatorCompId" -foregroundcolor "Yellow"
    Write-Host ""
 
    Set-Location $PSScriptRoot
 
    $fixServer = New-Object FixServer
    $fixServer.start($simulatorPort, $simulatorCompId, $clientCompId)
 
    while($true)
    {
        $fixMessage = $fixServer.recv()
   
        if( $fixMessage -eq $null)
        {
            continue
        }
   
        $messageType = $fixMessage.getMessageType().ToString()
 
        Write-Host
        Write-Host "Received : " -foregroundcolor "Yellow"
        Write-Host $fixMessage.toString($false)
        Write-Host
   
        if( $messageType -eq [FixConstants]::FIX_MESSAGE_LOG_OFF )
        {
            $fixServer.send($fixServer.FixSession.getLogoffMessage())
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
            $fixServer.send($execReport)
 
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
    if( $fixServer.FixSession.Connected -eq $true)
    {
        $fixServer.disconnect()
    }
    Write-Host "Press any key to continue..."
    $x = $host.ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}