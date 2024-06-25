# CHANGE ENV IN WINDOWS

$ENV_FILE_PATH="./.env"
$CONFIG_FILE_PATH="./src/config.env.js"

if(-not(Test-Path -Path $ENV_FILE_PATH)){
    Write-Host ".env file not found"
    Write-Host "creating .env file"
    New-Item -ItemType File -Path $ENV_FILE_PATH -Force -ErrorAction Stop
}

Write-Host "updating .env ..."

$TARGET_ENV = Get-Content "./$($args[0])"

$NEW_ENV_FILE = $TARGET_ENV -replace "[ ]=[ ]*","="
$NEW_ENV_FILE = $NEW_ENV_FILE -replace "\s(?!PRIVATE|KEY)","n"

Set-Content -Path $ENV_FILE_PATH -Value $NEW_ENV_FILE

Write-Host ".env updated"

$CONFIG_FILE = $NEW_ENV_FILE -replace "\s(?!PRIVATE|KEY)",","
$CONFIG_FILE = $CONFIG_FILE -replace "=",":"

if(-not(Test-Path -Path $CONFIG_FILE_PATH)){
    Write-Host "config.env.js not found"
    Write-Host "creating .config.env.js"
    New-Item -ItemType File -Path $CONFIG_FILE_PATH -Force -ErrorAction Stop
    Write-Host "config.env.js created"
}

$KEY_VALUE = ""

ForEach($item in $CONFIG_FILE){
    $array=$item.Split(':')
    if($array.Count -gt 2){
        $KEY_VALUE = $KEY_VALUE + "$($array[0]):'$($array[1]):$($array[2])', "
    }else{
        $KEY_VALUE = $KEY_VALUE + "$($array[0]):'$($array[1])', "
    }
}

$KEY_VALUE = $KEY_VALUE + "generatedAt:'$(Get-Date -Format yyyy-MM-ddTHH:mm:ss)'"

Write-Host "updating config.env.js"
$JSON = "export default {$KEY_VALUE}"
Set-Content -Path $CONFIG_FILE_PATH -Value $JSON
Write-Host "config.env.js updated"
