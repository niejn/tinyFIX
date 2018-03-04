$PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent
. "$PSScriptRoot\tiny_fix.ps1"
 
try
{
    minimalFixInitialise
 
    [int]$simulatorPort = 5555
    [string]$simulatorCompId = "SERVER"
    [string]$clientCompId="CLIENT"
    [string]$simulatorSubId = "01"
    [string]$clientSubId = "01"
 
    Write-Host ""
    Write-Host "Client is starting on port $simulatorPort with compid $clientCompId" -foregroundcolor "Yellow"
    Write-Host ""
 
    $fixClient = New-Object FixClient
    $fixClient.initialise([FixConstants]::FIX_VERSION_4_2, "127.0.0.1", $simulatorPort, $clientCompId, $clientSubId, $simulatorCompId, $simulatorSubId)
    $fixClient.FixSession.RestoreSequenceNumbersFromFile = $true # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
    $fixClient.FixSession.TimePrecision = [FixTime]::FIX_MICROSECONDS # Default value is FIX_MILLISECONDS, you can also set to FIX_SECONDS
    $connected = $fixClient.connect() # You can also pass a custom logon fix message
    
    if( $fixClient.FixSession.Connected)
    {
        for($i = 0; $i -lt 3 ; $i++)
        {
            $order = $fixClient.FixSession.getBaseMessage( [FixConstants]::FIX_MESSAGE_NEW_ORDER )
            $order.setTag([FixConstants]::FIX_TAG_CLIENT_ORDER_ID , 1)
            $order.setTag([FixConstants]::FIX_TAG_SYMBOL ,  "GOOGL")
            $order.setTag([FixConstants]::FIX_TAG_ORDER_QUANTITY, 100)
            $order.setTag([FixConstants]::FIX_TAG_ORDER_PRICE , 300)
            $order.setTag([FixConstants]::FIX_TAG_ORDER_SIDE , [FixConstants]::FIX_ORDER_SIDE_BUY)
            
            # Adding a repeating group to the order
            $order.setTag(453,2)
            $order.setTag(448,1234)
            $order.setTag(447,'P')
            $order.setTag(452,1)
            $order.setTag(448,1235)
            $order.setTag(447,'D')
            $order.setTag(452,2)
            
            $sent = $fixClient.send($order)
            
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
    }
}
catch
{
}
finally
{
    $fixClient.disconnect() # You can also pass a custom logoff message
    Write-Host "Press any key to continue..."
    $x = $host.ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}