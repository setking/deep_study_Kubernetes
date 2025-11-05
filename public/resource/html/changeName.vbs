' 批量替换文件名中的特定文本，去掉生成的文件名后缀_modified，不过要先删除原文件
Set fso = CreateObject("Scripting.FileSystemObject")

' 设置要处理的文件夹路径
folderPath = "F:\study\deepKubernetes\kubernetes\public\resource\html"  ' 修改为你的文件夹路径

' 设置要替换的文本和新文本
oldText = "_modified"  ' 要替换的文本
newText = ""  ' 替换后的新文本

' 检查文件夹是否存在
If Not fso.FolderExists(folderPath) Then
    WScript.Echo "文件夹不存在: " & folderPath
    WScript.Quit
End If

Set folder = fso.GetFolder(folderPath)
Set files = folder.Files

Dim count
count = 0

' 遍历所有文件
For Each file In files
    oldName = file.Name
    ' 检查文件名是否包含要替换的文本
    If InStr(oldName, oldText) > 0 Then
        newName = Replace(oldName, oldText, newText)
        
        ' 构建完整的旧路径和新路径
        oldPath = folderPath & "\" & oldName
        newPath = folderPath & "\" & newName
        
        ' 重命名文件
        On Error Resume Next
        fso.MoveFile oldPath, newPath
        If Err.Number = 0 Then
            WScript.Echo "重命名成功: " & oldName & " -> " & newName
            count = count + 1
        Else
            WScript.Echo "重命名失败: " & oldName & " - 错误: " & Err.Description
            Err.Clear
        End If
        On Error Goto 0
    End If
Next

WScript.Echo "完成! 共处理 " & count & " 个文件"