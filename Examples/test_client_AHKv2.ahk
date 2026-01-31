; Examples/test_client_AHKv2.ahk

path := A_ScriptDir "\..\client\"


SendCommand(action, args := "") {
    cmd := 'python ' path  'send_command.py "' action '" "' args '"'

    ToolTip(cmd)
    RunWait(cmd,, "Hide")
}

1::{
    SendCommand("load")
}
2::{
    SendCommand("unload")
}
3::{
    SendCommand("start")
}
4::{
    SendCommand("stop")
}
5::{
    SendCommand("hello")
}