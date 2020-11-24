# stop execution on error, defensive strategy, taken from https://stackoverflow.com/a/44810914
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$PSDefaultParameterValues['*:ErrorAction'] = 'Stop'



# set here the name of the virtual environment
$venv_name = 'venv'



# Test if venv file exists
if (!(Test-Path $venv_name)) {

    Write-Host "virtual environment does not exists: "-NoNewline; Write-Host $venv_name -ForegroundColor Magenta -NoNewline; $confirmation = Read-Host ". Create? [y/n]"
    
    if ($confirmation -eq 'y') {
        # create the virtual environment
        if ($null -eq (Get-Command "virtualenv" -ErrorAction SilentlyContinue)) { 
            Write-Host "Unable to find virtualenv.exe in your PATH."
            Write-Host "Make sure you have the the virtualenv.exe in your path."
            Write-Host "If not, you can modify this script, see the comments."
                
        }
        else {
            # if you do not have virtualenv in your path, you can place it here
            # but please, do not commit this change to the source control
            # todo - supply it as a parameter
            virtualenv $venv_name
            $activate = (Join-Path $venv_name "Scripts\Activate.ps1")
            . $activate
            pip install -r requirements.txt
            deactivate
        }
    }
    else {
        Write-Host("(Quiting the script.)")
    }
}
# if exists activate it
if (Test-Path $venv_name) {
    $activate = (Join-Path $venv_name "Scripts\Activate.ps1")
    . $activate
    Write-Host "Activated virtual environment " -NoNewline; Write-Host $venv_name -ForegroundColor Magenta -NoNewline; Write-Host  ". Currently installed packages:";
    Write-Host ""
    pip freeze
    Write-Host ""
    Write-Host "Run " -NoNewline; Write-Host "deactivate" -ForegroundColor Magenta -NoNewline; Write-Host " to deactivate the active virtual environment."
}
