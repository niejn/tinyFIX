$PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent
. "$PSScriptRoot\tiny_fix.ps1"
 
try
{
    minimalFixInitialise
 
    [int]$simulatorPort = 5555
    [string]$simulatorCompId = "SERVER"
    [string]$clientCompId="CLIENT"
 
    Write-Host ""
    Write-Host "Client is starting on port $simulatorPort with compid $clientCompId" -foregroundcolor "Yellow"
    Write-Host ""
 
    $fixClient = New-Object FixClient
    $fixClient.initialise("FIX.4.2", "127.0.0.1", $simulatorPort, $clientCompId, $simulatorCompId)
	
	$fixClient.connect()
	
	$order = $fixClient.FixSession.getBaseMessage( [FixConstants]::FIX_MESSAGE_NEW_ORDER )
	$order.setTag([FixConstants]::FIX_TAG_CLIENT_ORDER_ID , 1)
	$order.setTag([FixConstants]::FIX_TAG_SYMBOL ,  "GOOGL")
	$order.setTag([FixConstants]::FIX_TAG_ORDER_QUANTITY, 100)
	$order.setTag([FixConstants]::FIX_TAG_ORDER_PRICE , 300)
	$order.setTag([FixConstants]::FIX_TAG_ORDER_SIDE , [FixConstants]::FIX_ORDER_SIDE_BUY)
	
    $fixClient.send($order)
	
	Write-Host
    Write-Host "Sent : " -foregroundcolor "Yellow"
    Write-Host $order.toString($false)
    Write-Host
	
	$execReport = $fixClient.recv()
	
	Write-Host
    Write-Host "Received : " -foregroundcolor "Yellow"
    Write-Host $execReport.toString($false)
    Write-Host
}
catch
{}
finally
{
    if( $fixClient.FixSession.Connected -eq $true)
    {
        $fixClient.disconnect()
    }
    Write-Host "Press any key to continue..."
    $x = $host.ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}